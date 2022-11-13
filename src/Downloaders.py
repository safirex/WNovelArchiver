# coding: utf-8
from abc import ABC, abstractmethod
from urllib.error import HTTPError
import requests
import re
from bs4 import BeautifulSoup

from src.Chapters import *

# packages for callbacks
from inspect import signature
from enum import Enum, auto

class Callbacks(Enum):
    ChapterListFetched = auto(),
    ChapterBeginUpdate = auto(),
    ChapterBeginFetch = auto(),
    ChapterEndFetch = auto(),
    NovelBeginUpdate = auto(),
    NovelBeginTOCFetch = auto(),
    NovelEndTOCFetch = auto(),
    NovelNotFound = auto(),
    

class SystemCallbacks(ABC):
    """gives to subclass a callback interface"""
    def __init__(self, enum: Enum = Callbacks):
        self.enum = enum
        self.callbacks_dict = dict()
        self.init_callback_list()

    def init_callback_list(self):
        for enum in self.enum:
            self.callbacks_dict[enum] = []

    def registerCallback(self, hook: Enum, callback):
        """add a the callback to the method called on hook call"""
        self.callbacks_dict.get(hook).append(callback)
        
    def removeCallback(self, hook: Enum, callback):
        self.callbacks_dict.get(hook).remove(callback)

    def exec_callbacks(self,hook: Enum ,args=None):
        for method in self.callbacks_dict[hook]:
            sig = signature(method)
            params = sig.parameters
            if (len(params) <= 1):
                method()
            else:
                method(args)


class NovelCallbacks(SystemCallbacks):
    """middle-man between callback implementation and novel class for more visibility"""
    def __init__(self):
        super().__init__()
        self.init_callbacks()
        
        
    def init_callbacks(self):
        """create a Novel basic callback"""
        self.registerCallback(Callbacks.ChapterBeginUpdate,self.tempFunc)
        self.registerCallback(Callbacks.ChapterListFetched,self.onChapterListFetched)
        
    def tempFunc(self):
        print("callback works")
        
    def onChapterListFetched(self):
        print("chapter list obtained")
    

