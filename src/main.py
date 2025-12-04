# from datetime import datetime, date

# try:
#     from tracker import ExpenseTracker
#     from models import Expense
#     from storage import load_expenses, save_expenses
# except ModuleNotFoundError:
#     # Allow running as "python -m src.main" by falling back to relative imports
#     from .tracker import ExpenseTracker
#     from .models import Expense
#     from .storage import load_expenses, save_expenses


# DATA_FILE = "data/expenses.csv"


# def parse_date(date_str: str) -> date:
#     if not date_str.strip():
#         # default to today
#         return date.today()
#     return datetime.strptime(date_str, "%Y-%m-%d").date()


# def prompt_expense() -> Expense:
#     category = input("Enter category (e.g., Food, Rent, Travel): ").strip()
#     amount_str = input("Enter amount: ").strip()
#     date_str = input("Enter date (YYYY-MM-DD, leave blank for today): ").strip()
#     description = input("Enter description (optional): ").strip()

#     try:
#         amount = float(amount_str)
#     except ValueError:
#         print("Invalid amount. Please try again.")
#         return prompt_expense()

#     try:
#         d = parse_date(date_str)
#     except ValueError:
#         print("Invalid date. Please use YYYY-MM-DD.")
#         return prompt_expense()

#     return Expense(date=d, category=category, amount=amount, description=description)


# def show_summary(tracker: ExpenseTracker) -> None:
#     print("\n=== Summary ===")
#     print(f"Total expense: ${tracker.total_expense():.2f}")

#     totals_by_cat = tracker.total_by_category()
#     print("\nTotal by category:")
#     for cat, amt in totals_by_cat.items():
#         print(f"  {cat}: ${amt:.2f}")

#     highest, lowest = tracker.highest_and_lowest_category()
#     highest_text = f"{highest[0]} (${highest[1]:.2f})" if highest else "N/A"
#     lowest_text = f"{lowest[0]} (${lowest[1]:.2f})" if lowest else "N/A"
#     print("\nHighest spend category:", highest_text)
#     print("Lowest spend category:", lowest_text)

#     print("\nExpense trend (by date):")
#     trend = tracker.trend_by_date()
#     for d, amt in trend.items():
#         print(f"  {d.isoformat()}: ${amt:.2f}")
#     print()


# def main() -> None:
#     expenses = load_expenses(DATA_FILE)
#     tracker = ExpenseTracker(expenses)

#     while True:
#         print("==== Simple Expense Tracker ====")
#         print("1. Add expense")
#         print("2. View summary")
#         print("3. Save & exit")
#         choice = input("Choose an option (1-3): ").strip()

#         if choice == "1":
#             expense = prompt_expense()
#             tracker.add_expense(expense)
#             print("Expense added.\n")

#         elif choice == "2":
#             show_summary(tracker)

#         elif choice == "3":
#             save_expenses(DATA_FILE, tracker.expenses)
#             print("Expenses saved. Goodbye!")
#             break

#         else:
#             print("Invalid choice, please try again.\n")


# if __name__ == "__main__":
#     main()
