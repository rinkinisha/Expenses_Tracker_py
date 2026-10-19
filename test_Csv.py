
from app.models import ExpenseCreate
from app.services import (
    create_expense,
    get_all_expenses,
    get_expense_by_id,
    update_expense,
    delete_expense,
)

new_expense = ExpenseCreate(
    title="Bus Ticket",
    amount=80,
    category="Travel",
    date="2026-10-18",
    notes="Campus travel",
)

created = create_expense(new_expense)
print("Created:", created)

print("All expenses:", get_all_expenses())
print("Find expense:", get_expense_by_id(created["id"]))

updated_data = ExpenseCreate(
    title="Bus Ticket",
    amount=100,
    category="Travel",
    date="2026-10-18",
    notes="Updated fare",
)

print(
    "Updated:",
    update_expense(created["id"], updated_data)
)

print("Deleted:", delete_expense(created["id"]))
print("Final expenses:", get_all_expenses())
