import os
import unittest
from Downloaders import *

class Test_n18(unittest.TestCase):

    def setUp(self):
        global novel
        novel=N18SyosetuNovel('n18n6426w',"test", False)
    
    def test_parse_TOC(self):
        html = novel.fetchTOCPage()
        self.assertTrue(html != '',"failed to fetch the html page")
        toc = novel.parseTocResume(html)
        self.assertTrue(toc != '',"failed to parse the TOC resume")
    
    def test_parse_chapter_list(self):
        html = novel.fetchTOCPage()
        chapter_list = novel.parseOnlineChapterList(html)
        self.assertTrue(len(chapter_list) != 0)
        for chap_num in chapter_list:
            with self.subTest(i=chap_num):
                self.assertIsNotNone(int(chap_num))
                self.assertTrue(int(chap_num) > 0 )
                
    def test_parse_chapter_content(self):
        chapter = novel.processChapter(1)
        self.assertTrue(chapter.content !="")
        self.assertTrue(chapter.title != "")

if __name__ == '__main__':
    os.mkdir('novel_list')
    unittest.main()
    # runner = unittest.TextTestRunner()
    # runner.run(suite())