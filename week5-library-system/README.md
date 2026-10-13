# Library Management System with OOP

A comprehensive library management system implemented in Python following Object-Oriented Programming (OOP) principles.

## UML Class Diagram

```mermaid
classDiagram
    class Book {
        +str title
        +str author
        +str isbn
        +int year
        +bool available
        +str borrowed_by
        +str due_date
        +str date_added
        +check_out(member_id, loan_period)
        +return_book()
        +is_overdue() bool
        +days_overdue() int
        +to_dict() dict
        +from_dict(data) Book
        +__str__() str
    }

    class Member {
        +str name
        +str member_id
        +list borrowed_books
        +int max_borrow_limit
        +can_borrow() bool
        +borrow_book(isbn)
        +return_book(isbn)
        +to_dict() dict
        +from_dict(data) Member
        +__str__() str
    }

    class Library {
        +dict books
        +dict members
        +str data_dir
        +add_book(book)
        +remove_book(isbn)
        +find_book(isbn) Book
        +register_member(member)
        +find_member(member_id) Member
        +borrow_book(member_id, isbn, loan_period)
        +return_book(member_id, isbn)
        +search_books(query, search_by) list
        +get_overdue_books() list
        +get_statistics() dict
        +save_books(filepath)
        +load_books(filepath)
        +save_members(filepath)
        +load_members(filepath)
        +save_data()
        +load_data()
        +create_backup() list
    }

    Library "1" o-- "*" Book : manages
    Library "1" o-- "*" Member : manages
    Member "1" --> "*" Book : borrows
```

## Features

- **Class Architecture:**
  - `Book`: Manages book metadata, checkout/return states, overdue tracking, serialization (`to_dict`/`from_dict`), and display formatting.
  - `Member`: Manages member profile, active borrowed list, maximum borrow limit enforcement (default 5 books), and serialization.
  - `Library`: Manages collections of books and members, lending transactions, searches, statistics, file persistence, and backups.
- **Search Capabilities:** Search by Title, Author, ISBN, or filter all available books.
- **Overdue Calculations:** Real-time calculation of overdue status and elapsed overdue days.
- **Data Persistence & Backups:** Automatic loading and saving with JSON storage in `data/`, along with timestamped backups in `data/backup/`.
- **Interactive CLI:** Full-featured console menu with input validation and clear status reporting.

## Project Structure

```text
week5-library-system/
├── library_system/
│   ├── __init__.py
│   ├── book.py
│   ├── member.py
│   ├── library.py
│   └── main.py
├── data/
│   ├── books.json
│   ├── members.json
│   └── backup/
├── tests/
│   ├── test_book.py
│   ├── test_member.py
│   └── test_library.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Getting Started

### Prerequisites
- Python 3.8 or higher

### Running the Application

From within the `week5-library-system` folder:
```bash
python library_system/main.py
```

### Running Tests

Execute all unit tests using Python's built-in `unittest` runner:
```bash
python -m unittest discover -s tests
```
