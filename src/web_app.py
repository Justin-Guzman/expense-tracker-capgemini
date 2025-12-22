from datetime import datetime, date
from pathlib import Path

from flask import Flask, abort, redirect, render_template, request, url_for

try:
    from tracker import ExpenseTracker
    from models import Expense
    from storage import load_expenses, save_expenses
except ModuleNotFoundError:
    from .tracker import ExpenseTracker
    from .models import Expense
    from .storage import load_expenses, save_expenses


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "expenses.csv"
CATEGORIES = [
    "Food",
    "Housing",
    "Travel",
    "Entertainment",
    "Utilities",
    "Health",
    "Transportation",
    "Other",
]

app = Flask(__name__)


def load_tracker() -> ExpenseTracker:
    expenses = load_expenses(str(DATA_FILE))
    return ExpenseTracker(expenses)


def parse_date(date_str: str) -> date:
    if not date_str.strip():
        return date.today()
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def process_expense_form(form_data: dict[str, str]):
    values = {
        "category": form_data.get("category", "").strip(),
        "amount": form_data.get("amount", "").strip(),
        "date": form_data.get("date", "").strip(),
        "description": form_data.get("description", "").strip(),
    }

    error = None
    try:
        amount_value = float(values["amount"])
        if amount_value <= 0:
            raise ValueError
    except ValueError:
        amount_value = None
        error = error or "Amount must be a positive number."

    if not values["category"]:
        error = error or "Category is required."
    elif values["category"] not in CATEGORIES:
        error = error or "Please choose a category from the list."

    try:
        date_value = parse_date(values["date"])
        if date_value > date.today():
            raise ValueError
    except ValueError:
        date_value = None
        error = error or "Date cannot be in the future. Use today or earlier."

    if error:
        return values, None, error

    return values, {
        "category": values["category"],
        "amount": amount_value,
        "date": date_value,
        "description": values["description"],
    }, None


@app.route("/", methods=["GET", "POST"])
def index():
    tracker = load_tracker()
    error = None
    message = None

    if request.method == "POST":
        form_defaults, parsed_data, error = process_expense_form(request.form)
        if not error and parsed_data:
            expense = Expense(
                date=parsed_data["date"],
                category=parsed_data["category"],
                amount=parsed_data["amount"],
                description=parsed_data["description"],
            )
            tracker.add_expense(expense)
            save_expenses(str(DATA_FILE), tracker.expenses)
            return redirect(url_for("index", status="added"))
    else:
        form_defaults = {
            "category": CATEGORIES[0],
            "amount": "",
            "date": date.today().isoformat(),
            "description": "",
        }

    status = request.args.get("status")
    if not error:
        if status == "added":
            message = "Expense added successfully."
        elif status == "edited":
            message = "Expense updated successfully."
        elif status == "deleted":
            message = "Expense deleted."
        elif status == "missing":
            error = "Expense could not be found."

    totals_by_cat = tracker.total_by_category()
    highest, lowest = tracker.highest_and_lowest_category()
    trend = [(d.isoformat(), amt) for d, amt in tracker.trend_by_date().items()]
    monthly_totals = tracker.total_by_month()
    expenses = sorted(tracker.expenses, key=lambda e: e.date, reverse=True)

    return render_template(
        "index.html",
        form_data=form_defaults,
        error=error,
        message=message,
        total=tracker.total_expense(),
        totals_by_cat=totals_by_cat,
        trend=trend,
        highest=highest,
        lowest=lowest,
        expenses=expenses,
        categories=CATEGORIES,
        monthly_totals=monthly_totals,
    )


@app.route("/expense/<expense_id>/edit", methods=["GET", "POST"])
def edit_expense(expense_id: str):
    tracker = load_tracker()
    expense = tracker.get_expense(expense_id)
    if not expense:
        abort(404)

    error = None
    if request.method == "POST":
        form_values, parsed_data, error = process_expense_form(request.form)
        if not error and parsed_data:
            tracker.update_expense(
                expense_id,
                date=parsed_data["date"],
                category=parsed_data["category"],
                amount=parsed_data["amount"],
                description=parsed_data["description"],
            )
            save_expenses(str(DATA_FILE), tracker.expenses)
            return redirect(url_for("index", status="edited"))
    else:
        form_values = {
            "category": expense.category,
            "amount": f"{expense.amount:.2f}",
            "date": expense.date.isoformat(),
            "description": expense.description,
        }

    return render_template(
        "edit.html",
        form_data=form_values,
        error=error,
        expense=expense,
        categories=CATEGORIES,
    )


@app.route("/expense/<expense_id>/delete", methods=["POST"])
def delete_expense(expense_id: str):
    tracker = load_tracker()
    status = "deleted" if tracker.delete_expense(expense_id) else "missing"
    if status == "deleted":
        save_expenses(str(DATA_FILE), tracker.expenses)
    return redirect(url_for("index", status=status))


if __name__ == "__main__":
    app.run(debug=True)
