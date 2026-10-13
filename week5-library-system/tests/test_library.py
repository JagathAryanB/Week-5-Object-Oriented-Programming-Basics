import unittest
import sys
import os
import shutil
import tempfile
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from library_system.library import Library
from library_system.book import Book
from library_system.member import Member

class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.library = Library(data_dir=self.temp_dir)
        self.sample_book = Book("Python Crash Course", "Eric Matthes", "9781593279288", 2019)
        self.sample_member = Member("Alice Johnson", "MEM001")
        self.library.add_book(self.sample_book)
        self.library.register_member(self.sample_member)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_add_and_find_book(self):
        book = self.library.find_book("9781593279288")
        self.assertIsNotNone(book)
        self.assertEqual(book.title, "Python Crash Course")

    def test_add_duplicate_book(self):
        duplicate = Book("Duplicate", "Author", "9781593279288", 2020)
        success, msg = self.library.add_book(duplicate)
        self.assertFalse(success)

    def test_remove_book(self):
        success, msg = self.library.remove_book("9781593279288")
        self.assertTrue(success)
        self.assertIsNone(self.library.find_book("9781593279288"))

    def test_remove_borrowed_book_fails(self):
        self.library.borrow_book("MEM001", "9781593279288")
        success, msg = self.library.remove_book("9781593279288")
        self.assertFalse(success)

    def test_register_and_find_member(self):
        member = self.library.find_member("MEM001")
        self.assertIsNotNone(member)
        self.assertEqual(member.name, "Alice Johnson")

    def test_borrow_and_return_book(self):
        success, msg = self.library.borrow_book("MEM001", "9781593279288")
        self.assertTrue(success)
        self.assertFalse(self.sample_book.available)
        self.assertEqual(self.sample_book.borrowed_by, "MEM001")
        self.assertIn("9781593279288", self.sample_member.borrowed_books)

        ret_success, ret_msg = self.library.return_book("MEM001", "9781593279288")
        self.assertTrue(ret_success)
        self.assertTrue(self.sample_book.available)
        self.assertNotIn("9781593279288", self.sample_member.borrowed_books)

    def test_return_book_overdue_notice(self):
        self.library.borrow_book("MEM001", "9781593279288")
        past_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
        self.sample_book.due_date = past_date

        ret_success, ret_msg = self.library.return_book("MEM001", "9781593279288")
        self.assertTrue(ret_success)
        self.assertIn("Overdue", ret_msg)

    def test_search_books(self):
        book2 = Book("Fluent Python", "Luciano Ramalho", "9781491946008", 2022)
        self.library.add_book(book2)

        results_title = self.library.search_books("python", search_by='title')
        self.assertEqual(len(results_title), 2)

        results_author = self.library.search_books("matthes", search_by='author')
        self.assertEqual(len(results_author), 1)

        results_isbn = self.library.search_books("9781491946008", search_by='isbn')
        self.assertEqual(len(results_isbn), 1)

    def test_statistics(self):
        stats = self.library.get_statistics()
        self.assertEqual(stats['total_books'], 1)
        self.assertEqual(stats['available_books'], 1)
        self.assertEqual(stats['borrowed_books'], 0)
        self.assertEqual(stats['overdue_books'], 0)
        self.assertEqual(stats['total_members'], 1)

    def test_save_and_load_persistence(self):
        self.library.save_data()

        new_library = Library(data_dir=self.temp_dir)
        b_count, m_count = new_library.load_data()

        self.assertEqual(b_count, 1)
        self.assertEqual(m_count, 1)
        self.assertIn("9781593279288", new_library.books)
        self.assertIn("MEM001", new_library.members)

    def test_create_backup(self):
        self.library.save_data()
        backups = self.library.create_backup()
        self.assertTrue(len(backups) >= 2)
        for backup_file in backups:
            self.assertTrue(os.path.exists(backup_file))

if __name__ == '__main__':
    unittest.main()