# TODO: updateObject should be in a NovelFactory 
class Novel(NovelCallbacks):
    def __init__(self, codeNovel, titreNovel, keep_text_format=False):
        super().__init__()
        self.code = codeNovel
        self.titre = titreNovel
        self.keep_text_format = keep_text_format
        self.headers = ''
        
        # if(type(self)==Novel):
        #     print("i automatically update this shit")
        #     self.updateObject()
        if(type(self)!=Novel):
            self.setUrl()
            self.setDir('./novel_list/'+self.code+' '+self.titre)
        
    def downloadNovel(self, chapter) -> str:
        """ download chapter from site. """
        pass

    def processNovel(self) -> str:
        """ will process the html and download the chapter """
        pass

    def getNovelTitle(self,html="") -> str:
        """ get the novel title from the TOC html page """
        html = self.fetchTOCPage()
        title = self.parseTitle(html)
        return title
        pass

    def updateObject(self):
        """ instantiate a subclass depending on the object code attribute """

        if (len(self.code) > 7 and self.code.find('n18n') == 0):
            return N18SyosetuNovel(self)
        elif (len(self.code) >= 6 and len(self.code) <= 7 and self.code.find('n') == 0):
            return SyosetuNovel(self)
        elif (len(self.code) == len('1177354054888541019') or
              len(self.code) == len('16816452219449457673')):
            return KakuyomuNovel(self)
        elif (self.code.lower().find('wuxiaworld') == 0):
            return WuxiaWorldNovel(self)
        else:
            return 0

    # not used maybe one day
    @classmethod
    def getNovel(codeNovel, titreNovel, keep_text_format=False):
        """ instantiate a subclass depending on the object code attribute """
        nov = Novel(codeNovel, titreNovel, keep_text_format=False)
        return nov.updateObject()

    def createFile(self, chapterNumber, chapter_title, chapter_content: str):
        chapter_title = checkFileName(chapter_title)
        print('saving %s %s' % (chapterNumber, chapter_title))
        file = open('%s/%d_%s.txt' % (self.getDir(), chapterNumber,
                                      chapter_title), 'w+', encoding='utf-8')
        file.write(chapter_title + '\n')
        file.write(chapter_content)
        file.close()
        print('\n\n')

    def createFile(self, chapterNumber, chapter_title, chapter_content: list):
        chapter_title = checkFileName(chapter_title)
        print('saving %s %s' % (chapterNumber, chapter_title))
        file = open('%s/%d_%s.txt' % (self.getDir(), chapterNumber,
                                      chapter_title), 'w+', encoding='utf-8')
        file.write(chapter_title + '\n')
        for line in chapter_content:
            file.write(str(line))
        file.close()
        print('\n\n')

    
    def setLastChapter(self, chap):
        self.chap = chap

    def getLastChapter(self):
        return self.chap

    def setDir(self, dir):
        self.dir = dir

    def getDir(self):
        return self.dir

    def parseTitle(self, TocHTML) ->str:
        pass

    def getTitle(self):
        return self.titre

    def setCode(self, code):
        self.code = code

    def setUrl(self):
        """method meant to be implemented by subclasses, determine the url to said novel"""
        pass
    
    
    def fetchTOCPage(self):
        """fetch the TOC page of the novel"""
        url = self.url
        headers = self.headers
        print('accessing: ' + url)
        print()
        rep = requests.get(url, headers=headers)
        rep.encoding = 'utf-8'
        rep.raise_for_status()
        html = rep.text
        self.html = html
        return html

    def parseOnlineChapterList(self, html) -> list:
        """parse the list of chapters from the HTML of the TOC page"""
        pass

    def parseTocResume(self, html=''):
        """ format and interpret the content of the home page of the novel """
        pass

    def processNovel(self):
        print("novel " + self.titre)
        print('last chapter: ' + str(self.getLastChapter()))
        try:
            html = self.fetchTOCPage();
        except  requests.HTTPError :
            print("can't acces the novel TOC page")
            return ''
        # get the number of chapters (solely for user feedback)
        online_chapter_list = self.parseOnlineChapterList(html)
        if (self.getLastChapter() == 0):
            resumeContent = self.parseTocResume(html)
            # self.save("0_TOC",resumeContent)
        if (len(online_chapter_list) >= 1):

            # get the chapters url
            lastDL = self.getLastChapter()
            online_chapter_list = online_chapter_list[lastDL:]
            print("there are %d chapters to udpate" % len(online_chapter_list))
            print(online_chapter_list)
            self.processChapter(online_chapter_list)
            # will add new files for every revised chapters
            self.updatePerDate(html)
        else:
            print("this web novel has most likely been terminated")
            
    def processChapter(self, chapList):
        """ download every chapter of the list """
        for chapter_num in chapList:
                chap = self.getChapter(chapter_num)
                chap.createFile(self.dir + '/')
        pass
    def getChapter(self,chapter_num) ->Chapter:
        """return the subclass chapter type"""
        pass
    
    def updatePerDate(self,html):
        """check if local files are outdate compared to online chapters"""
        pass

