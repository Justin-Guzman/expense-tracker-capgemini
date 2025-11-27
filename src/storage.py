import csv
from datetime import datetime
from pathlib import Path
from typing import List
from uuid import uuid4

from .models import Expense


DATE_FORMAT = "%Y-%m-%d"


def load_expenses(path: str) -> List[Expense]:
    file_path = Path(path)
    if not file_path.exists():
        return []

    expenses: List[Expense] = []
    with file_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Expected columns: date, category, amount
            try:
                expense_date = datetime.strptime(row["date"], DATE_FORMAT).date()
                category = row["category"]
                amount = float(row["amount"])
                description = row.get("description", "")
                expense_id = row.get("id") or uuid4().hex
                expenses.append(
                    Expense(
                        date=expense_date,
                        category=category,
                        amount=amount,
                        description=description,
                        id=expense_id,
                    )
                )
            except (KeyError, ValueError):
                # In a real app, we might log this; for now, skip bad rows
                continue
    return expenses


def save_expenses(path: str, expenses: List[Expense]) -> None:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["id", "date", "category", "description", "amount"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for e in expenses:
            writer.writerow(
                {
                    "id": e.id,
                    "date": e.date.strftime(DATE_FORMAT),
                    "category": e.category,
                    "description": e.description,
                    "amount": f"{e.amount:.2f}",
                }
            )
