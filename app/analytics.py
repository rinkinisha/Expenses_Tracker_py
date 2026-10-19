
import pandas as pd
import numpy as np

from app.services import get_all_expenses


def _get_dataframe():
    expenses = get_all_expenses()

    columns = [
        "id",
        "title",
        "amount",
        "category",
        "date",
        "notes",
    ]

    df = pd.DataFrame(expenses, columns=columns)

    if not df.empty:
        df["amount"] = pd.to_numeric(df["amount"])
        df["date"] = pd.to_datetime(df["date"])

    return df


def monthly_summary(year: int, month: int):
    df = _get_dataframe()

    if df.empty:
        return {
            "year": year,
            "month": month,
            "total_expense": 0,
            "expense_count": 0,
        }

    monthly_df = df[
        (df["date"].dt.year == year)
        & (df["date"].dt.month == month)
    ]

    return {
        "year": year,
        "month": month,
        "total_expense": round(float(monthly_df["amount"].sum()), 2),
        "expense_count": len(monthly_df),
    }


def category_summary():
    df = _get_dataframe()

    if df.empty:
        return []

    summary = (
        df.groupby("category")["amount"]
        .sum()
        .reset_index()
    )

    summary["total_expense"] = summary["amount"]
    summary = summary.drop(columns=["amount"])

    return summary.to_dict(orient="records")


def highest_expense():
    df = _get_dataframe()

    if df.empty:
        return None

    index = df["amount"].idxmax()
    expense = df.loc[index].to_dict()

    expense["id"] = int(expense["id"])
    expense["amount"] = float(expense["amount"])
    expense["date"] = expense["date"].date().isoformat()

    return expense


def expense_statistics():
    df = _get_dataframe()

    if df.empty:
        return {
            "expense_count": 0,
            "total_expense": 0,
            "average_expense": 0,
            "highest_amount": 0,
        }

    amounts = df["amount"].to_numpy()

    return {
        "expense_count": int(len(amounts)),
        "total_expense": round(float(np.sum(amounts)), 2),
        "average_expense": round(float(np.mean(amounts)), 2),
        "highest_amount": round(float(np.max(amounts)), 2),
    }
