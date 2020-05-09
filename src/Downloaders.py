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

    def getNovelTitle(self) -> str:
        """"fetch the novel title from the TOC page"""
        pass


    #will instanciate an object depending of the code
    def updateObject(self):
        if (len(self.code)==7 and self.code.find('n')==0):
            return SyosetuNovel(self)
        elif(len(self.code)==len('1177354054888541019')):
            return KakuyomuNovel(self)
        elif(len(self.code)==10 and self.code.find('n18')==0):
            return N18SyosetuNovel(self)
        else:
            return 0





    def createFile(self,chapterNumber,chapter_title,chapter_content):
        chapter_title=checkTitle(chapter_title)
        print('saving '+chapter_title)
        file = open('%s/%d_%s.txt'%(self.getDir(),chapterNumber,chapter_title), 'w+', encoding='utf-8')
        file.write(chapter_title+'\n')
        file.write(chapter_content)
        file.close()
        print('\n\n')

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
        self.site='https://ncode.syosetu.com/'
        self.headers={"user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
        super().__init__(Novel.code,Novel.titre)

    def processNovel(self):
        print("sysosetu novel "+self.titre)
        print('last chapter: '+str(self.getLastChapter()))

        url='https://ncode.syosetu.com/%s/'%self.code
        headers = self.headers
        print('accessing: '+url)
        print()
        rep=requests.get(url,headers=headers)
        rep.encoding='utf-8'
        html=rep.text
        if(self.getLastChapter()==0):
            self.processTocResumelight(html)

        #get the number of chapters (solely for user feedback)
        online_chapter_list=re.findall(r'<a href="/'+self.code+'/'+'(.*?)'+'/">.*?</a>',html,re.S)

    #get the chapters url
        #chapter_list=re.findall(r'<a href="/'+self.code+'/'+'.*?'+'/">.*?</a>',html,re.S)
        lastDL=self.getLastChapter()
        online_chapter_list=online_chapter_list[lastDL:]
        #chapter_list=chapter_list[lastDL:]
        print("there are %d chapters to udpate"%len(online_chapter_list))
        print(online_chapter_list)

        #chapter_list=re.findall(r'<a href="(.*?)">(.*?)<',str(chapter_list))
        #i=lastDL+1
        for chapter_num in online_chapter_list:
            chap=self.processChapter(int(chapter_num))
            chap.createFile(self.dir+'/')

    def processTocResumelight(self,html):
        print(html)
        resume=re.findall('<div id="novel_ex">'+'(.*?)'+'</div>',html,re.S)[0]
        resume=self.cleanText(resume)
        title='novel title= '+self.getNovelTitle()
        resume=title+'\n\n'+resume
        self.createFile(0,'TOC',resume)

    def processTocResume(self):
        url='https://ncode.syosetu.com/%s/'%self.code
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
        rep=requests.get(url,headers=headers)
        rep.encoding='utf-8'
        html=rep.text
        resume=re.findall('<div id="novel_ex">'+'(.*?)'+'</div>',html,re.S)[0]
        resume=self.cleanText(resume)
        title='novel title= '+self.getNovelTitle()
        resume=title+'\n\n'+resume
        self.createFile(0,'TOC',resume)

    def processChapter(self,chapter_num):
        chapter=Chapters.SyosetuChapter(self.code,chapter_num)
        chapter_rep=requests.get(chapter.getUrl(),headers=self.headers)
        chapter_rep.encoding='utf-8'
        chapter_html=chapter_rep.text
        title=chapter.getTitle(chapter_html)
        content=chapter.getContent(chapter_html)
        return chapter
        #self.createFile(i,chapter_title,chapter_content)
        #self.setLastChapter(i)



    def cleanText(self,chapter_content):
        chapter_content = chapter_content.replace('</p>','\r\n')
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

    def validateTitle(self,title):
        rstr = r"[\/\\\:\*\?\"\<\>\|]"
        new_title = re.sub(rstr, "_", title)
        return new_title

    def getNovelTitle(self):
        url='https://ncode.syosetu.com/%s/'%self.code
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
        print('accessing: '+url)
        print()
        rep=requests.get(url,headers=headers)
        rep.encoding='utf-8'
        html=rep.text

        writer=re.findall(r'<p class="novel_title">(.*?)</p>',html,re.S)
        print('title = ')
        print(writer)
        return writer[0]

class KakuyomuNovel(Novel):
    def __init__(self,Novel):
        super().__init__(Novel.code,Novel.titre)

    def getChapterTitle(self,str):
        chapter_title=re.findall('<p class="widget-episodeTitle js-vertical-composition-item">(.*?)<',str)[0]
        return chapter_title



    def processNovel(self):
        print("Kakuyomu novel "+self.titre)
        print('last chapter: '+str(self.getLastChapter()))
        url='https://kakuyomu.jp/works/%s'%self.code
        print('accessing '+url)
        chapterListDiv='/works/%s/episodes/(.*?)"'%self.code
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
        rep=requests.get(url,headers=headers)
        rep.encoding='utf-8'
        html=rep.text
        chapList=re.findall(chapterListDiv,html,re.DOTALL)[1:]
        chapList=chapList[self.getLastChapter():]
        print()
        print("there are %d chapters to udpate"%len(chapList))
        print(chapList)
        print()
        for chap in chapList: #last chapter = 0 at beginning
            self.setLastChapter(self.getLastChapter()+1)
            chapter_url=url+'/episodes/'+chap
            print('chapter: '+str(self.getLastChapter())+'  '+chapter_url)
            self.processChapter(chapter_url)


    def processChapter(self,chapter_url):
        rep=requests.get(chapter_url)#,headers=headers)
        html=rep.text
        chapter_title=self.getChapterTitle(html)
        print(chapter_title)
        content=re.findall('<p id="p.*">(.*?)</p>',html)
        contentUPDATED=[]
        for sentence in content:
            sentence = sentence.replace('<br />','\n')
            sentence = sentence.replace('<ruby>','')
            sentence = sentence.replace('</ruby>','')
            sentence = sentence.replace('<rp>','')
            sentence = sentence.replace('</rp>','')
            sentence = sentence.replace('<rt>','')
            sentence = sentence.replace('</rt>','')
            sentence = sentence.replace('<rb>','')
            #signal character superpose
            sentence = sentence.replace('</rb>','//')
            sentence += '\n'
            contentUPDATED.append(sentence)
        self.createFile(chapter_title,contentUPDATED,chapter_url)


    def createFile(self,chapter_title,chapter_content,chapter_url):
        chapter_title=checkTitle(chapter_title)
        file = open('%s/%d_%s.txt'%(self.getDir(),self.getLastChapter(),chapter_title), 'w+', encoding='utf-8')
        file.write(chapter_url+'\n')
        file.write(chapter_title+'\n')
        for sentence in chapter_content:
            file.write(sentence)
        file.close()

    def getNovelTitle(self):
        titlediv='<h1 id="workTitle"><a href="/works/%s">'%self.code
        url='https://kakuyomu.jp/works/%s'%self.code
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
        rep=requests.get(url,headers=headers)
        rep.encoding='utf-8'
        html=rep.text
        titlediv1=html.find(titlediv)+len(titlediv)
        endTitleDiv=html[titlediv1:].find('</a>')+titlediv1
        return html[titlediv1:endTitleDiv]


class N18SyosetuNovel(Novel):
    def __init__(self,novel):
        super().__init__(novel.code[3:],novel.titre)
        self.site='https://novel18.syosetu.com'
    def createFile(self,chapterNumber,chapter_title,chapter_content):
        print(self.dir)
        super.createFile(chapterNumber,chapter_title,chapter_content)

    def processNovel(self):
        print("sysosetu novel "+self.titre)
        print('last chapter: '+str(self.getLastChapter()))

        url=self.site+'/%s/'%self.code
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
        print('accessing: '+url)
        print()
        print(url)
        #https://novel18.syosetu.com/n8321do/
        #autologin,
        cookies={'autologin':'1872412%3C%3E014ebbec6d4b5ba4b35b8b5853e19625f9e6bf77eb2609658c927a0a8b4989b6'}
        rep=requests.get(url,cookies=cookies)#,headers=headers)
        rep.encoding='utf-8'
        html=rep.text
        #print(html)
        print(self.code)
        print(rep.json)
        #get the number of chapters (solely for user feedback)
        online_chapter_list=re.findall('<p id="L'+'(.*?)'+'">',html,re.DOTALL)
        #get the chapters url
        chapter_list=re.findall(r'<p id="L'+'.*?'+'">'+'(.*?)'+'</p>',html,re.S)

        print(online_chapter_list)
        lastDL=self.getLastChapter()
        online_chapter_list=online_chapter_list[lastDL:]
        chapter_list=chapter_list[lastDL:]

        print("there are %d chapters to udpate"%len(online_chapter_list))
        print(online_chapter_list)

        #chapter_list=re.findall(r'<a href="(.*?)">(.*?)<',str(chapter_list))
        #i=lastDL+1
        for chapter_link in chapter_list:
            url+='/'    #syosetu/code/
            chapter_link=[url,chapter_link]
            #self.processChapter(chapter_link,headers)

    def processChapter(self,chapter_link,headers):
        i=self.getLastChapter()+1

        chapter_title=chapter_link[1]
        chapter_url='%s%s/'%(chapter_link[0],i)
        print(chapter_url)
        chapter_rep=requests.get(chapter_url,headers=headers)
        chapter_rep.encoding='utf-8'
        chapter_html=chapter_rep.text
        print(chapter_html)
        print(re.findall(r'<div id="novel_honbun" class="novel_view">(.*?)</div>',chapter_html,re.S))


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



    def getNovelTitle(self):
        #https://novel18.syosetu.com/n8451sz/
         url=self.site+'/%s/'%self.code
         headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
         print('accessing: '+url)
         print()
         print(url)
         #https://novel18.syosetu.com/n8451sz
         #cookies={'autologin':'1872412%3C%3E014ebbec6d4b5ba4b35b8b5853e19625f9e6bf77eb2609658c927a0a8b4989b6'}
         #cookies.update({'ASP.NET_SessionId':'to3210exzz4jerncygdnevl0'})
         #cookies.update({'ses':'qRtZF3-Wlg5ehnQXuig-X1'})
         #print(cookies['autologin'])

        


         rep=requests.get(url,cookies=cookies)#,headers=headers)
         rep.encoding='utf-8'
         html=rep.text
         writer=re.findall(r'<p class="novel_title">(.*?)</p>',html)
         print(writer)
         return writer[0]

    def connectViaRequests():


    def connectViaMechanize():


def checkTitle(str):
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




def testToc():
    x=Novel('n7244bl','')
    x=x.updateObject()
    x.setDir('../novel_list/n7244bl Modern Weapons Cheat in Another World')
    x.processTOC()

def testReMethodes():
    x=Novel('n8577dn','')
    x=x.updateObject()
    print(x)
    chap=x.processChapterNew(50)
    chap.createFile('./')
    #print(chap)



def test():
    import os

    x=Novel('n18n8321do','')

    x=x.updateObject()
    print(x)
    name=x.getNovelTitle()
    print(name)
    dir=x.code+' '+name
    print(dir)


    print("dir=  "+dir)
            #dir='./novel_list/'+code+' '+name
    x.setDir(dir)
    x.setLastChapter(0)
    x.processNovel()

#testToc()
import re
import Chapters
test()
