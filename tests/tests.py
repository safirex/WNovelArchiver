from archive_updater import check_env
import os
import sys
import unittest

sys.path.insert(0, '..')
sys.path.append('..\src')
sys.path.append('src')

from main_functions import findNovel




#target = __import__("my_sum.py")
#sum = target.sum


class TestMainFunctions(unittest.TestCase):

    def check_environment(self):
        check_env()

    def test_find(self):
        self.assertTrue(len(findNovel("")) ==
                        len(os.listdir('novel_list')))


if __name__ == '__main__':
    unittest.main()
