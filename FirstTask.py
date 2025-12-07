import json
import os

FILE = "attendance.json"


def full_name(s):
    return f"{s['surname']} {s['name']}".strip()


def load_data():
    if not os.path.exists(FILE):
        empty = {"students": [], "disciplines": [], "attendance": {}}
        save_data(empty)
        return empty

    try:
        with open(FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, StopIteration):

        data = {"students": [], "disciplines": [], "attendance": {}}
        save_data(data)
        return data

    if "students" not in data or "disciplines" not in data or "attendance" not in data:
        data = {"students": [], "disciplines": [], "attendance": {}}
        save_data(data)
        return data

    return data


def save_data(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def add_student():
    surname = input("Прізвище: ").strip()
    name = input("Імʼя: ").strip()

    if not surname or not name:
        print("Прізвище та імʼя не можуть бути порожніми.")
        return

    full = f"{surname} {name}"

    data = load_data()

    if full in data["attendance"]:
        print("Студент вже існує.")
        return

    data["students"].append({"surname": surname, "name": name})
    data["attendance"][full] = {d: 0 for d in data["disciplines"]}

    save_data(data)
    print("Студента додано.")


def remove_student():
    surname = input("Прізвище: ").strip()
    name = input("Імʼя: ").strip()
    full = f"{surname} {name}"

    data = load_data()

    found = False

    new_list = []
    for s in data["students"]:
        if full_name(s) == full:
            found = True
        else:
            new_list.append(s)

    if not found:
        print("Студент не знайдений.")
        return

    data["students"] = new_list

    if full in data["attendance"]:
        del data["attendance"][full]

    save_data(data)
    print("Студента видалено.")


def add_discipline():
    disc = input("Назва дисципліни: ").strip()

    if not disc:
        print("Назва дисципліни не може бути порожня.")
        return

    data = load_data()

    if disc in data["disciplines"]:
        print("Дисципліна вже існує.")
        return

    data["disciplines"].append(disc)

    for s in data["students"]:
        full = full_name(s)
        if full not in data["attendance"]:
            data["attendance"][full] = {}
        data["attendance"][full][disc] = 0

    save_data(data)
    print("Дисципліну додано.")


def remove_discipline():
    disc = input("Назва дисципліни: ").strip()
    data = load_data()

    if disc not in data["disciplines"]:
        print("Немає такої дисципліни.")
        return

    data["disciplines"].remove(disc)

    for s in data["students"]:
        full = full_name(s)
        if disc in data["attendance"][full]:
            del data["attendance"][full][disc]

    save_data(data)
    print("Дисципліну видалено.")


def add_absence():
    data = load_data()

    if not data["students"]:
        print("Немає жодного студента.")
        return
    if not data["disciplines"]:
        print("Немає жодної дисципліни.")
        return

    names = input("Студенти (Прізвище Імʼя через кому): ").split(",")
    names = [x.strip() for x in names]

    discipline = input("Дисципліна: ").strip()

    if discipline not in data["disciplines"]:
        print("Такої дисципліни немає.")
        return

    missing = []

    for full in names:
        if full in data["attendance"]:
            data["attendance"][full][discipline] += 1
        else:
            missing.append(full)

    save_data(data)

    print("Пропуски додано.")
    if missing:
        print("⚠ Наступних студентів не знайдено:", ", ".join(missing))


def show_table():
    data = load_data()

    if not data["students"]:
        print("Таблиця порожня.")
        return

    print("\n=== Таблиця відвідування ===")

    header = "Студент".ljust(25)
    for d in data["disciplines"]:
        header += d.ljust(20)
    print(header)

    for s in data["students"]:
        full = full_name(s)
        row = full.ljust(25)
        for d in data["disciplines"]:
            row += str(data["attendance"][full].get(d, 0)).ljust(20)
        print(row)


def show_student():
    full = input("Прізвище та імʼя студента: ").strip()
    data = load_data()

    if full not in data["attendance"]:
        print("Немає такого студента.")
        return

    print(f"\n=== Відвідування: {full} ===")
    for d, m in data["attendance"][full].items():
        print(f"{d}: {m}")


def main():
    while True:
        print("\n--- МЕНЮ ---")
        print("1. Додати студента")
        print("2. Видалити студента")
        print("3. Додати дисципліну")
        print("4. Видалити дисципліну")
        print("5. Внести пропуск")
        print("6. Показати всю таблицю")
        print("7. Показати студента")
        print("0. Вихід")

        choice = input("Вибір: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            remove_student()
        elif choice == "3":
            add_discipline()
        elif choice == "4":
            remove_discipline()
        elif choice == "5":
            add_absence()
        elif choice == "6":
            show_table()
        elif choice == "7":
            show_student()
        elif choice == "0":
            break
        else:
            print("Невірний вибір.")


if __name__ == "__main__":
    main()
