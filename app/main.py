
from fastapi import FastAPI, HTTPException, status
from fastapi import Query

import csv
from io import StringIO

from fastapi.responses import StreamingResponse


from app.analytics import (
    monthly_summary,
    category_summary,
    highest_expense,
    expense_statistics,
)

from app.models import ExpenseCreate, ExpenseResponse
from app.services import (
    create_expense,
    get_all_expenses,
    get_expense_by_id,
    update_expense,
    delete_expense,
)

app = FastAPI(
    title="Expense Tracker API",
    description="API for managing and analyzing expenses",
    version="1.0.0",
)


@app.get("/")
def home():
    return {"message": "Expense Tracker API is running"}


@app.post(
    "/expenses",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_expense(expense: ExpenseCreate):
    return create_expense(expense)



@app.get("/expenses", response_model=list[ExpenseResponse])
def list_expenses(
    category: str | None = None,
    search: str | None = None,
    sort_by: str = Query(
        default="date",
        pattern="^(date|amount|title)$",
    ),
    order: str = Query(
        default="asc",
        pattern="^(asc|desc)$",
    ),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    expenses = get_all_expenses()

    # 1. Filter by category
    if category:
        expenses = [
            expense
            for expense in expenses
            if expense["category"].casefold() == category.casefold()
        ]

    # 2. Search by title
    if search:
        keyword = search.casefold()
        expenses = [
            expense
            for expense in expenses
            if keyword in expense["title"].casefold()
        ]

    # 3. Sort results
    if sort_by == "title":
        expenses.sort(
            key=lambda expense: expense["title"].casefold(),
            reverse=(order == "desc"),
        )
    else:
        expenses.sort(
            key=lambda expense: expense[sort_by],
            reverse=(order == "desc"),
        )

    # 4. Apply pagination
    return expenses[offset:offset + limit]


@app.get("/expenses/export")
def export_expenses():
    expenses = get_all_expenses()

    output = StringIO()

    fieldnames = [
        "id",
        "title",
        "amount",
        "category",
        "date",
        "notes",
    ]

    writer = csv.DictWriter(
        output,
        fieldnames=fieldnames,
    )

    writer.writeheader()
    writer.writerows(expenses)

    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": 'attachment; filename="expenses.csv"'
        },
    )


@app.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int):
    expense = get_expense_by_id(expense_id)

    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    return expense


@app.put("/expenses/{expense_id}", response_model=ExpenseResponse)
def edit_expense(expense_id: int, updated_data: ExpenseCreate):
    expense = update_expense(expense_id, updated_data)

    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    return expense


@app.delete("/expenses/{expense_id}")
def remove_expense(expense_id: int):
    deleted = delete_expense(expense_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    return {"message": "Expense deleted successfully"}


@app.get("/analytics/monthly")
def get_monthly_summary(
    year: int,
    month: int = Query(ge=1, le=12),
):
    return monthly_summary(year, month)


@app.get("/analytics/categories")
def get_category_summary():
    return category_summary()


@app.get("/analytics/highest")
def get_highest_expense():
    expense = highest_expense()

    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No expenses found",
        )

    return expense


@app.get("/analytics/statistics")
def get_expense_statistics():
    return expense_statistics()


