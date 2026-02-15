<template>
  <div class="min-h-screen bg-transparent text-slate-800">
    <div class="mx-auto flex max-w-[1400px] gap-4 px-3 py-4 md:px-6">
      <aside class="hidden w-64 shrink-0 rounded-2xl bg-slate-900 p-4 text-slate-100 shadow-lg md:block">
        <h1 class="mb-6 text-lg font-semibold tracking-wide">Expense Tracker</h1>
        <nav class="space-y-2">
          <RouterLink v-for="item in navItems" :key="item.to" :to="item.to" class="block rounded-lg px-3 py-2 text-sm"
            :class="isActive(item.to) ? 'bg-brand-600 text-white' : 'hover:bg-slate-800'">
            {{ item.label }}
          </RouterLink>
        </nav>
      </aside>

      <main class="flex-1 rounded-2xl bg-white/85 p-4 shadow-sm backdrop-blur-sm md:p-6">
        <header class="mb-4 flex items-center justify-between md:hidden">
          <h1 class="text-lg font-semibold">Expense Tracker</h1>
        </header>
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { RouterLink, RouterView, useRoute } from "vue-router";

const route = useRoute();

const navItems = [
  { label: "Dashboard", to: "/dashboard" },
  { label: "Transactions", to: "/transactions" },
  { label: "Expenditure", to: "/expenditure" }
];

const currentPath = computed(() => route.path);

function isActive(path: string) {
  return currentPath.value === path;
}
</script>
