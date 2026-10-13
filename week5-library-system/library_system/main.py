# main.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from library_system.library import Library
    from library_system.book import Book
    from library_system.member import Member
except ImportError:
    from library import Library
    from book import Book
    from member import Member

def format_book_display(index, book):
    """Format single book details matching project specifications"""
    if book.available:
        status_text = "Available"
    else:
        due_info = f" (Due: {book.due_date})" if book.due_date else ""
        status_text = f"Borrowed by {book.borrowed_by}{due_info}"

    year_text = book.year if book.year is not None else "N/A"
    return (
        f"{index}. {book.title}\n"
        f"   Author: {book.author}\n"
        f"   ISBN: {book.isbn}\n"
        f"   Year: {year_text}\n"
        f"   Status: {status_text}"
    )

def handle_search(library):
    """Handle interactive book search submenu"""
    print("\nSearch books by:")
    print("1. Title")
    print("2. Author")
    print("3. ISBN")
    print("4. Show all available books")

    sub_choice = input("\nEnter search option: ").strip()

    if sub_choice == "1":
        query = input("\nEnter title to search: ").strip()
        results = library.search_books(query, search_by='title')
        header = f"\nSearch Results for '{query}':"
        footer = f"\nFound {len(results)} books matching '{query}'"
    elif sub_choice == "2":
        query = input("\nEnter author to search: ").strip()
        results = library.search_books(query, search_by='author')
        header = f"\nSearch Results for '{query}':"
        footer = f"\nFound {len(results)} books matching '{query}'"
    elif sub_choice == "3":
        query = input("\nEnter ISBN to search: ").strip()
        results = library.search_books(query, search_by='isbn')
        header = f"\nSearch Results for '{query}':"
        footer = f"\nFound {len(results)} books matching '{query}'"
    elif sub_choice == "4":
        results = library.search_books("", search_by='available')
        header = "\nSearch Results for Available Books:"
        footer = f"\nFound {len(results)} available books"
    else:
        print("Invalid search option.")
        return

    print(header)
    print("-" * 50)
    if not results:
        print("No matching books found.")
    else:
        for idx, book in enumerate(results, 1):
            print(format_book_display(idx, book))
            if idx < len(results):
                print()
    print(footer)

def handle_add_book(library):
    """Handle adding a new book to the library"""
    print("\n--- Add New Book ---")
    title = input("Enter title: ").strip()
    author = input("Enter author: ").strip()
    isbn = input("Enter ISBN: ").strip()
    year_input = input("Enter year of publication (optional): ").strip()

    if not title or not author or not isbn:
        print("Error: Title, Author, and ISBN are required.")
        return

    year = None
    if year_input:
        try:
            year = int(year_input)
        except ValueError:
            print("Error: Year must be a valid integer.")
            return

    new_book = Book(title=title, author=author, isbn=isbn, year=year)
    success, message = library.add_book(new_book)
    print(f"\n{message}")

def handle_register_member(library):
    """Handle registering a new member"""
    print("\n--- Register New Member ---")
    name = input("Enter member name: ").strip()
    member_id = input("Enter member ID: ").strip()

    if not name or not member_id:
        print("Error: Member name and ID are required.")
        return

    new_member = Member(name=name, member_id=member_id)
    success, message = library.register_member(new_member)
    print(f"\n{message}")

def handle_borrow_book(library):
    """Handle borrowing a book"""
    print("\n--- Borrow Book ---")
    member_id = input("Enter member ID: ").strip()
    isbn = input("Enter book ISBN: ").strip()
    days_input = input("Enter loan period in days (default 14): ").strip()

    loan_period = 14
    if days_input:
        try:
            loan_period = int(days_input)
        except ValueError:
            print("Error: Loan period must be a valid integer.")
            return

    success, message = library.borrow_book(member_id, isbn, loan_period=loan_period)
    print(f"\n{message}")

def handle_return_book(library):
    """Handle returning a book"""
    print("\n--- Return Book ---")
    member_id = input("Enter member ID: ").strip()
    isbn = input("Enter book ISBN: ").strip()

    success, message = library.return_book(member_id, isbn)
    print(f"\n{message}")

def handle_view_all_books(library):
    """Display all books in the library"""
    print("\n--- All Books in Library ---")
    print("-" * 50)
    if not library.books:
        print("No books available in library.")
        return

    for idx, book in enumerate(library.books.values(), 1):
        print(format_book_display(idx, book))
        if idx < len(library.books):
            print()
    print(f"\nTotal: {len(library.books)} books")

def handle_view_all_members(library):
    """Display all registered members"""
    print("\n--- All Registered Members ---")
    print("-" * 50)
    if not library.members:
        print("No members registered.")
        return

    for idx, member in enumerate(library.members.values(), 1):
        borrowed_info = ", ".join(member.borrowed_books) if member.borrowed_books else "None"
        print(f"{idx}. {member.name} (ID: {member.member_id})")
        print(f"   Borrowed ({len(member.borrowed_books)}/{member.max_borrow_limit}): {borrowed_info}")
        if idx < len(library.members):
            print()
    print(f"\nTotal: {len(library.members)} members")

def handle_view_overdue_books(library):
    """Display overdue books"""
    print("\n--- Overdue Books ---")
    print("-" * 50)
    overdue = library.get_overdue_books()
    if not overdue:
        print("No books are currently overdue.")
        return

    for idx, book in enumerate(overdue, 1):
        print(format_book_display(idx, book))
        print(f"   Overdue by: {book.days_overdue()} days")
        if idx < len(overdue):
            print()
    print(f"\nTotal: {len(overdue)} overdue books")

def main():
    """Main execution loop for Library Management System"""
    library = Library()

    print("=================================")
    print("    LIBRARY MANAGEMENT SYSTEM")
    print("=================================")

    books_loaded, members_loaded = library.load_data()
    print(f"Loaded {books_loaded} books from file")
    print(f"Loaded {members_loaded} members from file")

    while True:
        print("\n1. Add New Book")
        print("2. Register New Member")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Search Books")
        print("6. View All Books")
        print("7. View All Members")
        print("8. View Overdue Books")
        print("9. Save & Exit")
        print("0. Exit Without Saving")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            handle_add_book(library)
        elif choice == "2":
            handle_register_member(library)
        elif choice == "3":
            handle_borrow_book(library)
        elif choice == "4":
            handle_return_book(library)
        elif choice == "5":
            handle_search(library)
        elif choice == "6":
            handle_view_all_books(library)
        elif choice == "7":
            handle_view_all_members(library)
        elif choice == "8":
            handle_view_overdue_books(library)
        elif choice == "9":
            library.create_backup()
            library.save_data()
            print("\nData saved successfully and backup created. Exiting...")
            break
        elif choice == "0":
            print("\nExiting without saving changes.")
            break
        else:
            print("Invalid choice. Please select an option from 0 to 9.")

if __name__ == "__main__":
    main()
