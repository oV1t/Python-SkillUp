import json
import os
import re

FILE = "budget.json"

# ------------------ Валідація ------------------

def validate_month_format(month: str) -> bool:
    pattern = r"^\d{4}-(0[1-9]|1[0-2])$"
    return bool(re.match(pattern, month))


# ------------------ Форматування запису ------------------

def format_budget_record(record: dict) -> str:
    return f"{record['month']:10}|{record['income']:7}|{record['expenses']:9}"


# ------------------ Робота з файлом ------------------

def load_budget_data():
    if not os.path.exists(FILE):
        empty = {"records": []}
        save_budget_data(empty)
        return empty

    try:
        with open(FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, StopIteration):
        data = {"records": []}
        save_budget_data(data)
        return data

    if "records" not in data:
        data = {"records": []}
        save_budget_data(data)
        return data

    return data


def save_budget_data(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# ------------------ Додавання запису ------------------

def add_budget_record():
    month = input("Місяць (YYYY-MM): ").strip()
    income_input = input("Доходи: ").strip()
    expenses_input = input("Витрати: ").strip()

    if not month or not income_input or not expenses_input:
        print("Місяць, доходи та витрати не можуть бути порожніми.")
        return

    if not validate_month_format(month):
        print("Невірний формат. Приклад: 2025-11.")
        return

    try:
        income = float(income_input)
        expenses = float(expenses_input)
    except ValueError:
        print("Доходи та витрати повинні бути числовими.")
        return

    data = load_budget_data()

    for record in data["records"]:
        if record["month"] == month:
            print("Запис за цей місяць вже існує.")
            return

    data["records"].append({
        "month": month,
        "income": income,
        "expenses": expenses
    })

    save_budget_data(data)
    print("Запис бюджету додано.")


# ------------------ Вивід усієї історії ------------------

def list_budget_records():
    data = load_budget_data()

    if not data["records"]:
        print("Немає записів бюджету.")
        return

    print("МІСЯЦЬ     | ДОХОДИ | ВИТРАТИ | ЗАЛИШОК")
    print("-----------------------------------------------")

    for record in data["records"]:
        balance = record["income"] - record["expenses"]
        print(f"{record['month']:10}|{record['income']:7}|{record['expenses']:7}|{balance:8}")


# ------------------ Максимальні витрати ------------------

def max_expense_record():
    data = load_budget_data()

    if not data["records"]:
        print("Немає записів бюджету.")
        return

    max_record = max(data["records"], key=lambda r: r["expenses"])

    print("Запис з найбільшими витратами:")
    print("МІСЯЦЬ     | ДОХОДИ | ВИТРАТИ")
    print("------------------------------------------")
    print(format_budget_record(max_record))


# ------------------ Головне меню ------------------

def main_menu():
    while True:
        print("\n=== ЖУРНАЛ СТУДЕНТСЬКОГО БЮДЖЕТУ ===")
        print("1 — Додати новий місяць")
        print("2 — Переглянути історію бюджету")
        print("3 — Місяць з найбільшими витратами")
        print("0 — Вийти")
        choice = input("Ваш вибір: ").strip()

        if choice == "1":
            add_budget_record()
        elif choice == "2":
            list_budget_records()
        elif choice == "3":
            max_expense_record()
        elif choice == "0":
            print("Вихід...")
            break
        else:
            print("Невірний вибір. Спробуйте ще.")

# Запуск програми
main_menu()
