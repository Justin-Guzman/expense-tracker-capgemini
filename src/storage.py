import csv
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Iterable, List
from uuid import uuid4

from .models import Expense


DATE_FORMAT = "%Y-%m-%d"


def _db_path_from_csv(csv_path: str) -> Path:
    return Path(csv_path).with_suffix(".db")


def _init_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id TEXT PRIMARY KEY,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            amount REAL NOT NULL
        )
        """
    )
    conn.commit()


def _row_to_expense(row: sqlite3.Row) -> Expense:
    expense_date = datetime.strptime(row["date"], DATE_FORMAT).date()
    return Expense(
        date=expense_date,
        category=row["category"],
        amount=float(row["amount"]),
        description=row["description"] or "",
        id=row["id"],
    )


def _load_from_csv(csv_path: Path) -> List[Expense]:
    if not csv_path.exists():
        return []

    expenses: List[Expense] = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
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
                continue
    return expenses


def _write_csv(csv_path: Path, expenses: Iterable[Expense]) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as f:
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


def load_expenses(path: str) -> List[Expense]:
    csv_path = Path(path)
    db_path = _db_path_from_csv(path)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        _init_db(conn)
        count = conn.execute("SELECT COUNT(*) FROM expenses").fetchone()[0]
        if count == 0:
            seed_expenses = _load_from_csv(csv_path)
            if seed_expenses:
                conn.executemany(
                    """
                    INSERT OR REPLACE INTO expenses (id, date, category, description, amount)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    [
                        (
                            e.id,
                            e.date.strftime(DATE_FORMAT),
                            e.category,
                            e.description,
                            e.amount,
                        )
                        for e in seed_expenses
                    ],
                )
                conn.commit()
        rows = conn.execute(
            "SELECT id, date, category, description, amount FROM expenses ORDER BY date DESC"
        ).fetchall()
    finally:
        conn.close()

    return [_row_to_expense(row) for row in rows]


def save_expenses(path: str, expenses: List[Expense]) -> None:
    csv_path = Path(path)
    db_path = _db_path_from_csv(path)

    conn = sqlite3.connect(db_path)
    try:
        _init_db(conn)
        conn.execute("DELETE FROM expenses")
        conn.executemany(
            """
            INSERT INTO expenses (id, date, category, description, amount)
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                (
                    e.id,
                    e.date.strftime(DATE_FORMAT),
                    e.category,
                    e.description,
                    e.amount,
                )
                for e in expenses
            ],
        )
        conn.commit()
    finally:
        conn.close()

    _write_csv(csv_path, expenses)
