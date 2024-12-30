import os
import sys
import unittest

sys.path.insert(0, '..')
sys.path.append('..\src')
sys.path.append('src')

from main_functions import findNovel
from Downloaders import *
from archive_updater import check_env

class TestMainFunctions(unittest.TestCase):

    def test_find_novel_folder(self):
        self.assertTrue(len(findNovel("")) == len(os.listdir('novel_list')))

if __name__ == '__main__':
    os.mkdir('novel_list')
    unittest.main()
    # runner = unittest.TextTestRunner()
    # runner.run(suite())