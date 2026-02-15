import axios from "axios";
import type {
  ApiResponse,
  CategoryBreakdown,
  MonthlySummary,
  PaginatedData,
  ProjectionSummary,
  Transaction,
  TransactionCreatePayload,
  WeeklySummary
} from "../types/api";

const api = axios.create({
  baseURL: "/api",
  timeout: 10000
});

export async function getMonthlySummary(year: number, month: number) {
  const { data } = await api.get<ApiResponse<MonthlySummary>>(
    `/v1/transactions/summary/monthly`,
    { params: { year, month } }
  );
  return data;
}

export async function getProjection(year: number, month: number) {
  const { data } = await api.get<ApiResponse<ProjectionSummary>>(
    `/v1/transactions/summary/projection`,
    { params: { year, month } }
  );
  return data;
}

export async function getWeeklySummary() {
  const { data } = await api.get<ApiResponse<WeeklySummary>>(`/v1/transactions/summary/weekly`);
  return data;
}

export async function getCategoryBreakdown(year: number, month: number) {
  const { data } = await api.get<ApiResponse<CategoryBreakdown>>(
    `/v1/transactions/summary/category`,
    { params: { year, month } }
  );
  return data;
}

export async function getTransactions(pageNo = 1, maxPerPage = 10) {
  const { data } = await api.get<ApiResponse<PaginatedData<Transaction>>>(`/v1/transactions/`, {
    params: { page_no: pageNo, max_per_page: maxPerPage }
  });
  return data;
}

export async function createTransaction(payload: TransactionCreatePayload) {
  const { data } = await api.post<ApiResponse<Transaction>>(`/v1/transactions/`, payload);
  return data;
}
