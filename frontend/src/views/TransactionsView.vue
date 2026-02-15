<template>
  <section class="space-y-5">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h2 class="text-2xl font-semibold">Transactions</h2>
        <p class="text-sm text-slate-500">Track and manage income and expenses.</p>
      </div>
    </div>

    <article class="rounded-xl border border-slate-200 bg-white p-4">
      <h3 class="mb-3 text-sm font-medium text-slate-700">Add Transaction</h3>
      <form class="grid gap-3 md:grid-cols-2 xl:grid-cols-5" @submit.prevent="submitTransaction">
        <input v-model.number="form.amount" type="number" step="0.01" min="0.01" placeholder="Amount"
          class="rounded-lg border border-slate-200 px-3 py-2 text-sm" required />
        <select v-model="form.type" class="rounded-lg border border-slate-200 px-3 py-2 text-sm">
          <option value="expense">Expense</option>
          <option value="income">Income</option>
        </select>
        <input v-model="form.category" type="text" placeholder="Category"
          class="rounded-lg border border-slate-200 px-3 py-2 text-sm" required />
        <input v-model="form.transaction_date" type="date" class="rounded-lg border border-slate-200 px-3 py-2 text-sm" />
        <button type="submit" class="rounded-lg bg-brand-600 px-3 py-2 text-sm font-medium text-white hover:bg-brand-700">
          Add
        </button>
      </form>
      <p v-if="feedback" class="mt-2 text-sm" :class="feedbackType === 'error' ? 'text-rose-600' : 'text-brand-700'">
        {{ feedback }}
      </p>
    </article>

    <article class="rounded-xl border border-slate-200 bg-white p-4">
      <h3 class="mb-3 text-sm font-medium text-slate-700">All Transactions</h3>
      <div class="overflow-x-auto">
        <table class="min-w-full text-sm">
          <thead>
            <tr class="border-b border-slate-200 text-left text-xs uppercase tracking-wide text-slate-500">
              <th class="py-2">Date</th>
              <th class="py-2">Type</th>
              <th class="py-2">Category</th>
              <th class="py-2">Description</th>
              <th class="py-2 text-right">Amount</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="txn in transactions" :key="txn.id" class="border-b border-slate-100">
              <td class="py-2">{{ txn.transaction_date }}</td>
              <td class="py-2 capitalize">{{ txn.type }}</td>
              <td class="py-2 capitalize">{{ txn.category }}</td>
              <td class="py-2">{{ txn.description || "-" }}</td>
              <td class="py-2 text-right font-medium">{{ fmt(txn.amount) }}</td>
            </tr>
            <tr v-if="transactions.length === 0">
              <td colspan="5" class="py-4 text-center text-slate-400">No transactions found.</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="mt-3 flex items-center justify-between text-sm text-slate-600">
        <span>Page {{ pageNo }} of {{ totalPages }}</span>
        <div class="space-x-2">
          <button class="rounded border px-3 py-1 disabled:opacity-40" :disabled="pageNo <= 1" @click="changePage(-1)">Prev</button>
          <button class="rounded border px-3 py-1 disabled:opacity-40" :disabled="pageNo >= totalPages"
            @click="changePage(1)">Next</button>
        </div>
      </div>
    </article>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { createTransaction, getTransactions } from "../services/api";
import type { Transaction, TransactionType } from "../types/api";

const pageNo = ref(1);
const maxPerPage = 10;
const total = ref(0);
const transactions = ref<Transaction[]>([]);
const feedback = ref("");
const feedbackType = ref<"success" | "error">("success");

const form = reactive<{
  amount: number;
  type: TransactionType;
  category: string;
  transaction_date: string;
}>({
  amount: 0,
  type: "expense",
  category: "",
  transaction_date: ""
});

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / maxPerPage)));

function fmt(value?: string | number | null) {
  const parsed = Number(value ?? 0);
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(parsed);
}

async function loadTransactions() {
  const res = await getTransactions(pageNo.value, maxPerPage);
  transactions.value = res.data?.data ?? [];
  total.value = res.data?.total ?? 0;
}

async function submitTransaction() {
  feedback.value = "";
  try {
    const res = await createTransaction({
      amount: form.amount,
      type: form.type,
      category: form.category,
      transaction_date: form.transaction_date || undefined
    });

    if (!res.success) {
      feedbackType.value = "error";
      feedback.value = res.message || "Failed to add transaction.";
      return;
    }

    feedbackType.value = "success";
    feedback.value = res.message || "Transaction added.";
    form.amount = 0;
    form.category = "";
    form.transaction_date = "";
    await loadTransactions();
  } catch {
    feedbackType.value = "error";
    feedback.value = "Failed to add transaction.";
  }
}

async function changePage(delta: number) {
  const next = pageNo.value + delta;
  if (next < 1 || next > totalPages.value) return;
  pageNo.value = next;
  await loadTransactions();
}

onMounted(loadTransactions);
</script>
