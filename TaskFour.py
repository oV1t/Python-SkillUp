import csv
import os
from typing import List, Dict

ORDERS_FILE = "orders.csv"

# ------------------ Меню ------------------

MENU: Dict[int, Dict[str, int]] = {
    1: {"name": "Кава", "price": 40},
    2: {"name": "Булочка", "price": 25},
    3: {"name": "Сендвіч", "price": 60},
}

# ------------------ Робота з файлом ------------------

def load_orders() -> List[Dict]:
    if not os.path.exists(ORDERS_FILE):
        return []

    orders = []
    with open(ORDERS_FILE, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            if len(row) != 4:
                continue
            try:
                order_id = int(row[0])
                date = row[1]
                items_str = row[2]
                total = float(row[3])
            except ValueError:
                continue

            orders.append({
                "id": order_id,
                "date": date,
                "items_str": items_str,
                "total": total,
            })
    return orders


def save_order(order: Dict):
    """Дописує одне замовлення в кінець файлу."""
    with open(ORDERS_FILE, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow([
            order["id"],
            order["date"],
            order["items_str"],
            order["total"],
        ])

# ------------------ Дії користувача ------------------

def show_menu():
    print("Меню:")
    for num, item in MENU.items():
        print(f"{num}. {item['name']} — {item['price']} грн")


def create_order():
    date = input("Введіть дату (рядок, напр. 2025-11-25): ").strip()
    if not date:
        print("❌ Дата не може бути порожньою")
        return

    print("Введіть номери страв через пробіл (напр. 1 2 2):")
    show_menu()
    items_input = input("Номери страв: ").strip()

    if not items_input:
        print("❌ Ви не обрали жодної страви")
        return

    # Парсимо номери
    parts = items_input.replace(",", " ").split()
    dish_numbers: List[int] = []
    for p in parts:
        try:
            n = int(p)
        except ValueError:
            print(f"❌ '{p}' — не число")
            return
        if n not in MENU:
            print(f"❌ Страви з номером {n} немає в меню")
            return
        dish_numbers.append(n)

    # Формуємо список назв і суму
    dish_names: List[str] = []
    total = 0
    for n in dish_numbers:
        dish_names.append(MENU[n]["name"])
        total += MENU[n]["price"]

    items_str = ",".join(dish_names)

    # Визначаємо новий ID
    orders = load_orders()
    if orders:
        max_id = max(o["id"] for o in orders)
    else:
        max_id = 0
    new_id = max_id + 1

    order = {
        "id": new_id,
        "date": date,
        "items_str": items_str,
        "total": total,
    }

    print(f"Ви замовили: {items_str}")
    print(f"Сума: {total} грн")
    save_order(order)
    print(f"✅ Замовлення збережено як ID={new_id}")


def list_orders():
    orders = load_orders()
    if not orders:
        print("Замовлень немає")
        return

    print("Історія замовлень:")
    for o in orders:
        print(f"{o['id']} — {o['date']} — {o['items_str']} — {o['total']} грн")


def total_revenue():
    orders = load_orders()
    if not orders:
        print("Замовлень немає")
        return

    total = sum(o["total"] for o in orders)
    print(f"Загальна виручка: {total} грн")

# ------------------ Меню програми ------------------

def main_menu():
    actions = {
        "1": show_menu,
        "2": create_order,
        "3": list_orders,
        "4": total_revenue,
        "0": exit,
    }

    while True:
        print(
"""
1 — Переглянути меню
2 — Створити замовлення
3 — Переглянути всі замовлення
4 — Показати загальну виручку
0 — Вийти
"""
        )
        choice = input("Ваш вибір: ").strip()
        action = actions.get(choice)
        if action:
            action()
        else:
            print("❌ Невірний пункт меню")

# ------------------ Старт ------------------

if __name__ == "__main__":
    main_menu()
