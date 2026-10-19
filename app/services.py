
from app.models import ExpenseCreate
from app.utils import read_expenses, write_expenses


def _convert_row(row):
    """Convert CSV string values into appropriate Python types."""
    return {
        "id": int(row["id"]),
        "title": row["title"],
        "amount": float(row["amount"]),
        "category": row["category"],
        "date": row["date"],
        "notes": row["notes"] or None,
    }


def get_all_expenses():
    rows = read_expenses()
    return [_convert_row(row) for row in rows]


def get_expense_by_id(expense_id: int):
    expenses = get_all_expenses()

    for expense in expenses:
        if expense["id"] == expense_id:
            return expense

    return None


def create_expense(expense: ExpenseCreate):
    expenses = get_all_expenses()

    if expenses:
        new_id = max(item["id"] for item in expenses) + 1
    else:
        new_id = 1

    new_expense = {
        "id": new_id,
        "title": expense.title,
        "amount": expense.amount,
        "category": expense.category,
        "date": expense.date.isoformat(),
        "notes": expense.notes,
    }

    expenses.append(new_expense)
    write_expenses(expenses)

    return new_expense


def update_expense(expense_id: int, updated_data: ExpenseCreate):
    expenses = get_all_expenses()

    for index, expense in enumerate(expenses):
        if expense["id"] == expense_id:
            expenses[index] = {
                "id": expense_id,
                "title": updated_data.title,
                "amount": updated_data.amount,
                "category": updated_data.category,
                "date": updated_data.date.isoformat(),
                "notes": updated_data.notes,
            }

            write_expenses(expenses)
            return expenses[index]

    return None


def delete_expense(expense_id: int):
    expenses = get_all_expenses()

    remaining_expenses = [
        expense
        for expense in expenses
        if expense["id"] != expense_id
    ]

    if len(remaining_expenses) == len(expenses):
        return False

    write_expenses(remaining_expenses)
    return True
