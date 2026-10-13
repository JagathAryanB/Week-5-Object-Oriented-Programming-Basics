import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from library_system.member import Member

class TestMember(unittest.TestCase):
    def test_member_initialization(self):
        member = Member("John Doe", "MEM100", max_borrow_limit=5)
        self.assertEqual(member.name, "John Doe")
        self.assertEqual(member.member_id, "MEM100")
        self.assertEqual(member.borrowed_books, [])
        self.assertEqual(member.max_borrow_limit, 5)

    def test_borrow_book_success(self):
        member = Member("John Doe", "MEM100")
        success, msg = member.borrow_book("1234567890")
        self.assertTrue(success)
        self.assertIn("1234567890", member.borrowed_books)

    def test_borrow_limit_reached(self):
        member = Member("John Doe", "MEM100", max_borrow_limit=2)
        member.borrow_book("111")
        member.borrow_book("222")
        self.assertFalse(member.can_borrow())
        success, msg = member.borrow_book("333")
        self.assertFalse(success)
        self.assertIn("Maximum borrow limit reached", msg)

    def test_return_book_success(self):
        member = Member("John Doe", "MEM100")
        member.borrow_book("1234567890")
        success, msg = member.return_book("1234567890")
        self.assertTrue(success)
        self.assertNotIn("1234567890", member.borrowed_books)

    def test_return_unborrowed_book(self):
        member = Member("John Doe", "MEM100")
        success, msg = member.return_book("1234567890")
        self.assertFalse(success)
        self.assertEqual(msg, "Book not found in borrowed list")

    def test_to_dict_and_from_dict(self):
        member = Member("John Doe", "MEM100", max_borrow_limit=3)
        member.borrow_book("111")
        data = member.to_dict()
        recreated = Member.from_dict(data)
        self.assertEqual(recreated.name, member.name)
        self.assertEqual(recreated.member_id, member.member_id)
        self.assertEqual(recreated.borrowed_books, member.borrowed_books)
        self.assertEqual(recreated.max_borrow_limit, 3)

    def test_str_representation(self):
        member = Member("John Doe", "MEM100", max_borrow_limit=5)
        self.assertIn("John Doe", str(member))
        self.assertIn("MEM100", str(member))

if __name__ == '__main__':
    unittest.main()
