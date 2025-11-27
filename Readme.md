# Simple Expense Tracker

## Overview
A command-line application to track daily expenses by category and date.
It computes:
- Total expense
- Total expense by category
- Expense trend over time (by date)
- Highest and lowest spend categories

## Tech Stack
- Python 3.x
- Standard library only (csv, datetime, unittest)

## Project Structure
- `src/models.py` – Expense data model
- `src/tracker.py` – Core business logic (aggregations, trends)
- `src/storage.py` – CSV load/save utilities
- `src/main.py` – Command-line interface
- `data/expenses_seed.csv` – Sample/seed data
- `tests/test_tracker.py` – Unit tests

## How to Run

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt  # optional if you add dependencies

python -m src.main
