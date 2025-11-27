import unittest
from datetime import date

from src.models import Expense
from src.tracker import ExpenseTracker


class ExpenseTrackerTests(unittest.TestCase):
    def setUp(self):
        self.tracker = ExpenseTracker(
            [
                Expense(date(2025, 11, 1), "Food", 10.0),
                Expense(date(2025, 11, 1), "Rent", 500.0),
                Expense(date(2025, 11, 2), "Food", 5.0),
            ]
        )

    def test_total_expense(self):
        self.assertAlmostEqual(self.tracker.total_expense(), 515.0)

    def test_total_by_category(self):
        totals = self.tracker.total_by_category()
        self.assertAlmostEqual(totals["Food"], 15.0)
        self.assertAlmostEqual(totals["Rent"], 500.0)

    def test_highest_and_lowest_category(self):
        highest, lowest = self.tracker.highest_and_lowest_category()
        self.assertEqual(highest, ("Rent", 500.0))
        self.assertEqual(lowest, ("Food", 15.0))

    def test_trend_by_date(self):
        trend = self.tracker.trend_by_date()
        self.assertEqual(len(trend), 2)
        self.assertAlmostEqual(trend[date(2025, 11, 1)], 510.0)
        self.assertAlmostEqual(trend[date(2025, 11, 2)], 5.0)

    def test_total_by_month(self):
        totals = self.tracker.total_by_month()
        self.assertIn("2025-11", totals)
        self.assertAlmostEqual(totals["2025-11"], 515.0)


if __name__ == "__main__":
    unittest.main()
