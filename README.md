# Week 5: Object-Oriented Programming Basics

This repository contains the complete implementation for **Week 5: Object-Oriented Programming Basics** from **The Developers Arena**.

## UML Class Diagram (Step 1)

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

## Contents

1. **Hands-On Practice**: Located in [`hands_on_practice.py`](file:///c:/devolopers%20arena/Week-5-Object-Oriented-Programming-Basics/hands_on_practice.py).
   - `Student` class with name, age, and grade attributes
   - `BankAccount` class with deposit and withdraw methods
   - `PracticeBook` class with status property management
   - `Vehicle`, `Car`, and `Motorcycle` inheritance hierarchy
   - Multi-object instantiation examples

2. **Library Management System with OOP**: Located in [`week5-library-system/`](file:///c:/devolopers%20arena/Week-5-Object-Oriented-Programming-Basics/week5-library-system/).
   - `Book` class ([`book.py`](file:///c:/devolopers%20arena/Week-5-Object-Oriented-Programming-Basics/week5-library-system/library_system/book.py)): Checkout, return, overdue tracking, days overdue calculation, JSON serialization.
   - `Member` class ([`member.py`](file:///c:/devolopers%20arena/Week-5-Object-Oriented-Programming-Basics/week5-library-system/library_system/member.py)): Member details, borrow tracking, and 5-book limit enforcement.
   - `Library` class ([`library.py`](file:///c:/devolopers%20arena/Week-5-Object-Oriented-Programming-Basics/week5-library-system/library_system/library.py)): Collection management, book borrowing/returns, searches, statistics, file persistence, and backups.
   - Interactive Menu System ([`main.py`](file:///c:/devolopers%20arena/Week-5-Object-Oriented-Programming-Basics/week5-library-system/library_system/main.py)): Full terminal UI matching the reference specification.
   - Automated Unit Test Suite ([`tests/`](file:///c:/devolopers%20arena/Week-5-Object-Oriented-Programming-Basics/week5-library-system/tests/)): Unit tests for Book, Member, and Library classes.

## Execution

### Run Hands-On Practice
```bash
python hands_on_practice.py
```

### Run Library Management System
```bash
python week5-library-system/library_system/main.py
```

### Run Test Suite
```bash
python -m unittest discover -s week5-library-system/tests
```
