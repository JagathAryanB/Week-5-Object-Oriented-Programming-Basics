# library.py
import os
import json
import shutil
from datetime import datetime

try:
    from .book import Book
    from .member import Member
except ImportError:
    from book import Book
    from member import Member

class Library:
    """Manages the library collections, operations, and data persistence"""

    def __init__(self, data_dir=None):
        self.books = {}
        self.members = {}

        if data_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.data_dir = os.path.join(base_dir, 'data')
        else:
            self.data_dir = os.path.abspath(data_dir)

        self.books_file = os.path.join(self.data_dir, 'books.json')
        self.members_file = os.path.join(self.data_dir, 'members.json')
        self.backup_dir = os.path.join(self.data_dir, 'backup')

    def add_book(self, book):
        """Add a book to the library collections"""
        if book.isbn in self.books:
            return False, f"Book with ISBN '{book.isbn}' already exists"
        self.books[book.isbn] = book
        return True, f"Book '{book.title}' added successfully"

    def remove_book(self, isbn):
        """Remove a book from the library collections"""
        if isbn not in self.books:
            return False, f"Book with ISBN '{isbn}' not found"
        book = self.books[isbn]
        if not book.available:
            return False, f"Cannot remove book '{book.title}' because it is currently borrowed"
        del self.books[isbn]
        return True, f"Book '{book.title}' removed successfully"

    def find_book(self, isbn):
        """Find a book by ISBN"""
        return self.books.get(isbn)

    def register_member(self, member):
        """Register a new member in the library"""
        if member.member_id in self.members:
            return False, f"Member with ID '{member.member_id}' already registered"
        self.members[member.member_id] = member
        return True, f"Member '{member.name}' registered successfully"

    def find_member(self, member_id):
        """Find a member by ID"""
        return self.members.get(member_id)

    def borrow_book(self, member_id, isbn, loan_period=14):
        """Process book borrowing with limit validation"""
        member = self.find_member(member_id)
        if not member:
            return False, f"Member with ID '{member_id}' not found"

        book = self.find_book(isbn)
        if not book:
            return False, f"Book with ISBN '{isbn}' not found"

        if not book.available:
            return False, f"Book '{book.title}' is currently checked out"

        if not member.can_borrow():
            return False, f"Member '{member.name}' reached maximum borrow limit ({member.max_borrow_limit} books)"

        success, msg = book.check_out(member_id, loan_period)
        if not success:
            return False, msg

        member.borrow_book(isbn)
        return True, f"Book '{book.title}' checked out to {member.name}. Due date: {book.due_date}"

    def return_book(self, member_id, isbn):
        """Process book return with overdue calculation"""
        member = self.find_member(member_id)
        if not member:
            return False, f"Member with ID '{member_id}' not found"

        book = self.find_book(isbn)
        if not book:
            return False, f"Book with ISBN '{isbn}' not found"

        if book.borrowed_by != member_id or isbn not in member.borrowed_books:
            return False, f"Book '{book.title}' is not currently borrowed by member '{member.name}'"

        days_overdue = book.days_overdue()
        success, msg = book.return_book()
        if not success:
            return False, msg

        member.return_book(isbn)
        if days_overdue > 0:
            return True, f"Book '{book.title}' returned successfully by {member.name} (Overdue by {days_overdue} days)"
        return True, f"Book '{book.title}' returned successfully by {member.name}"

    def search_books(self, query, search_by='title'):
        """Search books by title, author, isbn, or retrieve all available books"""
        query_clean = str(query).strip().lower()
        results = []
        for book in self.books.values():
            if search_by == 'title' and query_clean in book.title.lower():
                results.append(book)
            elif search_by == 'author' and query_clean in book.author.lower():
                results.append(book)
            elif search_by == 'isbn' and query_clean in book.isbn.lower():
                results.append(book)
            elif search_by == 'available' and book.available:
                results.append(book)
        return results

    def get_overdue_books(self):
        """Retrieve list of all overdue books"""
        return [book for book in self.books.values() if book.is_overdue()]

    def get_statistics(self):
        """Calculate summary statistics for books and members"""
        total_books = len(self.books)
        available_books = sum(1 for b in self.books.values() if b.available)
        borrowed_books = total_books - available_books
        overdue_books = len(self.get_overdue_books())
        total_members = len(self.members)
        return {
            'total_books': total_books,
            'available_books': available_books,
            'borrowed_books': borrowed_books,
            'overdue_books': overdue_books,
            'total_members': total_members
        }

    def save_books(self, filepath=None):
        """Save books collection to JSON file"""
        target = filepath or self.books_file
        os.makedirs(os.path.dirname(os.path.abspath(target)), exist_ok=True)
        data = [book.to_dict() for book in self.books.values()]
        with open(target, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return len(data)

    def load_books(self, filepath=None):
        """Load books collection from JSON file"""
        target = filepath or self.books_file
        if not os.path.exists(target):
            return 0
        try:
            with open(target, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.books = {}
            for item in data:
                book = Book.from_dict(item)
                self.books[book.isbn] = book
            return len(self.books)
        except Exception:
            return 0

    def save_members(self, filepath=None):
        """Save members collection to JSON file"""
        target = filepath or self.members_file
        os.makedirs(os.path.dirname(os.path.abspath(target)), exist_ok=True)
        data = [member.to_dict() for member in self.members.values()]
        with open(target, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return len(data)

    def load_members(self, filepath=None):
        """Load members collection from JSON file"""
        target = filepath or self.members_file
        if not os.path.exists(target):
            return 0
        try:
            with open(target, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.members = {}
            for item in data:
                member = Member.from_dict(item)
                self.members[member.member_id] = member
            return len(self.members)
        except Exception:
            return 0

    def save_data(self):
        """Save all collections to files"""
        books_count = self.save_books()
        members_count = self.save_members()
        return books_count, members_count

    def load_data(self):
        """Load all collections from files"""
        books_count = self.load_books()
        members_count = self.load_members()
        return books_count, members_count

    def create_backup(self):
        """Create timestamped copies of current data files"""
        os.makedirs(self.backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backups_created = []

        if os.path.exists(self.books_file):
            dest_books = os.path.join(self.backup_dir, f'books_{timestamp}.json')
            shutil.copy2(self.books_file, dest_books)
            backups_created.append(dest_books)

        if os.path.exists(self.members_file):
            dest_members = os.path.join(self.backup_dir, f'members_{timestamp}.json')
            shutil.copy2(self.members_file, dest_members)
            backups_created.append(dest_members)

        return backups_created