class SyosetuNovel(Novel):
    def __init__(self, Novel):
        self.site = 'https://ncode.syosetu.com/'
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
        super().__init__(Novel.code, Novel.titre, Novel.keep_text_format)
    
    def setUrl(self):
        self.url = self.site + self.code + "/"
    
    def updatePerDate(self, html):
        """check every local file is the same version as online """
        from bs4 import BeautifulSoup
        from datetime import date
        import os
        soup = BeautifulSoup(html, 'html.parser')
        online_chap_list = []
        for h in soup.find_all('dl'):
            tmpChapTitle = h.find('a').text
            tmpChapUpdateDate = h.find('dt').text[1:11].replace('/', '-')
            tmp = [tmpChapTitle, tmpChapUpdateDate]
            online_chap_list.append(tmp)

        dirList = os.listdir(self.getDir())

        # check that no online chapter has been removed / aka whole story deleted
        if (len(dirList) < len(online_chap_list)):
            for offlineChap in dirList:
                fileDir = self.getDir() + '/' + offlineChap
                modifTime = date.fromtimestamp(os.stat(fileDir).st_mtime)
                offChapNum = int(offlineChap[:offlineChap.find('_')])

                # time to check if a chap has been modified since download
                if (offChapNum != 0) & (len(online_chap_list) - 1 >= offChapNum):
                    onlineDate = online_chap_list[offChapNum - 1][1]
                    onlineDate = date.fromisoformat(onlineDate)
                    if (onlineDate > modifTime):
                        # modif after last revision of chapter
                        print('need update man')
                        chap = self.processChapter(int(offChapNum))
                        chap.createFile(self.dir + '/')
                        print('updated chap ' + str(offChapNum))
        print("fin update")

    def parseOnlineChapterList(self, html='') -> list:
        if html == '':
            html = self.html
        online_chapter_list = re.findall(
            r'<a href="/' + self.code + '/' + '(.*?)' + '/">.*?</a>', html, re.S)
        if (online_chapter_list is None or len(online_chapter_list) == 0):
            print("the novel has most likely been terminated\n")
        return online_chapter_list

    def fetchTOCPage(self):
        url = self.url
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
        }
        rep = requests.get(url, headers=headers)
        rep.encoding = 'utf-8'
        html = rep.text
        self.html = html
        return html

    def parseTocResume(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        resume = soup.find("div", id="novel_ex")
        # resume=re.findall('<div id="novel_ex">'+'(.*?)'+'</div>',html,re.S)[0]
        if (resume is None):
            print("the novel has most likely been terminated")
        else:
            # self.cleanText(resume)
            string = 'novel title= ' + self.getNovelTitle(html) + '\n\n'
            resume.insert(0, string)
            self.createFile(0, 'TOC', resume)

    def getChapter(self, chapter_num):
        chapter = SyosetuChapter(self.code, chapter_num)
        chapter.processChapter(self.headers)
        return chapter

    def cleanText(self, chapter_content):
        chapter_content = chapter_content.replace('</p>', '\r\n')
        chapter_content = chapter_content.replace('<br />', '')
        chapter_content = chapter_content.replace('<rb>', '')
        chapter_content = chapter_content.replace('</rb>', '')
        chapter_content = chapter_content.replace('<rp>', '')
        chapter_content = chapter_content.replace('</rp>', '')
        chapter_content = chapter_content.replace('<rt>', '')
        chapter_content = chapter_content.replace('</rt>', '')
        chapter_content = chapter_content.replace('<ruby>', '')
        chapter_content = chapter_content.replace('</ruby>', '')
        return chapter_content

    def validateTitle(self, title):
        rstr = r"[\/\\\:\*\?\"\<\>\|]"
        new_title = re.sub(rstr, "_", title)
        return new_title
    def parseTitle(self, TocHTML) -> str:

        writer = re.findall(r'<p class="novel_title">(.*?)</p>', TocHTML, re.S)
        print('title = '+str(writer))
        return writer[0]

        


def test():
    import os

    x = Novel('n6912eh', 'My Skills Are Too Strong to Be a Heroine')

    x = x.updateObject()
    x.setLastChapter(0)
    print(x)
    name = x.titre
    print(name)
    dir = './novel_list/' + x.code + ' ' + name
    print(dir)

    print("dir=  " + dir)
    # dir='./novel_list/'+code+' '+name
    x.setDir(dir)
    x.setLastChapter(145)
    x.processNovel()


class KakuyomuNovel(Novel):
    def __init__(self, Novel):
        super().__init__(Novel.code, Novel.titre, Novel.keep_text_format)

    def setUrl(self):
        self.url = 'https://kakuyomu.jp/works/%s' % self.code

    def parseTitle(self, TocHTML):
        soup = BeautifulSoup(TocHTML,'html.parser')
        chapter_title =soup.find('h1',id='workTitle').text
        # print(soup.find('h1',class_='workTitle'))

        # chapter_title = re.findall(
        #     '<p class="widget-episodeTitle js-vertical-composition-item">(.*?)<', TocHTML)[0]
        return chapter_title

    def parseOnlineChapterList(self, html) -> list:
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup.find_all("a", "widget-toc-chapter"))
        # print("end")
        soup = soup.find('div', "widget-toc-main")
        regex = str(self.code) + "/episodes/"
        # regex = '/episodes/">(?P<num>.*?)</a>'
        chapList = []
        if (soup is not None):
            chapList = soup.find_all(href=re.compile(regex))

            for i in range(0, len(chapList)):
                # list should contain links and not number because can't be found from relative way
                chapList[i] ='https://kakuyomu.jp' +  str(chapList[i].get('href'))
        self.onlineChapterList  = chapList
        return chapList

    def getChapterTitle(self, str): 
        chapter_title = re.findall(
            '<p class="widget-episodeTitle js-vertical-composition-item">(.*?)<', str)[0]
        return chapter_title
    
    def getChapter(self,chapter_num) ->Chapter:
        # workaround because of absolute kakyomu's absolute links
        chap =KakyomuChapter(self.onlineChapterList.index(chapter_num),chapter_num)
        chap.processChapter(self.headers)
        return chap



