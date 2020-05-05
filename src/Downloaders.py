# coding: utf-8
import requests
import re


class Novel:
    def __init__(self,codeNovel,titreNovel):
        self.code=codeNovel
        self.titre=titreNovel

    def download(self) -> str:
        """download chapter from site."""
        pass

    def processNovel(self) -> str:
        """"will process the html and download the chapter"""
        pass
    #will instanciate an object depending of the code
    def updateObject(self):
        if (len(self.code)==7 and self.code.find('n')==0):
            return SyosetuNovel(self)
        elif(len(self.code)>7):
            return KakyomuNovel(self)
        else:
            return 0

    def createFile(self,chapterNumber,chapter_title,chapter_content):
        file = open('%s\%d_%s.txt'%(self.getDir(),chapterNumber,chapter_title), 'w+', encoding='utf-8')
        file.write(chapter_title)
        file.write(chapter_content)
        file.close()

    def setLastChapter(self,chap):
        self.chap=chap
    def getLastChapter(self):
        return self.chap
    def setDir(self,dir):
        self.dir=dir
    def getDir(self):
        return self.dir
    def getTitle(self):
        return self.titre

class SyosetuNovel(Novel):
    def __init__(self,Novel):
        super().__init__(Novel.code,Novel.titre)
    def download(self):
        print("roar")
        return 'syos'

    def processNovel(self):
        print("sysosetu novel "+self.titre)
        print('last chapter: '+str(self.getLastChapter()))

        url='https://ncode.syosetu.com/%s/'%self.code
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
        print('accessing: '+url)
        print()
        rep=requests.get(url,headers=headers)
        rep.encoding='utf-8'
        html=rep.text

        #get the number of chapters (solely for user feedback)
        online_chapter_list=re.findall(r'<a href="/'+self.code+'/'+'(.*?)'+'/">.*?</a>',html,re.S)
        #get the chapters url
        chapter_list=re.findall(r'<a href="/'+self.code+'/'+'.*?'+'/">.*?</a>',html,re.S)

        lastDL=self.getLastChapter()
        online_chapter_list=online_chapter_list[lastDL:]
        chapter_list=chapter_list[lastDL:]

        print("there are %d chapters to udpate"%len(online_chapter_list))
        print(online_chapter_list)

        chapter_list=re.findall(r'<a href="(.*?)">(.*?)<',str(chapter_list))
        #i=lastDL+1
        for chapter_link in chapter_list:
            self.processChapter(chapter_link,headers)

    def processChapter(self,chapter_link,headers):
        i=self.getLastChapter()+1

        chapter_title=chapter_link[1]
        chapter_url='https://ncode.syosetu.com%s'%chapter_link[0]
        print(chapter_url)
        chapter_rep=requests.get(chapter_url,headers=headers)
        chapter_rep.encoding='utf-8'
        chapter_html=chapter_rep.text
        chapter_content=re.findall(r'<div id="novel_honbun" class="novel_view">(.*?)</div>',chapter_html,re.S)[0]
        replacething=re.findall(r'<p id=' + '.*?' + '>', chapter_content)
        for y in replacething:
            chapter_content=chapter_content.replace(y,'')
        chapter_content=chapter_content.replace('</p>','\r\n')
        chapter_content = chapter_content.replace('<br />', '')
        chapter_content = chapter_content.replace('<rb>', '')
        chapter_content = chapter_content.replace('</rb>', '')
        chapter_content = chapter_content.replace('<rp>', '')
        chapter_content = chapter_content.replace('</rp>', '')
        chapter_content = chapter_content.replace('<rt>', '')
        chapter_content = chapter_content.replace('</rt>', '')
        chapter_content = chapter_content.replace('<ruby>', '')
        chapter_content = chapter_content.replace('</ruby>', '')

        chapter_title=self.validateTitle(chapter_title)
        replacething=re.findall('_u3000', chapter_title)
        for y in replacething:
            chapter_title=chapter_title.replace(y,' ')
        print(chapter_title)
        self.createFile(i,chapter_title,chapter_content)
        self.setLastChapter(i)


    def validateTitle(self,title):
        rstr = r"[\/\\\:\*\?\"\<\>\|]"
        new_title = re.sub(rstr, "_", title)
        return new_title



class KakyomuNovel(Novel):
    def __init__(self,Novel):
        super().__init__(Novel.code,Novel.titre)
    def download(self):
        print("pas rora")
        return 'kaky'
