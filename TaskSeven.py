import os
import json
import base64
import secrets
import string
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


FILE = "vault.dat"

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def create_new_vault():
    password = input("Створіть master password: ").strip()
    salt = os.urandom(16)
    key = derive_key(password, salt)

    data = {"records": []}
    encrypted = Fernet(key).encrypt(json.dumps(data).encode())

    with open(FILE, "wb") as f:
        f.write(salt + encrypted)

    return data, key, salt


def load_vault():
    with open(FILE, "rb") as f:
        content = f.read()

    salt = content[:16]
    encrypted = content[16:]

    password = input("Введіть master password: ").strip()
    key = derive_key(password, salt)

    try:
        decrypted = Fernet(key).decrypt(encrypted)
        data = json.loads(decrypted.decode())
        return data, key, salt
    except InvalidToken:
        print("Невірний master password.")
        exit()


def save_vault(data, key, salt):
    encrypted = Fernet(key).encrypt(json.dumps(data).encode())
    with open(FILE, "wb") as f:
        f.write(salt + encrypted)

def add_record(vault):
    service = input("Service: ").strip()
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if any(r["service"] == service for r in vault["records"]):
        print("Такий сервіс вже існує.")
        return

    vault["records"].append({
        "service": service,
        "username": username,
        "password": password,
        "notes": ""
    })

    print("Додано.")


def show_all(vault):
    if not vault["records"]:
        print("Порожньо.")
        return

    for r in vault["records"]:
        print(f"- {r['service']}")


def show_record(vault):
    service = input("Service: ").strip()

    for r in vault["records"]:
        if r["service"] == service:
            print(f"Username: {r['username']}")
            print("Password: ********")
            confirm = input("Показати пароль? (yes/no): ").strip().lower()
            if confirm == "yes":
                print(f"Password: {r['password']}")
            return

    print("Не знайдено.")


def delete_record(vault):
    service = input("Service: ").strip()

    for r in vault["records"]:
        if r["service"] == service:
            vault["records"].remove(r)
            print("Видалено.")
            return

    print("Не знайдено.")


def update_record(vault):
    service = input("Service: ").strip()

    for r in vault["records"]:
        if r["service"] == service:
            r["username"] = input("Новий username: ").strip()
            r["password"] = input("Новий password: ").strip()
            print("Оновлено.")
            return

    print("Не знайдено.")

def generate_password():
    length = int(input("Довжина (8-64): "))
    if length < 8 or length > 64:
        print("Невірна довжина.")
        return

    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(chars) for _ in range(length))
    print("Згенерований пароль:", password)

def main():
    if not os.path.exists(FILE):
        vault, key, salt = create_new_vault()
    else:
        vault, key, salt = load_vault()

    while True:
        print("\n1. Додати")
        print("2. Показати запис")
        print("3. Показати всі сервіси")
        print("4. Оновити")
        print("5. Видалити")
        print("6. Згенерувати пароль")
        print("0. Вихід")

        choice = input(">> ")

        if choice == "1":
            add_record(vault)
            save_vault(vault, key, salt)

        elif choice == "2":
            show_record(vault)

        elif choice == "3":
            show_all(vault)

        elif choice == "4":
            update_record(vault)
            save_vault(vault, key, salt)

        elif choice == "5":
            delete_record(vault)
            save_vault(vault, key, salt)

        elif choice == "6":
            generate_password()

        elif choice == "0":
            break

        else:
            print("Невірний вибір.")


if __name__ == "__main__":
    main()
