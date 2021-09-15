import os
import sys

sys.path.insert(0,'..')
sys.path.append('..\src')

from main_functions import findNovel
import unittest

class TestMainFunctions(unittest.TestCase):
    
    def test_find(self):
        self.assertTrue(len(findNovel("",'../novel_list'))== \
            len(os.listdir('../novel_list')))
        




if __name__ == '__main__':
    unittest.main()