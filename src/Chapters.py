import re




def checkTitle(str):
    # make sure the title is conform to windows url settings (260 char max)
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
    def __init__(self,num):
        self.num=num
        self.content=[]
        self.title=''

    def setContent(self,content):
        self.content=content

    def setTitle(self,Title):
        self.title=Title

    def setUrl() -> str:
        """"will define Url chapter"""
        pass
    def getUrl(self):
        return self.url
    def validateTitle(self,title):
        rstr = r"[\/\\\:\*\?\"\<\>\|]"
        new_title = re.sub(rstr, "_", title)
        return new_title

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


    def createFile(self,dir):
        chapter_title=checkTitle(self.title)
        print('saving '+chapter_title)
        file = open('%s/%d_%s.txt'%(dir,self.num,chapter_title), 'w+', encoding='utf-8')
        file.write(chapter_title+'\n')
        file.write(self.content)
        file.close()
        print('\n\n')



class SyosetuChapter(Chapter):
    def __init__(self,novelNum,num):
        self.novelNum=novelNum
        super().__init__(num)
        self.setUrl()

    def setUrl(self):
        self.url='https://ncode.syosetu.com/%s/%s/'%(self.novelNum,self.num)

    def getTitle(self,html):
        title=re.findall('<p class="novel_subtitle">(.*?)</p>',html)[0]
        replacething=re.findall('_u3000',title)
        for y in replacething:
            chapter_title=chapter_title.replace(y,' ')
        title=self.validateTitle(title)
        self.setTitle(title)
        return title

    def getContent(self,html):
        chapter_content=re.findall(r'<div id="novel_honbun" class="novel_view">(.*?)</div>',html,re.S)[0]
        replacething=re.findall(r'<p id=' + '.*?' + '>', chapter_content)
        for y in replacething:
            chapter_content=chapter_content.replace(y,'')
        chapter_content=self.cleanText(chapter_content)
        self.setContent(chapter_content)
        return chapter_content
