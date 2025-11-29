# Simple Expense Tracker

## Overview
A lightweight web application for tracking daily expenses with a friendly UI. Users can:
- Add expenses with category (from a dropdown), amount, date, and description.
- View running totals, highest/lowest spend categories (aggregated), and per-category totals.
- See both a daily trend table and a monthly line chart powered by Chart.js.
- Edit or delete existing entries, with all data persisted to a CSV file.


## Tech Stack
- Python 3.x
- Flask for the web server/templates
- Chart.js (via CDN) for the monthly trend visualization
- CSV files for persistence (no database required)

## Project Structure
- `src/models.py` – Expense data model (with UUID IDs and descriptions)
- `src/tracker.py` – Core business logic (aggregations, trends, CRUD helpers)
- `src/storage.py` – CSV load/save utilities
- `src/web_app.py` – Flask app entry point
- `src/templates/` – HTML templates (main dashboard + edit form)
- `src/main.py` – Legacy CLI interface (optional)
- `data/expenses.csv` – Persisted expense data
- `tests/` – Unit tests for tracker logic

## Getting Started

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Run the Web App

```bash
python -m flask --app src.web_app run --debug
```

Visit http://127.0.0.1:5000/ to add, edit, and analyze expenses. Data is saved to `data/expenses.csv`, so it persists between sessions.

## Live Demo

- https://expense-tracker-capgemini.onrender.com/ (hosted on Render; note that the free tier may spin down when idle, so the first request can take a few seconds)
