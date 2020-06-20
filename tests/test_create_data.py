import sys
sys.path.append("..")
import unittest
from create_data import *

class TestMethods(unittest.TestCase):

    def test_document_token_count(self):
        test_cases = {1:[6, ['life','practic','win','life','practic','life'], {'life':[1,3],'practic':[1,2],'win':[1,1]}], 3:[1, ['life'], {'life':[3,1]}]}
        for id, input_output in test_cases.items():
            self.assertEqual(document_token_count(input_output[0], input_output[1], id), input_output[2])

    def test_create_dictionary_data(self):
        test_data = [
            {
                "id": 1,
                "summary": "The Book in Three Sentences: life people have control of your life."
            },
            {
                "id": 2,
                "summary": "The Book in Three Sentences: People spend their life."
            }
        ]
        result = {
            "life":[[1,'0.1505'],[2,'0.1003']],
            "peopl":[[1,'0.0752'],[2,'0.1003']],
            "control":[[1,'0.1193']],
            "spend":[[2,'0.1590']]
        }
        compare = create_dictionary_data(test_data)
        self.assertEqual(result, compare)

if __name__ == '__main__':
    unittest.main()
