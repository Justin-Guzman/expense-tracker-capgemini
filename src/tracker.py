from collections import defaultdict
from datetime import date
from typing import Dict, List, Tuple

from .models import Expense


class ExpenseTracker:
    def __init__(self, expenses: List[Expense] | None = None):
        self.expenses: List[Expense] = expenses or []

    def add_expense(self, expense: Expense) -> None:
        self.expenses.append(expense)

    def total_expense(self) -> float:
        return sum(e.amount for e in self.expenses)

    def total_by_category(self) -> Dict[str, float]:
        totals: Dict[str, float] = defaultdict(float)
        for e in self.expenses:
            totals[e.category] += e.amount
        return dict(totals)

    def highest_and_lowest_category(self) -> Tuple[Tuple[str, float] | None, Tuple[str, float] | None]:
        """
        Returns (highest_category_with_total, lowest_category_with_total).
        Each entry is a tuple of (category_name, total_amount).
        If there are no expenses, returns (None, None).
        """
        totals = self.total_by_category()
        if not totals:
            return None, None

        highest = max(totals.items(), key=lambda kv: kv[1])
        lowest = min(totals.items(), key=lambda kv: kv[1])
        return highest, lowest

    def trend_by_date(self) -> Dict[date, float]:
        """
        Returns a dict of date -> total amount for that date,
        sorted by date when iterated over.
        """
        totals: Dict[date, float] = defaultdict(float)
        for e in self.expenses:
            totals[e.date] += e.amount
        # Return as a normal dict but sorted by date for predictable output
        return dict(sorted(totals.items(), key=lambda kv: kv[0]))

    def get_expense(self, expense_id: str) -> Expense | None:
        for expense in self.expenses:
            if expense.id == expense_id:
                return expense
        return None

    def update_expense(
        self, expense_id: str, *, date: date, category: str, amount: float, description: str
    ) -> bool:
        expense = self.get_expense(expense_id)
        if not expense:
            return False
        expense.date = date
        expense.category = category
        expense.amount = amount
        expense.description = description
        return True

    def delete_expense(self, expense_id: str) -> bool:
        for idx, expense in enumerate(self.expenses):
            if expense.id == expense_id:
                del self.expenses[idx]
                return True
        return False