class N18SyosetuNovel(Novel):
    
    def __init__(self, novel):
        
        novel.setCode(novel.code[3:]) 
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
        self.site = 'https://novel18.syosetu.com'
        # SyosetuNovel.__init__(self,novel)
        super().__init__(novel.code, novel.titre, novel.keep_text_format)
        # self.cookie={'autologin':getCookies()}

    def processNovel(self):
        import http.cookiejar as cookielib
        import mechanize
        import sys
        print("sysosetu novel " + self.titre)
        print('last chapter: ' + str(self.getLastChapter()))

        url = self.site + '/%s/' % self.code
        print('accessing: ' + url)
        print()
        try:
            html = self.connectViaMechanize(url)
        except (mechanize.HTTPError,mechanize.URLError) as e:
            print('novel has been stopped')
            return ''


        if (self.getLastChapter() == 0):
            self.processTocResume(html)
        # get the number of chapters (solely for user feedback)
        online_chapter_list = re.findall(
            '<a href="/' + self.code + '/' + '(.*?)' + '/">', html, re.DOTALL)

        print('<href="/' + self.code + '/' + '(.*?)' + '/">')
        lastDL = self.getLastChapter()
        online_chapter_list = online_chapter_list[lastDL:]
        print("there are %d chapters to udpate" % len(online_chapter_list))
        print(online_chapter_list)

        for chapter_num in online_chapter_list:
            chap = self.processChapter(int(chapter_num))
            chap.createFile(self.dir + '/')

    def processTocResume(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        resume = soup.find("div", id="novel_ex")
        # resume=re.findall('<div id="novel_ex">'+'(.*?)'+'</div>',html,re.S)[0]
        if (resume is None):
            print("the novel has most likely been terminated")
        else:
            # self.cleanText(resume)
            string = 'novel title= ' + self.getNovelTitle(html) + '\n\n'
            resume.insert(0, string)
            self.createFile(0, 'TOC', resume)

    def processChapter(self, chapter_num):
        chapter = N18SyosetuChapter(self.code, chapter_num)
        chapter_html = self.connectViaMechanize(
            '%s/%s/%s/' % (self.site, self.code, chapter_num))
        chapter.setTitle(chapter.parseTitle(chapter_html))
        chapter.setContent(chapter.parseContent(chapter_html))
        return chapter

    def getNovelTitle(self, html=''):
        # https://novel18.syosetu.com/n8451sz/
        url = self.site + '/%s/' % self.code
        print('\naccessing: ' + url)
        # https://novel18.syosetu.com/n8451sz
        # cookies={'autologin':'1872412%3C%3E014ebbec6d4b5ba4b35b8b5853e19625f9e6bf77eb2609658c927a0a8b4989b6'}
        # cookies.update({'ASP.NET_SessionId':'to3210exzz4jerncygdnevl0'})
        # cookies.update({'ses':'qRtZF3-Wlg5ehnQXuig-X1'})
        # print(cookies['autologin'])

        if (html == ''):
            html = self.connectViaMechanize(url)
        import sys
        writer = re.findall(r'<p class="novel_title">(.*?)</p>', html)
        # print(writer)
        return writer[0]

    def __createFile__(self, chapterNumber, chapter_title, chapter_content):
        chapter_title = checkFileName(chapter_title)
        print('saving %s %s' % (chapterNumber, chapter_title))
        file = open('%s/%d_%s.txt' % (self.getDir(), chapterNumber,
                                      chapter_title), 'w+', encoding='utf-8')
        file.write(chapter_title + '\n')
        file.write(chapter_content)
        file.close()
        print('\n\n')

    def connectViaMechanize(self, url):
        import http.cookiejar as cookielib
        import mechanize

        print('beginning server cracking beep boop')
        br = mechanize.Browser()
        br.addheaders = [('User-agent', 'Firefox')]

        cj = cookielib.LWPCookieJar()
        # add a cookie to cookie jar
        # Cookie(version, name, value, port, port_specified, domain,
        # domain_specified, domain_initial_dot, path, path_specified,
        # secure, discard, comment, comment_url, rest)

        cj.set_cookie(cookielib.Cookie(0, 'over18', 'yes', '80', False, '.syosetu.com',
                                       True, False, '/', True, False, None, False, None, None, None))

        # autologinkey=str(self.cookie.get('autologin'))
        # cj.set_cookie(cookielib.Cookie(0, 'autologin', autologinkey, '80', False, '.syosetu.com',
        #    True, False, '/', True, False, None, False, None, None, None))

        # print(cj)
        br.set_handle_redirect(True)
        br.set_cookiejar(cj)
        print('accessing : ' + url)
        br.open(url)
        resp = br.response()
        content = resp.get_data()
        soup = BeautifulSoup(content, 'html.parser')
        # print(soup.prettify())
        return str(soup)


def getCookies():
    file = open('./file.config', 'r+', encoding='utf-8')
    line = searchNextLine(file, 'N18')
    line = searchNextLine(file, 'autologin')
    autologinkey = getCookieKey(line)
    print('key=' + autologinkey)
    file.close()
    return autologinkey


def getCookieKey(line):
    # will get the key of the line
    print(line)
    key = line[line.find(':') + 1:]
    key = key[key.find('"') + 1:]
    key = key[:key.find('"')]
    return key


def searchNextLine(file, str):
    line = file.readline()
    while line:
        print("{}".format(line.strip()))
        if (line.find(str) != -1):
            return line
        line = file.readline()
    return -1


def checkFileName(str):
    str = str.replace('?', '')
    str = str.replace('!', '')
    str = str.replace(':', '')
    str = str.replace('"', '')
    str = str.replace('\"', '')
    str = str.replace('*', '')
    str = str.replace('/', '')
    str = str.replace('\\', '')
    str = str.replace('|', '')
    str = str.replace('<', '')
    str = str.replace('>', '')
    str = str.replace('\t', '')
    str = str.replace('\u3000', '')
    str = str[:250 - len('./novel_list/')]
    return str

def checkFilePathLength(str):
    return str[:200]

class WuxiaWorldNovel(Novel):
    def __init__(self, Novel):
        self.site = 'https://www.wuxiaworld.com/novel/'
        # "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
        self.headers = {"user-agent": "test"}
        code = Novel.titre.replace(' ', '-')
        code = code.lower()
        Novel.code = code
        # novel.code = the-trash-of-count
        super(WuxiaWorldNovel, self).__init__(Novel.code, Novel.titre)

    def processNovel(self):
        print("WuxiaWorld novel " + self.titre)
        print('last chapter: ' + str(self.getLastChapter()))
        url = self.site + self.code
        print('accessing ' + url)

        chapterListDiv = '/novel/%s/(.*?)"' % self.code
        # rep=requests.get(url,headers=self.headers)
        # rep.encoding='utf-8'
        html = self.connectViaMechanize(url)
        chapList = re.findall(chapterListDiv, html, re.DOTALL)[2:]
        chapList = chapList[self.getLastChapter():]
        print()
        print("there are %d chapters to udpate" % len(chapList))
        print(chapList)
        print()
        for chap in chapList:  # last chapter = 0 at beginning
            self.setLastChapter(self.getLastChapter() + 1)
            chapter_url = url + '/' + chap
            print('chapter: ' + str(self.getLastChapter()) + '  ' + chapter_url)
            chapter = self.processChapter(chapter_url, self.getLastChapter())
            chapter.createFile(self.dir + '/')

    def processChapter(self, chapter_url, chapter_num):
        chapter = WuxiaWorldChapter(chapter_url, chapter_num)
        # chapter_rep=requests.get(chapter.getUrl(),headers=self.headers)
        # chapter_rep.encoding='utf-8'
        chapter_html = self.connectViaMechanize(chapter_url)
        chapter.getTitle(chapter_html)
        print(chapter.title)
        chapter.getContent(chapter_html)
        return chapter

    def connectViaMechanize(self, url):
        import http.cookiejar as cookielib
        from bs4 import BeautifulSoup
        import mechanize

        print('beginning server cracking beep boop')
        br = mechanize.Browser()
        br.addheaders = [('User-agent', 'Chrome')]

        cj = cookielib.LWPCookieJar()
        # add a cookie to cookie jar
        # Cookie(version, name, value, port, port_specified, domain,
        # domain_specified, domain_initial_dot, path, path_specified,
        # secure, discard, comment, comment_url, rest)

        cj.set_cookie(cookielib.Cookie(0, 'over18', 'yes', '80', False, '.syosetu.com',
                                       True, False, '/', True, False, None, False, None, None, None))

        # autologinkey=str(self.cookie.get('autologin'))
        # cj.set_cookie(cookielib.Cookie(0, 'autologin', autologinkey, '80', False, '.syosetu.com',
        #    True, False, '/', True, False, None, False, None, None, None))

        # print(cj)
        br.set_handle_redirect(True)
        br.set_cookiejar(cj)
        print('accessing : ' + url)
        br.open(url)
        resp = br.response()
        content = resp.get_data()
        soup = BeautifulSoup(content, 'html.parser')
        return str(soup)

class NovelPia(Novel):
    def __init__(self, novel):
        super().__init__(novel.code, novel.titre, novel.keep_text_format)

    def setUrl(self):
        self.url = 'https://novelpia.com/novel//%s'%self.code

    def fetchTOCPage(self):
        from requests_html import HTMLSession
        session = HTMLSession()
        r = session.get(self.url)
        r.html.render()
        print(r.html.text)
        # print(r.html.find('div'))

        # list = r.html.find('#episode_list').text
        # print(list)


    def parseOnlineChapterList(self, html) -> list:
        # print(html)
        return super().parseOnlineChapterList(html)
    def parseTitle(self, TocHTML) -> str:
        return super().parseTitle(TocHTML)
    def parseTocResume(self, html=''):
        return super().parseTocResume(html)
    
    