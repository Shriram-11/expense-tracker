<template>
  <section class="space-y-5">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h2 class="text-2xl font-semibold">Expenditure</h2>
        <p class="text-sm text-slate-500">Deep breakdown of where your money is going.</p>
      </div>
      <div class="flex items-center gap-2">
        <select v-model.number="selectedMonth" class="rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm">
          <option v-for="month in months" :key="month.value" :value="month.value">{{ month.label }}</option>
        </select>
        <input v-model.number="selectedYear" type="number" class="w-24 rounded-lg border border-slate-200 px-3 py-2 text-sm" />
      </div>
    </div>

    <div class="grid gap-4 xl:grid-cols-2">
      <article class="rounded-xl border border-slate-200 bg-white p-4">
        <h3 class="mb-3 text-sm font-medium text-slate-700">Category Share</h3>
        <Doughnut v-if="donutData" :data="donutData" />
        <p v-else class="text-sm text-slate-400">No category expense data for this month.</p>
      </article>
      <article class="rounded-xl border border-slate-200 bg-white p-4">
        <h3 class="mb-3 text-sm font-medium text-slate-700">Category Ranking</h3>
        <ul class="space-y-2 text-sm">
          <li v-for="item in items" :key="item.category"
            class="flex items-center justify-between rounded-lg border border-slate-100 bg-slate-50 px-3 py-2">
            <span class="capitalize">{{ item.category }}</span>
            <span class="font-medium">{{ fmt(item.total) }}</span>
          </li>
          <li v-if="items.length === 0" class="text-slate-400">No data for selected month.</li>
        </ul>
      </article>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { Doughnut } from "vue-chartjs";
import { ArcElement, Chart as ChartJS, Legend, Tooltip } from "chart.js";
import { getCategoryBreakdown } from "../services/api";
import type { CategoryBreakdownItem } from "../types/api";

ChartJS.register(ArcElement, Tooltip, Legend);

const now = new Date();
const selectedMonth = ref(now.getMonth() + 1);
const selectedYear = ref(now.getFullYear());
const items = ref<CategoryBreakdownItem[]>([]);

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

const donutData = computed(() => {
  if (items.value.length === 0) return null;
  return {
    labels: items.value.map((item) => item.category),
    datasets: [
      {
        data: items.value.map((item) => Number(item.total)),
        backgroundColor: ["#2e8668", "#49a283", "#78c1a8", "#f59e0b", "#ef4444", "#0ea5e9", "#6366f1"]
      }
    ]
  };
});

function fmt(value?: string | number | null) {
  const parsed = Number(value ?? 0);
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(parsed);
}

async function loadBreakdown() {
  const res = await getCategoryBreakdown(selectedYear.value, selectedMonth.value);
  items.value = res.data?.items ?? [];
}

watch([selectedMonth, selectedYear], loadBreakdown);
onMounted(loadBreakdown);
</script>

<style scoped>
canvas {
  min-height: 300px;
}
</style>
