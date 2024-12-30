import os
import sys
import unittest

sys.path.insert(0, '..')
sys.path.append('..\src')
sys.path.append('src')

from main_functions import findNovel
from Downloaders import *
from archive_updater import check_env


class Test_factory(unittest.TestCase):

    def setUp(self):
        global factory 
        factory= NovelFactory()
        factory.registerObject(SyosetuNovel)
        factory.registerObject(N18SyosetuNovel)
        factory.registerObject(KakuyomuNovel)
        
    def test_builder_n18(self):
        x= factory.getNovel('n18n2935bp', 'memory rewrite ')
        self.assertTrue(x.__class__ == N18SyosetuNovel )
                
    def test_builder_syosetu(self):
        novel=factory.getNovel('n5080fi')
        self.assertTrue(novel.__class__ == SyosetuNovel)
        
    def test_builder_kakuyomu(self):
        novel=factory.getNovel('16816452220453312822')
        self.assertTrue(novel.__class__ == KakuyomuNovel)