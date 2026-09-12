from dataclasses import dataclass

@dataclass
class Expense:
    id: int
    amount: int
    category: str
    description: str
    date: str