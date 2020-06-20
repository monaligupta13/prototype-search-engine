import sys
sys.path.append("..")
import unittest
from text_processing import token_list

class TestMethods(unittest.TestCase):

    def test_token_list(self):
        test_cases = {'' : [], 'life is a magical game' : ['life', 'magic', 'game'], 'is a' : []}

        for input, output in test_cases.items():
            self.assertEqual(token_list(input), output)

if __name__ == '__main__':
    unittest.main()
