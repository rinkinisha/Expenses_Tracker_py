
from fastapi.testclient import TestClient

from app.main import app
import app.utils as utils


client = TestClient(app)


def setup_test_csv(monkeypatch, tmp_path):
    test_data_dir = tmp_path / "data"
    test_csv_file = test_data_dir / "expenses.csv"

    monkeypatch.setattr(utils, "DATA_DIR", test_data_dir)
    monkeypatch.setattr(utils, "CSV_FILE", test_csv_file)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Expense Tracker API is running"
    }


def test_create_expense(monkeypatch, tmp_path):
    setup_test_csv(monkeypatch, tmp_path)

    payload = {
        "title": "Lunch",
        "amount": 250,
        "category": "Food",
        "date": "2026-10-19",
        "notes": "Office lunch",
    }

    response = client.post("/expenses", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Lunch"
    assert data["amount"] == 250


def test_get_all_expenses(monkeypatch, tmp_path):
    setup_test_csv(monkeypatch, tmp_path)

    payload = {
        "title": "Bus Ticket",
        "amount": 80,
        "category": "Travel",
        "date": "2026-10-19",
        "notes": "Campus travel",
    }

    client.post("/expenses", json=payload)

    response = client.get("/expenses")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Bus Ticket"


def test_invalid_expense():
    payload = {
        "title": "Invalid Expense",
        "amount": -100,
        "category": "Food",
        "date": "2026-10-19",
        "notes": None,
    }

    response = client.post("/expenses", json=payload)

    assert response.status_code == 422


def test_expense_not_found(monkeypatch, tmp_path):
    setup_test_csv(monkeypatch, tmp_path)

    response = client.get("/expenses/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"


def test_filter_by_category(monkeypatch, tmp_path):
    setup_test_csv(monkeypatch, tmp_path)

    client.post("/expenses", json={
        "title": "Lunch",
        "amount": 250,
        "category": "Food",
        "date": "2026-10-19",
        "notes": None,
    })

    client.post("/expenses", json={
        "title": "Bus",
        "amount": 80,
        "category": "Travel",
        "date": "2026-10-19",
        "notes": None,
    })

    response = client.get("/expenses?category=food")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Lunch"


def test_sort_by_amount_desc(monkeypatch, tmp_path):
    setup_test_csv(monkeypatch, tmp_path)

    for title, amount in [("Lunch", 250), ("Bus", 80)]:
        client.post("/expenses", json={
            "title": title,
            "amount": amount,
            "category": "Food",
            "date": "2026-10-19",
            "notes": None,
        })

    response = client.get(
        "/expenses?sort_by=amount&order=desc"
    )

    amounts = [item["amount"] for item in response.json()]

    assert amounts == [250, 80]


def test_pagination(monkeypatch, tmp_path):
    setup_test_csv(monkeypatch, tmp_path)

    for title, amount in [("A", 10), ("B", 20), ("C", 30)]:
        client.post("/expenses", json={
            "title": title,
            "amount": amount,
            "category": "Food",
            "date": "2026-10-19",
            "notes": None,
        })

    response = client.get(
        "/expenses?sort_by=title&order=asc&limit=2&offset=1"
    )

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert [item["title"] for item in response.json()] == ["B", "C"]



def test_export_expenses(monkeypatch, tmp_path):

    setup_test_csv(monkeypatch, tmp_path)

    client.post("/expenses", json={
        "title": "Lunch",
        "amount": 250,
        "category": "Food",
        "date": "2026-10-19",
        "notes": "Office lunch",
    })

    response = client.get("/expenses/export")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert 'filename="expenses.csv"' in response.headers["content-disposition"]
    assert "Lunch" in response.text
    assert "250" in response.text



def test_monthly_summary(monkeypatch, tmp_path):
    setup_test_csv(monkeypatch, tmp_path)

    client.post("/expenses", json={
        "title": "Lunch",
        "amount": 250,
        "category": "Food",
        "date": "2026-10-19",
        "notes": None,
    })

    client.post("/expenses", json={
        "title": "Bus",
        "amount": 80,
        "category": "Travel",
        "date": "2026-10-19",
        "notes": None,
    })

    response = client.get(
        "/analytics/monthly?year=2026&month=10"
    )

    assert response.status_code == 200
    assert response.json()["total_expense"] == 330
    assert response.json()["expense_count"] == 2


def test_category_summary(monkeypatch, tmp_path):
    setup_test_csv(monkeypatch, tmp_path)

    client.post("/expenses", json={
        "title": "Lunch",
        "amount": 250,
        "category": "Food",
        "date": "2026-10-19",
        "notes": None,
    })

    client.post("/expenses", json={
        "title": "Bus",
        "amount": 80,
        "category": "Travel",
        "date": "2026-10-19",
        "notes": None,
    })

    response = client.get("/analytics/categories")

    assert response.status_code == 200

    totals = {
        item["category"]: item["total_expense"]
        for item in response.json()
    }

    assert totals["Food"] == 250
    assert totals["Travel"] == 80


def test_highest_expense(monkeypatch, tmp_path):
    setup_test_csv(monkeypatch, tmp_path)

    client.post("/expenses", json={
        "title": "Lunch",
        "amount": 250,
        "category": "Food",
        "date": "2026-10-19",
        "notes": None,
    })

    client.post("/expenses", json={
        "title": "Bus",
        "amount": 80,
        "category": "Travel",
        "date": "2026-10-19",
        "notes": None,
    })

    response = client.get("/analytics/highest")

    assert response.status_code == 200
    assert response.json()["title"] == "Lunch"
    assert response.json()["amount"] == 250


def test_expense_statistics(monkeypatch, tmp_path):
    setup_test_csv(monkeypatch, tmp_path)

    client.post("/expenses", json={
        "title": "Lunch",
        "amount": 250,
        "category": "Food",
        "date": "2026-10-19",
        "notes": None,
    })

    client.post("/expenses", json={
        "title": "Bus",
        "amount": 80,
        "category": "Travel",
        "date": "2026-10-19",
        "notes": None,
    })

    response = client.get("/analytics/statistics")

    assert response.status_code == 200

    data = response.json()

    assert data["expense_count"] == 2
    assert data["total_expense"] == 330
    assert data["average_expense"] == 165
    assert data["highest_amount"] == 250
