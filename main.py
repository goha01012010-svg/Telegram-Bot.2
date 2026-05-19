import json
import os
from datetime import datetime

DATA_FILE = "books.json"

def load_books():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_books(books):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

def add_book(books):
    author = input("Введите автора: ").strip()
    title = input("Введите название: ").strip()
    
    for book in books:
        if book["author"].lower() == author.lower() and book["title"].lower() == title.lower():
            print("Ошибка: такая книга уже есть!")
            return
    
    try:
        rating = int(input("Оценка (1–5): "))
        if rating < 1 or rating > 5:
            print("Оценка от 1 до 5")
            return
    except ValueError:
        print("Введите число")
        return
    
    date = input("Дата (ГГГГ-ММ-ДД): ")
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Неверный формат даты")
        return
    
    books.append({"author": author, "title": title, "rating": rating, "date": date})
    save_books(books)
    print("Книга добавлена!")

def show_all_books(books):
    if not books:
        print("Список пуст")
        return
    for i, b in enumerate(books, 1):
        print(f"{i}. {b['author']} — {b['title']} | Оценка: {b['rating']} | {b['date']}")

def show_average_rating(books):
    if not books:
        print("Нет книг")
        return
    avg = sum(b["rating"] for b in books) / len(books)
    print(f"Средняя оценка: {avg:.2f}")

def show_stats_by_author(books):
    if not books:
        print("Нет книг")
        return
    stats = {}
    for b in books:
        stats[b["author"]] = stats.get(b["author"], 0) + 1
    for author, count in stats.items():
        print(f"{author}: {count} книг(и)")

def delete_book(books):
    if not books:
        print("Нет книг")
        return
    show_all_books(books)
    try:
        idx = int(input("Номер книги для удаления: ")) - 1
        if 0 <= idx < len(books):
            removed = books.pop(idx)
            save_books(books)
            print(f"Удалена: {removed['title']}")
        else:
            print("Неверный номер")
    except ValueError:
        print("Введите число")

def main():
    books = load_books()
    while True:
        print("\n1. Добавить книгу\n2. Показать все\n3. Средняя оценка\n4. Статистика по авторам\n5. Удалить книгу\n6. Выход")
        choice = input("Выберите: ")
        if choice == "1":
            add_book(books)
            books = load_books()
        elif choice == "2":
            show_all_books(books)
        elif choice == "3":
            show_average_rating(books)
        elif choice == "4":
            show_stats_by_author(books)
        elif choice == "5":
            delete_book(books)
            books = load_books()
        elif choice == "6":
            print("До свидания!")
            break
        else:
            print("Неверный ввод")

if __name__ == "__main__":
    main()
