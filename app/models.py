
from datetime import date

from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    amount: float = Field(gt=0)
    category: str = Field(min_length=1, max_length=50)
    date: date
    notes: str | None = None


class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: float
    category: str
    date: date
    notes: str | None = None
