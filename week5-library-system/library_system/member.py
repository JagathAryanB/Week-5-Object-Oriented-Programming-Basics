# member.py

class Member:
    """Represents a library member"""

    def __init__(self, name, member_id, max_borrow_limit=5):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []
        self.max_borrow_limit = max_borrow_limit

    def can_borrow(self):
        """Check if member has reached borrow limit"""
        return len(self.borrowed_books) < self.max_borrow_limit

    def borrow_book(self, isbn):
        """Add book to borrowed list"""
        if not self.can_borrow():
            return False, f"Maximum borrow limit reached ({self.max_borrow_limit} books)"
        if isbn in self.borrowed_books:
            return False, "Book is already borrowed by this member"
        self.borrowed_books.append(isbn)
        return True, "Book borrowed successfully"

    def return_book(self, isbn):
        """Remove book from borrowed list"""
        if isbn not in self.borrowed_books:
            return False, "Book not found in borrowed list"
        self.borrowed_books.remove(isbn)
        return True, "Book returned successfully"

    def to_dict(self):
        """Convert member to dictionary for serialization"""
        return {
            'name': self.name,
            'member_id': self.member_id,
            'borrowed_books': self.borrowed_books,
            'max_borrow_limit': self.max_borrow_limit
        }

    @classmethod
    def from_dict(cls, data):
        """Create Member instance from dictionary"""
        member = cls(
            name=data['name'],
            member_id=data['member_id'],
            max_borrow_limit=data.get('max_borrow_limit', 5)
        )
        member.borrowed_books = list(data.get('borrowed_books', []))
        return member

    def __str__(self):
        return f"Member: {self.name} (ID: {self.member_id}) - Borrowed: {len(self.borrowed_books)}/{self.max_borrow_limit}"
