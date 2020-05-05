# coding: utf-8
import requests
#正则表达式模块
import re
import locale
import ctypes
import os
import platform

def createFile(title,i,chapter_title,chapter_content):
     #写入
    file = open('%s\%d_%s.txt'%(title,i,chapter_title), 'w+', encoding='utf-8')
    i+=1#章节自增
    file.write(chapter_title)
    file.write(chapter_content)
    file.close()


def batchDL(title,num):
    global html
    #返回作者
    print(url1)
    writer=re.findall(r'<div class="novel_writername">(.*?)</div>',html,re.S)[0]
    print(writer[0])
    #正则匹配
    #返回匹配链接
    dl=re.findall(r'<a href="/'+url1+'/'+'.*?'+'/">.*?</a>',html,re.S)
    print(dl[0])
    dirlist=os.listdir(os.getcwd())
    if title not in dirlist:
        os.mkdir('%s'%title)

    #search all chapters from num-1 to max
    #返回需要链接
    chapter_list=re.findall(r'<a href="(.*?)">(.*?)<',str(dl))[num-1:]
    print(chapter_list)
    #章节提示以防乱序
    i=num
    chapter_list = chapter_list
    for x in chapter_list:
        chapter_title=x[1]
        chapter_url='https://ncode.syosetu.com%s'%x[0]
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

        chapter_title=validateTitle(chapter_title)
        replacething=re.findall('_u3000', chapter_title)
        for y in replacething:
            chapter_title=chapter_title.replace(y,' ')
        print(chapter_title)
        createFile(title,i,chapter_title,chapter_content)
        i+=1


#标题规范化
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title


def getLangage():
    windll = ctypes.windll.kernel32
    lg=locale.windows_locale[ windll.GetUserDefaultUILanguage()]
    if(lg.find('zh')==-1):
        return 'english'
    else:
        return 'chinese'





headers={}
html=''
def processNovel(url1,dltype):
    global html
    global headers
    #the url of the novel TOC
    url='https://ncode.syosetu.com/%s/'%url1
    print(url)
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
    #模拟 http
    rep=requests.get(url,headers=headers)
    #目标小说主页源码
    rep.encoding='utf-8'
    html=rep.text

    #返回title
    title=re.findall(r'<p class="novel_title">(.*?)</p>',html)
    #标题规范化
    title=validateTitle(title[0])
    print(title)
    title=url1+" "+title

    #define the type of download
    if (dltype==1):
        batchDL(title,1)
    else:
        ddlType=input('batch [b]/batch from chapter [bf]')

        if (ddlType=='b'):
            batchDL(title,1)
            return 0
        elif (ddlType=='bf'):
            chapnum=int(input('chapter (min=1):'))
            batchDL(title,chapnum)
            return 0
        else:
            input("try again")
            return -1















if(platform.system()=='Windows'):
    print("is windows")
    language=getLangage()  #windows dependent (maybe)

if(language=='english'):
    txtUrl1=' input the novel TOC page number or type input '
else:
    txtUrl1='请输入小说url编号：'

inputfile=open('input.txt','r+', encoding='utf-8')
inputlist=inputfile.read()
inputfile.close()
length=len(inputlist)
i=0
novelTab=[]
while i<length :
    print(inputlist[i:i+7])
    listindex=i+7
    novelTab.append(inputlist[i:listindex])
    i+=8 #count the carriage return char

#目标小说URL

url1=input(txtUrl1)

if (url1=='input'):

    print('processing input.txt')
    for Novel in novelTab:
        url1=Novel
        print(len(Novel))
        processNovel(Novel,1)
else:
    print(len(url1))
    print(str(type(url1)))
    processNovel(url1,0)
