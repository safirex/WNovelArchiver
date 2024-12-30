import unittest
from Downloaders import *

class Tests_syosetu(unittest.TestCase):


    def setUp(self):
        global novel
        novel= SyosetuNovel('n7671do', "test", False)
        
    def test_parse_TOC(self):
        html = novel.fetchTOCPage()
        self.assertTrue(html != '',"failed to fetch the html page")
        toc_resume = novel.parseTocResume(html)
        self.assertTrue(toc_resume != '',"failed to parse the TOC resume")
        print("resume = ",toc_resume)
    
    def test_parse_chapter_list(self):
        html = novel.fetchTOCPage()
        chapter_list = novel.parseOnlineChapterList(html)
        self.assertTrue(len(chapter_list) != 0)
        for chap_num in chapter_list:
            with self.subTest(i=chap_num):
                self.assertIsNotNone(int(chap_num))
                self.assertTrue(int(chap_num) > 0 )
                
    # def test_parse_chapter_content(self):
    #     chapter = novel.parse([1])
    #     self.assertTrue(chapter.content !="")
    #     self.assertTrue(chapter.title != "")