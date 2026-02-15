import { createRouter, createWebHistory } from "vue-router";
import DashboardView from "../views/DashboardView.vue";
import TransactionsView from "../views/TransactionsView.vue";
import ExpenditureView from "../views/ExpenditureView.vue";

const routes = [
  { path: "/", redirect: "/dashboard" },
  { path: "/dashboard", component: DashboardView },
  { path: "/transactions", component: TransactionsView },
  { path: "/expenditure", component: ExpenditureView }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
