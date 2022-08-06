import re
from pandas import array
import requests
from bs4 import BeautifulSoup



def checkFileName(str) -> str:
    """ make sure the title is conform to windows url settings (260 char max)"""
    str=str.replace('?','')
    str=str.replace('!','')
    str=str.replace(':','')
    str=str.replace('"','')
    str=str.replace('*','')
    str=str.replace('/','')
    str=str.replace('\\','')
    str=str.replace('|','')
    str=str.replace('<','')
    str=str.replace('>','')
    str=str[:250-len('./novel_list/')]
    return str

class Chapter():
    def __init__(self,num,url=''):
        self.num=num
        self.content=[]
        self.title=""
        self.url=url
        self.setUrl()

    def setContent(self,content):
        self.content=content

    def setTitle(self,Title):
        self.title=Title

    def setUrl(self) -> str:
        """"will define Url chapter"""
        pass
    def getUrl(self):
        return self.url

    def processChapter(self,headers):
        chapter_rep = requests.get(self.getUrl(), headers=headers)
        chapter_rep.encoding = 'utf-8'
        chapter_html = chapter_rep.text
        self.setTitle(self.parseTitle(chapter_html))
        self.setContent(self.parseContent(chapter_html))
        
        
    def parseTitle(self,html) -> str:
        """returns the title of the page"""
        pass
    
    def parseContent(self,html):
        """returns the content of the page"""
        pass
    
    
    def validateTitle(self,title):
        rstr = r"[\/\\\:\*\?\"\<\>\|]"
        new_title = re.sub(rstr, "_", title)
        return new_title

    def cleanText(self,chapter_content):
        chapter_content = chapter_content.replace('</p>','\r\n')
        chapter_content = chapter_content.replace('<br />', '')
        chapter_content = chapter_content.replace('<br/>', '')
        chapter_content = chapter_content.replace('<rb>', '')
        chapter_content = chapter_content.replace('</rb>', '')
        chapter_content = chapter_content.replace('<rp>', '')
        chapter_content = chapter_content.replace('</rp>', '')
        chapter_content = chapter_content.replace('<rt>', '')
        chapter_content = chapter_content.replace('</rt>', '')
        chapter_content = chapter_content.replace('<ruby>', '')
        chapter_content = chapter_content.replace('</ruby>', '')
        return chapter_content


    def save(self,dir):
        pass

    def createFile(self,dir):
        chapter_title=checkFileName(self.title)
        print("titre"+chapter_title)
        print('saving '+str(self.num)+' '+chapter_title)
        file = open('%s/%s_%s.txt'%(dir,self.num,chapter_title), 'w+', encoding='utf-8')
        file.write(chapter_title+'\n')
        file.write(self.content)
        file.close()
        print('\n\n')
        


class KakyomuChapter(Chapter):
    def __init__(self,num,url):
        super().__init__(num,url)
        
    def setUrl(self) -> str:
        # self.url = 'https://kakuyomu.jp/works/%s/episodes/%s'%(self.novelNum,self.num)
        print("url = "+str(self.url))
        pass
    
    def parseTitle(self, html) -> str:
        print("parsing title")
        chapter_title = re.findall(
            '<p class="widget-episodeTitle js-vertical-composition-item">(.*?)<', html)[0]
        print("title found = "+str(chapter_title))
        return chapter_title
    
    def parseContent(self, html,keep_text_format=False):
        soup = BeautifulSoup(html, 'html.parser')
        soup = soup.find('div', 'widget-episodeBody')
        content = []
        if (keep_text_format == False):
            content = soup.getText()
        else:
            content = str(soup)
        return content
    
class SyosetuChapter(Chapter):
    def __init__(self,novelNum,num):
        self.novelNum=novelNum
        super(SyosetuChapter,self).__init__(num)
        self.setUrl()

    def setUrl(self):
        self.url='https://ncode.syosetu.com/%s/%s/'%(self.novelNum,self.num)

    def parseTitle(self, html) -> str:
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find("p","novel_subtitle").text
        return title
    
    def parseContent(self,html):
        chapter_content=re.findall(r'<div id="novel_honbun" class="novel_view">(.*?)</div>',html,re.S)[0]
        replacething=re.findall(r'<p id=' + '.*?' + '>', chapter_content)
        for y in replacething:
            chapter_content=chapter_content.replace(y,'')
        chapter_content=self.cleanText(chapter_content)
        self.setContent(chapter_content)
        return chapter_content

class N18SyosetuChapter(SyosetuChapter,Chapter):
    def __init__(self,novelNum,num):
        super(N18SyosetuChapter,self).__init__(novelNum,num)
        self.setUrl()

    def setUrl(self):
        self.url='https://novel18.syosetu.com/%s/%s/'%(self.novelNum,self.num)

    def getContent(self,html):
        chapter_content=re.findall(r'<div class="novel_view" id="novel_honbun">(.*?)</div>',html,re.S)[0]
        replacething=re.findall(r'<p id=' + '.*?' + '>', chapter_content)
        for y in replacething:
            chapter_content=chapter_content.replace(y,'')
        chapter_content=self.cleanText(chapter_content)
        self.setContent(chapter_content)
        return chapter_content

    def createFile(self,dir):
        chapter_title=checkFileName(self.title)

        print('saving '+str(self.num)+' '+chapter_title)
        file = open('%s/%d_%s.txt'%(dir,self.num,chapter_title), 'w+', encoding='utf-8')
        file.write(chapter_title+'\n')
        file.write(self.content)
        file.close()
        print('\n\n')

class WuxiaWorldChapter(Chapter):
    
    def __init__(self,chapterUrl,num):
        super(WuxiaWorldChapter,self).__init__(num)
        self.setUrl(chapterUrl)

    def setUrl(self,url):
        self.url=url

    def getTitle(self,html):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html)
        title=''
        for h in soup.find_all('title'):
            title=h.string

        #title=re.findall('<h4 class="" (*<>) (.*?)</h4>',html)[0]
        replacething=re.findall('_u3000',title)
        for y in replacething:
            chapter_title=chapter_title.replace(y,' ')
        title=self.validateTitle(title)
        self.setTitle(title)
        return title

    def getContent(self,html):
        from bs4 import BeautifulSoup

        #can be made better with soup.id["chapter-content"]
        soup = BeautifulSoup(html)
        chapter_content=''
        for div in soup.find_all('div'):
            id=div.get("id")
            if(id!=None):
                if(id=="chapter-content"):
                    chapter_content=div.text
                    break
        self.setContent(chapter_content)
        return chapter_content