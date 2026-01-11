import os
import random


def ensureFile(filename: str) -> None:
    if os.path.exists(filename):
        return
    f = open(filename, "w", encoding="utf-8")
    f.close()


def loadPoll(filename: str) -> dict[str, list[list]]:
    data = {}
    ensureFile(filename)

    f = open(filename, "r", encoding="utf-8")
    for line in f:
        line = line.strip()
        if not line:
            continue

        parts = line.split(";")
        if len(parts) != 3:
            continue

        q, opt, votes = parts
        q = q.strip()
        opt = opt.strip()

        try:
            votes = int(votes.strip())
        except:
            continue

        if q == "" or opt == "":
            continue

        if q not in data:
            data[q] = []
        data[q].append([opt, votes])

    f.close()
    return data


def savePoll(filename: str, data: dict[str, list[list]]) -> None:
    f = open(filename, "w", encoding="utf-8")
    for q in data:
        for opt, votes in data[q]:
            f.write(f"{q};{opt};{votes}\n")
    f.close()


def chooseQuestion(data: dict[str, list[list]]) -> str:
    questions = list(data.keys())
    if len(questions) == 0:
        print("Опитувань нема.")
        return ""

    for i in range(len(questions)):
        print(f"{i+1}. {questions[i]}")

    s = input("Номер питання: ").strip()
    if not s.isdigit():
        return ""

    idx = int(s) - 1
    if idx < 0 or idx >= len(questions):
        return ""

    return questions[idx]


def createPoll(data: dict[str, list[list]]) -> bool:
    q = input("Питання: ").strip()
    if q == "":
        return False

    if q in data:
        print("Таке питання вже є.")
        return False

    data[q] = []
    print("Вводь варіанти (пусто = кінець):")

    while True:
        opt = input("> ").strip()
        if opt == "":
            break
        data[q].append([opt, 0])

    if len(data[q]) < 2:
        print("Мало варіантів. Скасовано.")
        del data[q]
        return False

    print("Створено.")
    return True


def votePoll(data: dict[str, list[list]]) -> bool:
    q = chooseQuestion(data)
    if q == "":
        return False

    options = data[q]
    if len(options) == 0:
        return False

    print("Питання:", q)
    for i in range(len(options)):
        print(f"{i+1}. {options[i][0]}")

    s = input("Ваш вибір: ").strip()
    if not s.isdigit():
        return False

    idx = int(s) - 1
    if idx < 0 or idx >= len(options):
        return False

    options[idx][1] += 1
    print("Ваш голос зараховано!")
    return True


def showResults(data: dict[str, list[list]]) -> None:
    q = chooseQuestion(data)
    if q == "":
        return

    options = data[q]
    if len(options) == 0:
        return

    max_votes = -1
    for opt, votes in options:
        if votes > max_votes:
            max_votes = votes

    leaders = []
    for opt, votes in options:
        if votes == max_votes:
            leaders.append(opt)

    print("\nРезультати:")
    for opt, votes in options:
        print(f"{opt} — {votes} голосів")

    if len(leaders) == 1:
        print("Лідер:", leaders[0])
    else:
        print("Лідери:", ", ".join(leaders))


def main():
    filename = "poll.csv"
    data = loadPoll(filename)

    changed = False

    while True:
        print("\n1. Створити опитування")
        print("2. Проголосувати")
        print("3. Показати результати")
        print("4. Вихід")

        choice = input(">>> ").strip()

        if choice == "1":
            if createPoll(data):
                changed = True
        elif choice == "2":
            if votePoll(data):
                changed = True
        elif choice == "3":
            showResults(data)
        elif choice == "4":
            break

    if changed:
        savePoll(filename, data)


main()
