
import csv

from app.config import CSV_COLUMNS, CSV_FILE, DATA_DIR


def ensure_csv_exists():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not CSV_FILE.exists():
        with CSV_FILE.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
            writer.writeheader()


def read_expenses():
    ensure_csv_exists()

    with CSV_FILE.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def write_expenses(expenses):
    ensure_csv_exists()

    with CSV_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(expenses)
