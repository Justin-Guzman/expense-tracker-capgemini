from dataclasses import dataclass, field
from datetime import date
from uuid import uuid4


@dataclass
class Expense:
    date: date
    category: str
    amount: float
    description: str = ""
    id: str = field(default_factory=lambda: uuid4().hex)
