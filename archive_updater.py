# coding: utf-8
import os
import sys
cwd=os.getcwd()
sys.path.insert(1,cwd+'\\src')

import Downloaders


def updateArchive():
    for novel_directory in os.listdir('./novel_list'):
        print()
        code=novel_directory.find(' ')
        novel_name=novel_directory[code:]
        code=novel_directory[:code]
        #here we got the novel code and our folder name

        #let's change the fetching process behaviour following the site it's hosted on
        novel=Downloaders.Novel(code,novel_name)
        novel=novel.updateObject()
        if(novel==0):
            print(novel_directory+' couldnt be updated')
            continue
        #now we fetch the local chapters and get the last chapter stored
        chapter_list=os.listdir('./novel_list/%s'%novel_directory)
        last_downloaded=0
        for chap in chapter_list:
            n=chap.find('_')
            tmp=chap[:n]
            tmp=int(tmp)
            if(last_downloaded<tmp):
                last_downloaded=tmp
        novel.setLastChapter(last_downloaded)
        #now that we have the number of the last chapter and the novel code
        #let's update the archive

        novel.setDir('novel_list\\'+code+novel_name)
        novel.processNovel()




def getInputFile():

    inputfile=open('input.txt','r+', encoding='utf-8')
    line=inputfile.readline()
    cnt=0
    novel_list=[]
    while line:
        print("{}".format(line.strip()))
        separator=line.find(';')
        code=line[:separator]
        novel_name=line[separator+1:len(line)-1] #delete carriage return
        novel_list.append([code,novel_name])
        line = inputfile.readline()
    inputfile.close()
    #print('list= ')

    # novel_list[]= [code,name]
    #print(novel_list)
    return novel_list





def download():
    novel_list=getInputFile()
    for novel_info in novel_list:
        code=novel_info[0]
        if code=='':
            continue

        name=novel_info[1]
        #print('i '+name)

        novel=Downloaders.Novel(code,name)
        novel=novel.updateObject()
        dir=''
        if (name==''):
            dir='./novel_list/'
            name=novel.getNovelTitle()
            print(name)
            dir+=code+' '+name
            print(dir)
        else:
            dir='./novel_list/'+code+' '+name
        dirlist=os.listdir('./novel_list/')
        if code+' '+name not in dirlist:
            os.mkdir('%s'%dir)

        print("dir=  "+dir)

        novel.setDir(dir)
        novel.setLastChapter(0)
        novel.processNovel()



type=''
for arg in sys.argv:
    type=arg
    print(arg)

updateInput='u'
downloadInput='d'


if(type=='' or type == 'archive_updater.py'):
    print('el ye')
    input=input("update archive (%s) or download (%s) ?  "%(updateInput,downloadInput))
    if (input==updateInput):
        updateArchive()
    elif (input==downloadInput):
        download()

if(type==updateInput):
    updateArchive()

if(type==downloadInput):
    download()
