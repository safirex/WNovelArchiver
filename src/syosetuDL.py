# coding: utf-8
import requests
import re
import locale
import ctypes
import sys

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title

def createFile(title,i,chapter_title,chapter_content):
     #写入
    file = open('%s\%d_%s.txt'%(title,i,chapter_title), 'w+', encoding='utf-8')
    i+=1#章节自增
    file.write(chapter_title)
    file.write(chapter_content)
    file.close()


def processSyosetuNovel(code,novel_name,lastDL):
    url='https://ncode.syosetu.com/%s/'%code
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
    print('accessing: '+url)
    rep=requests.get(url,headers=headers)
    rep.encoding='utf-8'
    html=rep.text
    #get the number of chapters (solely for user feedback)
    online_chapter_list=re.findall(r'<a href="/'+code+'/'+'(.*?)'+'/">.*?</a>',html,re.S)
    #get the chapters url
    chapter_list=re.findall(r'<a href="/'+code+'/'+'.*?'+'/">.*?</a>',html,re.S)

    online_chapter_list=online_chapter_list[lastDL:]
    chapter_list=chapter_list[lastDL:]
    print("there are %d chapters to udpate"%len(online_chapter_list))
    print(online_chapter_list)

    chapter_list=re.findall(r'<a href="(.*?)">(.*?)<',str(chapter_list))
    
    #here begins the chapters handling
    i=lastDL+1
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
        createFile(novel_name,i,chapter_title,chapter_content)
        i+=1
