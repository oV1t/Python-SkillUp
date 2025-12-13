import csv
import os
import re
from typing import List, Dict

FILE = "grades.csv"

# ------------------ ECTS ------------------

def ects_letter(score: float) -> str:
    if score >= 90:
        return "A"
    if score >= 82:
        return "B"
    if score >= 74:
        return "C"
    if score >= 64:
        return "D"
    if score >= 60:
        return "E"
    if score >= 35:
        return "FX"
    return "F"

# ------------------ Validation ------------------

def validate_date(date: str) -> bool:
    return bool(re.match(r"^\d{4}-(0[1-9]|1[0-2])-([0][1-9]|[12][0-9]|3[01])$", date))

def validate_score(score: str) -> bool:
    try:
        value = float(score)
        return 0 <= value <= 100
    except ValueError:
        return False

# ------------------ File I/O ------------------

def load_grades() -> List[Dict]:
    if not os.path.exists(FILE):
        return []

    with open(FILE, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        return [
            {"subject": r[0], "date": r[1], "score": float(r[2])}
            for r in reader if len(r) == 3
        ]

def save_grade(record: Dict):
    with open(FILE, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow([record["subject"], record["date"], record["score"]])

# ------------------ Actions ------------------

def add_grade():
    subject = input("Дисципліна: ").strip()
    date = input("Дата (YYYY-MM-DD): ").strip()
    score = input("Бал (0–100): ").strip()

    if not subject or not validate_date(date) or not validate_score(score):
        print("❌ Невірні дані")
        return

    record = {
        "subject": subject,
        "date": date,
        "score": float(score)
    }

    save_grade(record)
    print("✅ Оцінку додано")

def show_all():
    grades = load_grades()
    if not grades:
        print("Записів немає")
        return

    for g in grades:
        print(f"{g['subject']} — {g['date']} — {g['score']} — {ects_letter(g['score'])}")

def average_by_subject():
    subject = input("Введіть дисципліну: ").strip()
    grades = [g["score"] for g in load_grades() if g["subject"] == subject]

    if not grades:
        print("Записів не знайдено")
        return

    avg = sum(grades) / len(grades)
    print(f"Середній бал: {avg:.2f} ({ects_letter(avg)})")

def average_all():
    grades = [g["score"] for g in load_grades()]
    if not grades:
        print("Записів немає")
        return

    avg = sum(grades) / len(grades)
    print(f"Загальний середній бал: {avg:.2f} ({ects_letter(avg)})")

# ------------------ Menu ------------------

def menu():
    actions = {
        "1": add_grade,
        "2": show_all,
        "3": average_by_subject,
        "4": average_all,
        "0": exit
    }

    while True:
        print("""
1 — Додати оцінку
2 — Переглянути всі оцінки
3 — Середній бал по дисципліні
4 — Загальний середній бал
0 — Вийти
""")
        choice = input("Ваш вибір: ").strip()
        action = actions.get(choice)

        if action:
            action()
        else:
            print("❌ Невірний пункт")

# ------------------ Start ------------------

if __name__ == "__main__":
    menu()
