import unittest
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from library_system.book import Book

class TestBook(unittest.TestCase):
    def test_book_initialization(self):
        book = Book("1984", "George Orwell", "1234567890", 1949)
        self.assertEqual(book.title, "1984")
        self.assertEqual(book.author, "George Orwell")
        self.assertEqual(book.isbn, "1234567890")
        self.assertEqual(book.year, 1949)
        self.assertTrue(book.available)
        self.assertIsNone(book.borrowed_by)
        self.assertIsNone(book.due_date)
        self.assertIsNotNone(book.date_added)

    def test_check_out_success(self):
        book = Book("1984", "George Orwell", "1234567890", 1949)
        success, msg = book.check_out("MEM001", loan_period=14)
        self.assertTrue(success)
        self.assertFalse(book.available)
        self.assertEqual(book.borrowed_by, "MEM001")
        self.assertIsNotNone(book.due_date)

    def test_check_out_already_checked_out(self):
        book = Book("1984", "George Orwell", "1234567890", 1949)
        book.check_out("MEM001")
        success, msg = book.check_out("MEM002")
        self.assertFalse(success)
        self.assertEqual(msg, "Book is already checked out")

    def test_return_book_success(self):
        book = Book("1984", "George Orwell", "1234567890", 1949)
        book.check_out("MEM001")
        success, msg = book.return_book()
        self.assertTrue(success)
        self.assertTrue(book.available)
        self.assertIsNone(book.borrowed_by)
        self.assertIsNone(book.due_date)

    def test_return_book_already_available(self):
        book = Book("1984", "George Orwell", "1234567890", 1949)
        success, msg = book.return_book()
        self.assertFalse(success)
        self.assertEqual(msg, "Book is already available")

    def test_is_overdue_and_days_overdue(self):
        book = Book("1984", "George Orwell", "1234567890", 1949)
        book.check_out("MEM001")
        past_date = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
        book.due_date = past_date
        self.assertTrue(book.is_overdue())
        self.assertGreaterEqual(book.days_overdue(), 4)

    def test_to_dict_and_from_dict(self):
        book = Book("1984", "George Orwell", "1234567890", 1949)
        data = book.to_dict()
        recreated = Book.from_dict(data)
        self.assertEqual(recreated.title, book.title)
        self.assertEqual(recreated.author, book.author)
        self.assertEqual(recreated.isbn, book.isbn)
        self.assertEqual(recreated.year, book.year)
        self.assertEqual(recreated.available, book.available)

    def test_str_representation(self):
        book = Book("1984", "George Orwell", "1234567890", 1949)
        self.assertIn("1984", str(book))
        self.assertIn("Available", str(book))
        book.check_out("MEM001")
        self.assertIn("Borrowed by MEM001", str(book))

if __name__ == '__main__':
    unittest.main()
