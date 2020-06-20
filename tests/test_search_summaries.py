import sys
sys.path.append("..")
import unittest
from search_summaries import *

class TestMethods(unittest.TestCase):

    # get matching documents with scores (sorted desc) for phrase searched
    def test_get_all_matches(self):

        search_index = {'life':[[1,2],[2,1],[3,1]], 'bird':[[1,4],[2,1]], 'mind':[[1,1],[2,1],[3,5],[4,4]], 'pit':[[1,1]]}
        test_cases = [[['life'], [[2,1],[1,3],[1,2]]],
                      [['life','mind'], [[6,3],[4,4],[3,1],[2,2]]],
                      [['life','mind','bird'], [[7,1],[6,3],[4,4],[3,2]]],
                      [[],[]],
                      [['not', 'present'],[]]]

        for el in test_cases:
            self.assertEqual(get_all_matches(search_index, el[0]), el[1])

if __name__ == '__main__':
    unittest.main()
