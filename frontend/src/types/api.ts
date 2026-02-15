export type ApiResponse<T> = {
  data: T;
  success: boolean;
  message?: string | null;
};

export type TransactionType = "income" | "expense";

export type Transaction = {
  id: number;
  amount: string;
  type: TransactionType;
  category: string;
  description?: string | null;
  transaction_date: string;
  created_at: string;
  updated_at: string;
};

export type PaginatedData<T> = {
  data: T[];
  total: number;
  page_no: number;
  max_per_page: number;
  current_count: number;
};

export type MonthlySummary = {
  total_expense: string;
  total_income: string;
  net_savings: string;
};

export type WeeklySummary = {
  week_start: string;
  week_end: string;
  total_expense: string;
  total_income: string;
  net_savings: string;
};

export type CategoryBreakdownItem = {
  category: string;
  total: string;
};

export type CategoryBreakdown = {
  year: number;
  month: number;
  total_expense: string;
  items: CategoryBreakdownItem[];
};

export type ProjectionSummary = {
  spent_so_far: string;
  projected_month_end: string;
  days_passed: number;
  total_days: number;
};

export type TransactionCreatePayload = {
  amount: number;
  type: TransactionType;
  category: string;
  description?: string;
  transaction_date?: string;
};
