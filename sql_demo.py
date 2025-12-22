import sqlite3
from pathlib import Path


def print_title(title: str) -> None:
    print(f"\n== {title} ==")


def main() -> None:
    db_path = Path(__file__).resolve().parent / "data" / "expenses.db"
    if not db_path.exists():
        print(f"Database not found at {db_path}. Run the app once to create it.")
        return

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    queries = [
        (
            "Total spend by category",
            """
            SELECT category, SUM(amount) AS total
            FROM expenses
            GROUP BY category
            ORDER BY total DESC;
            """,
        ),
        (
            "Highest spending category",
            """
            SELECT category, SUM(amount) AS total
            FROM expenses
            GROUP BY category
            ORDER BY total DESC
            LIMIT 1;
            """,
        ),
        (
            "Daily spend trend",
            """
            SELECT date, SUM(amount) AS total
            FROM expenses
            GROUP BY date
            ORDER BY date;
            """,
        ),
        (
            "Monthly spend trend (YYYY-MM)",
            """
            SELECT substr(date, 1, 7) AS month, SUM(amount) AS total
            FROM expenses
            GROUP BY month
            ORDER BY month;
            """,
        ),
        (
            "Expenses in a date range (example)",
            """
            SELECT *
            FROM expenses
            WHERE date BETWEEN '2025-01-01' AND '2025-01-31'
            ORDER BY date;
            """,
        ),
        (
            "Average expense amount",
            """
            SELECT AVG(amount) AS avg_amount
            FROM expenses;
            """,
        ),
        (
            "Top 5 largest expenses",
            """
            SELECT *
            FROM expenses
            ORDER BY amount DESC
            LIMIT 5;
            """,
        ),
        (
            "Total spend per category for a specific month (example)",
            """
            SELECT category, SUM(amount) AS total
            FROM expenses
            WHERE substr(date, 1, 7) = '2025-01'
            GROUP BY category
            ORDER BY total DESC;
            """,
        ),
        (
            "Count of expenses per category",
            """
            SELECT category, COUNT(*) AS count
            FROM expenses
            GROUP BY category
            ORDER BY count DESC;
            """,
        ),
        (
            "Categories with total spend > 500",
            """
            SELECT category, SUM(amount) AS total
            FROM expenses
            GROUP BY category
            HAVING total > 500
            ORDER BY total DESC;
            """,
        ),
    ]

    try:
        for title, sql in queries:
            print_title(title)
            rows = conn.execute(sql).fetchall()
            if not rows:
                print("(no rows)")
                continue
            columns = rows[0].keys()
            print(" | ".join(columns))
            for row in rows:
                print(" | ".join(str(row[col]) for col in columns))
    finally:
        conn.close()


if __name__ == "__main__":
    main()
