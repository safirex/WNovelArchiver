import os
import sys
import unittest

sys.path.insert(0, '..')
sys.path.append('..\src')
sys.path.append('src')

from main_functions import findNovel
from Downloaders import KakuyomuNovel, Novel
from archive_updater import check_env



#target = __import__("my_sum.py")
#sum = target.sum


class TestMainFunctions(unittest.TestCase):

    def test_find(self):
        self.assertTrue(len(findNovel("")) ==
                        len(os.listdir('novel_list')))
    
    def builder(self):
        novel=Novel(16816452220453312822)
        self.assertTrue(novel.__class__==Novel.__class__)
        novel=novel.updateObject();
        self.assertTrue(novel.__class__==KakuyomuNovel.__class__)





if __name__ == '__main__':
    check_env()
    unittest.main()
