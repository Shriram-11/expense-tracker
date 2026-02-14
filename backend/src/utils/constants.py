from enum import Enum


class TransactionType(str, Enum):
    """Enum for transaction types."""
    INCOME = "income"
    EXPENSE = "expense"


class TransactionCategory(str, Enum):
    """Enum for transaction categories."""
    SALARY = "salary"
    BONUS = "bonus"
    FREELANCE = "freelance"
    INVESTMENT = "investment"
    
    FOOD = "food"
    GROCERIES = "groceries"
    TRANSPORT = "transport"
    UTILITIES = "utilities"
    ENTERTAINMENT = "entertainment"
    HEALTHCARE = "healthcare"
    SHOPPING = "shopping"
    EDUCATION = "education"
    RENT = "rent"
    INSURANCE = "insurance"
    SUBSCRIPTIONS = "subscriptions"
    
    OTHER = "other"
