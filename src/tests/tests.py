import os
import sys
import unittest

sys.path.insert(0, '..')
sys.path.append('..\src')
sys.path.append('src')

from main_functions import findNovel
from Downloaders import *
from archive_updater import check_env



#target = __import__("my_sum.py")
#sum = target.sum


class TestMainFunctions(unittest.TestCase):


    def setUp(self):
        self.assertTrue(len(findNovel("")) ==
                        len(os.listdir('novel_list')))
    
    def test_builder(self):
       
        x = Novel('n18n2935bp', 'memory rewrite ')
        x = x.updateObject()
        self.assertTrue(x.__class__ == N18SyosetuNovel )
                
    '''        tests Syosetu           '''
    def test_SyosetuNovel(self):
        novel=Novel('n5080fi')
        self.assertTrue(novel.__class__ == Novel)
        novel=novel.updateObject()
        self.assertTrue(novel.__class__ == SyosetuNovel)
        
    def test_fetchSyosetu(self):
        novel=Novel('n5080fi')
        novel=novel.updateObject()
        html = novel.fetchTOCPage()
        self.assertTrue(html != '')
        self.assertRegex(html,'novel_ex')
        
        
    '''   tests kakyomu           '''
    def test_KakyomuNovel(self):
        novel=Novel('16816452220453312822')
        self.assertTrue(novel.__class__ == Novel)
        novel=novel.updateObject()
        self.assertTrue(novel.__class__ == KakuyomuNovel)
    
    def test_fetchKakyomu(self):
        novel=Novel('16816452220453312822')
        novel=novel.updateObject()
        html = novel.fetchTOCPage()
        self.assertTrue(html != '')
        self.assertRegex(html,'workTitle')
        
        
        
        '''   tests n18   '''
    def test_n18SyosetuNovel(self):
        novel=Novel('n18n6426w')
        self.assertTrue(novel.__class__ == Novel)
        novel=novel.updateObject()
        self.assertTrue(novel.__class__ == N18SyosetuNovel)
    
    def test_fetchN18Syosetu(self):
        novel=Novel('n18n6426w')
        novel=novel.updateObject()
        html = novel.fetchTOCPage()
        self.assertTrue(html != '')
        self.assertRegex(html,'novel_ex')
        



if __name__ == '__main__':
    os.mkdir('novel_list')
    unittest.main()
    # runner = unittest.TextTestRunner()
    # runner.run(suite())