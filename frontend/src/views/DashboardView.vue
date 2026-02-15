<template>
  <section class="space-y-5">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h2 class="text-2xl font-semibold">Dashboard</h2>
        <p class="text-sm text-slate-500">Monthly savings, projections, and recent activity.</p>
      </div>
      <div class="flex items-center gap-2">
        <select v-model.number="selectedMonth" class="rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm">
          <option v-for="month in months" :key="month.value" :value="month.value">{{ month.label }}</option>
        </select>
        <input v-model.number="selectedYear" type="number" class="w-24 rounded-lg border border-slate-200 px-3 py-2 text-sm" />
      </div>
    </div>

    <div class="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
      <article class="rounded-xl border border-slate-200 bg-white p-4">
        <p class="text-xs uppercase tracking-wide text-slate-500">Income</p>
        <p class="mt-1 text-2xl font-semibold text-brand-700">{{ fmt(monthly?.total_income) }}</p>
      </article>
      <article class="rounded-xl border border-slate-200 bg-white p-4">
        <p class="text-xs uppercase tracking-wide text-slate-500">Expense</p>
        <p class="mt-1 text-2xl font-semibold text-rose-600">{{ fmt(monthly?.total_expense) }}</p>
      </article>
      <article class="rounded-xl border border-slate-200 bg-white p-4">
        <p class="text-xs uppercase tracking-wide text-slate-500">Net Savings</p>
        <p class="mt-1 text-2xl font-semibold">{{ fmt(monthly?.net_savings) }}</p>
      </article>
      <article class="rounded-xl border border-slate-200 bg-white p-4">
        <p class="text-xs uppercase tracking-wide text-slate-500">Projected Month-End Spend</p>
        <p class="mt-1 text-2xl font-semibold text-amber-700">{{ fmt(projection?.projected_month_end) }}</p>
      </article>
    </div>

    <div class="grid gap-4 xl:grid-cols-2">
      <article class="rounded-xl border border-slate-200 bg-white p-4">
        <h3 class="mb-3 text-sm font-medium text-slate-700">Income vs Expense</h3>
        <Bar v-if="barData" :data="barData" :options="barOptions" />
      </article>

      <article class="rounded-xl border border-slate-200 bg-white p-4">
        <h3 class="mb-3 text-sm font-medium text-slate-700">Expense Category Split</h3>
        <Doughnut v-if="donutData" :data="donutData" />
      </article>
    </div>

    <article class="rounded-xl border border-slate-200 bg-white p-4">
      <div class="mb-3 flex items-center justify-between">
        <h3 class="text-sm font-medium text-slate-700">Most Recent Transactions</h3>
        <RouterLink to="/transactions" class="text-sm text-brand-700 hover:underline">View all</RouterLink>
      </div>
      <div class="overflow-x-auto">
        <table class="min-w-full text-sm">
          <thead>
            <tr class="border-b border-slate-200 text-left text-xs uppercase tracking-wide text-slate-500">
              <th class="py-2">Date</th>
              <th class="py-2">Type</th>
              <th class="py-2">Category</th>
              <th class="py-2 text-right">Amount</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="txn in recentTransactions" :key="txn.id" class="border-b border-slate-100">
              <td class="py-2">{{ txn.transaction_date }}</td>
              <td class="py-2 capitalize">{{ txn.type }}</td>
              <td class="py-2 capitalize">{{ txn.category }}</td>
              <td class="py-2 text-right font-medium">{{ fmt(txn.amount) }}</td>
            </tr>
            <tr v-if="recentTransactions.length === 0">
              <td colspan="4" class="py-4 text-center text-slate-400">No transactions yet.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </article>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { RouterLink } from "vue-router";
import { Bar, Doughnut } from "vue-chartjs";
import {
  ArcElement,
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  Tooltip
} from "chart.js";
import { getCategoryBreakdown, getMonthlySummary, getProjection, getTransactions } from "../services/api";
import type { CategoryBreakdown, MonthlySummary, ProjectionSummary, Transaction } from "../types/api";

ChartJS.register(ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend);

const now = new Date();
const selectedMonth = ref(now.getMonth() + 1);
const selectedYear = ref(now.getFullYear());

const monthly = ref<MonthlySummary | null>(null);
const projection = ref<ProjectionSummary | null>(null);
const categories = ref<CategoryBreakdown | null>(null);
const recentTransactions = ref<Transaction[]>([]);

const months = [
  { value: 1, label: "Jan" },
  { value: 2, label: "Feb" },
  { value: 3, label: "Mar" },
  { value: 4, label: "Apr" },
  { value: 5, label: "May" },
  { value: 6, label: "Jun" },
  { value: 7, label: "Jul" },
  { value: 8, label: "Aug" },
  { value: 9, label: "Sep" },
  { value: 10, label: "Oct" },
  { value: 11, label: "Nov" },
  { value: 12, label: "Dec" }
];

const barData = computed(() => {
  if (!monthly.value) return null;
  return {
    labels: ["Income", "Expense"],
    datasets: [
      {
        label: "Monthly totals",
        data: [Number(monthly.value.total_income), Number(monthly.value.total_expense)],
        backgroundColor: ["#2e8668", "#f43f5e"]
      }
    ]
  };
});

const barOptions = {
  responsive: true,
  maintainAspectRatio: false
};

const donutData = computed(() => {
  if (!categories.value || categories.value.items.length === 0) return null;
  return {
    labels: categories.value.items.map((item) => item.category),
    datasets: [
      {
        data: categories.value.items.map((item) => Number(item.total)),
        backgroundColor: ["#2e8668", "#49a283", "#78c1a8", "#f59e0b", "#ef4444", "#0ea5e9", "#6366f1"]
      }
    ]
  };
});

function fmt(value?: string | number | null) {
  const parsed = Number(value ?? 0);
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(parsed);
}

async function loadData() {
  const [monthlyRes, projectionRes, categoryRes, txnRes] = await Promise.all([
    getMonthlySummary(selectedYear.value, selectedMonth.value),
    getProjection(selectedYear.value, selectedMonth.value),
    getCategoryBreakdown(selectedYear.value, selectedMonth.value),
    getTransactions(1, 8)
  ]);

  monthly.value = monthlyRes.data;
  projection.value = projectionRes.data;
  categories.value = categoryRes.data;
  recentTransactions.value = txnRes.data?.data ?? [];
}

watch([selectedMonth, selectedYear], loadData);
onMounted(loadData);
</script>

<style scoped>
canvas {
  min-height: 260px;
}
</style>
