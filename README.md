
# Expense Tracker API

A REST API built with Python and FastAPI to manage expenses,
analyze spending patterns, and export expenses to CSV.

## Features

- Create, read, update, and delete expenses
- Validate request data using Pydantic
- Store expenses in a CSV file
- Search and filter expenses
- Sort and paginate results
- Monthly and category-wise analytics
- Highest expense and spending statistics
- Export expenses as a CSV file
- Automated API tests using pytest

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Pydantic
- Pandas
- NumPy
- CSV
- pytest
- HTTPX

## Setup

Clone the repository and navigate into the project:

```bash
git clone <your-repository-url>
cd expense_tracker_api
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the development server:

```bash
uvicorn app.main:app --reload
```

## API Documentation

Open Swagger UI:

http://127.0.0.1:8000/docs

## Run Tests

```bash
python -m pytest -v
```

## Storage

Expenses are stored in `data/expenses.csv`.

## License

Add your chosen license here.
