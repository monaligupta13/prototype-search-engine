import sys
sys.path.append("..")
import unittest
from unittest import mock
from unittest.mock import patch
from find_books import queryBooks

class TestMethods(unittest.TestCase):

    @mock.patch('find_books.getSummaries', return_value=[{'id':1, 'summary':'first summary'}, {'id':2, 'summary':'second summary'}])
    def test_queryBooks(self, mock_getSummaries):
        self.assertEqual(queryBooks('query life', 2), [{'id': 1, 'summary': 'first summary', 'query': 'query life', 'author': 'Grant Cardone'}, {'id': 2, 'summary': 'second summary', 'query': 'query life', 'author': 'Anna Quindlen'}])

if __name__ == '__main__':
    unittest.main()
