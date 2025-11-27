from dataclasses import dataclass
from datetime import date


@dataclass
class Expense:
    date: date
    category: str
    amount: float