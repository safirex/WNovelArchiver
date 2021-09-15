import os
import sys
import unittest

sys.path.insert(0, '..')
sys.path.append('..\src')
sys.path.append('src')

from main_functions import findNovel

class TestMainFunctions(unittest.TestCase):

    def test_find(self):
        self.assertTrue(len(findNovel("")) ==
                        len(os.listdir('novel_list')))


if __name__ == '__main__':
    unittest.main()
