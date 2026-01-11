import os
import random


def loadWords(filename: str) -> dict[str, str]:
    words = {}
    if not os.path.exists(filename):
        f = open(filename, "w", encoding="utf-8")
        f.write("кіт;cat\n")
        f.write("собака;dog\n")
        f.write("будинок;house\n")
        f.close()

    f = open(filename, "r", encoding="utf-8")
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split(";")
        if len(parts) != 2:
            continue
        uk, en = parts
        words[uk.strip().lower()] = en.strip().lower()
    f.close()
    return words


def loadStats(filename: str) -> dict[str, list[int]]:
    stats = {}
    if not os.path.exists(filename):
        return stats

    f = open(filename, "r", encoding="utf-8")
    for line in f:
        line = line.strip()
        if not line or line.lower().startswith("слово"):
            continue
        parts = line.split(";")
        if len(parts) != 3:
            continue
        word, total, correct = parts
        try:
            total = int(total)
            correct = int(correct)
        except:
            continue
        stats[word.strip().lower()] = [total, correct]
    f.close()
    return stats


def saveStats(filename: str, stats: dict[str, list[int]]) -> None:
    f = open(filename, "w", encoding="utf-8")
    f.write("СЛОВО_UK;ВСЬОГО_СПРОБ;ПРАВИЛЬНИХ\n")
    for word in stats:
        total, correct = stats[word]
        f.write(f"{word};{total};{correct}\n")
    f.close()


def train(words: dict[str, str], stats: dict[str, list[int]]) -> None:
    keys = list(words.keys())

    for i in range(5):
        word = random.choice(keys)
        if word not in stats:
            stats[word] = [0, 0]

        answer = input(f"{word}: ").strip().lower()
        stats[word][0] += 1

        if answer == words[word]:
            print("Правильно")
            stats[word][1] += 1
        else:
            print("Неправильно, правильна відповідь:", words[word])


def showResult(stats: dict[str, list[int]]) -> None:
    print("\nРезультати:")
    for word in stats:
        total, correct = stats[word]
        if total == 0:
            percent = 0
        else:
            percent = int(correct / total * 100)
        print(word, "-", correct, "/", total, f"({percent}%)")


def main():
    words = loadWords("words.csv")
    stats = loadStats("stats.csv")

    train(words, stats)
    saveStats("stats.csv", stats)
    showResult(stats)


main()
