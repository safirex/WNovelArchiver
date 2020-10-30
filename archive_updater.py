# coding: utf-8
import os
import sys

cwd=os.getcwd()
sys.path.insert(1,cwd+'\\src')
import tkinter

import Downloaders
import SysTray

def archiveUpdate():
    for novel_folder in os.listdir('./novel_list'):
        print()
        code=novel_folder.find(' ')
        novel_name=novel_folder[code:]
        code=novel_folder[:code]
        #here we got the novel code and our folder name

        #let's change the fetching process following the site it's hosted on
        novel=Downloaders.Novel(code,novel_name)
        novel=novel.updateObject()
        if(novel==0):
            print(novel_folder+' couldnt be updated because errored')
            continue

        #now we fetch the local chapters and determine the last chapter stored
        chapter_list=os.listdir('./novel_list/%s'%novel_folder)
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
        novel.setDir('./novel_list/'+code+novel_name)
        novel.processNovel()


def archiveFullUpdate():
    for novel_folder in os.listdir('./novel_list'):
        print()
        code=novel_folder.find(' ')
        novel_name=novel_folder[code:]
        code=novel_folder[:code]
        #here we got the novel code and our folder name

        #let's change the fetching process behaviour following the site it's hosted on
        novel=Downloaders.Novel(code,novel_name)
        novel=novel.updateObject()
        if(novel==0):
            print(novel_folder+' couldnt be updated')
            continue
        #now we fetch the local chapters and get the last chapter stored

        chapter_list=os.listdir('./novel_list/%s'%novel_folder)
        novel.setDir('./novel_list/'+code+novel_name)

        last_downloaded=0
        taille=len(chapter_list)
        code_list=[]
        for nov in chapter_list:
            chapter_code=nov.find('_')
            chapter_code=nov[:chapter_code]
            code_list.append(chapter_code)
            if(int(last_downloaded)<int(chapter_code)):
                last_downloaded=chapter_code
        print(last_downloaded)
        print(code_list)
        for i in range(0,int(last_downloaded)):

            if '%s'%i not in code_list:
                print('no '+str(i))
                if int(i) == 0 and isinstance(novel,Downloaders.SyosetuNovel) :
                    novel.processTocResume()
                    continue
                elif isinstance(novel,Downloaders.SyosetuNovel) :
                    novel.setLastChapter(int(i)) #work around cause conception is shit
                    chap=int(i)
                    novel.processChapter(chap)
                    continue
        novel.setLastChapter(int(last_downloaded))
        #now that we have the number of the last chapter and the novel code
        #let's update the archive
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
        if(novel==0):
            continue
        dir=''
        if (name==''):
            dir='./novel_list/'
            name=novel.getNovelTitle()
            name=Downloaders.checkTitle(name)
            print(name)
            dir+=code+' '+name
            print(dir)
        else:
            name=Downloaders.checkTitle(name)
            dir='./novel_list/'+code+' '+name
        dirlist=os.listdir('./novel_list/')
        bool='false'
        for file in dirlist:

            if (file[:7]==code):
                bool=file
        if bool!='false':
            print(bool[:25]+'... \tfolder already exists')
            continue

        if code+' '+name not in dirlist:
            os.mkdir('%s'%dir)
        else:
            print(code+' '+name+' folder already imported, update to keep up with site')
            continue

        print("dir=  "+dir)
        #dir='./novel_list/'+code+' '+name
        novel.setDir(dir)
        novel.setLastChapter(0)
        novel.processNovel()

def getFolderStatus():
    dir='./novel_list'
    statusList=[]
    for novel_folder in os.listdir(dir):
        code=novel_folder.find(' ')
        if code==-1:
            print(code)
            continue
        novel_name=novel_folder[code:]
        code=novel_folder[:code]

        novel=Downloaders.Novel(code,novel_name)
        lastchap=0
        for file in os.listdir(dir+'/'+novel_folder):
            chapnum=file.find('_')
            chapnum=int(file[:chapnum])
            if(chapnum>lastchap):
                lastchap=chapnum
        statusList.append([code,lastchap,novel_name])
        print('%s %s %s'%(code,lastchap,novel_name))
    enterInCSV(dir+'/status.csv',statusList)


def enterInCSV(filename,tab):
    file = open(filename, 'w+', encoding='utf-8')
    for line in tab:
        file.write('%1s %1s %2s\n'%(line[0],line[1],line[2]))
    file.close()



def compressNovelDirectory(novelDirectory,outputDir):
    import zipfile
    novelname=novelDirectory[novelDirectory.rfind('/')+1:]
    outputZipName=outputDir+'/'+novelname+'.zip'
    zipf = zipfile.ZipFile(outputZipName, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(novelDirectory):
        for file in files:
            zipf.write(os.path.join(root, file))
    print()
    zipf.close()

def compressAll(regex='',outputDir=''):
    if (outputDir==''):
        dirlist=os.listdir('./')
        print(dirlist)
        outputDir='./zip'
        if 'zip' not in dirlist :
            os.mkdir('zip')
    dir='./novel_list'
    DirToCompress=[]
    for novel_folder in os.listdir(dir):
        if novel_folder.find(regex)!=-1:
            DirToCompress.append(novel_folder)

    for subdir in DirToCompress:
        print('done at '+str(DirToCompress.index(subdir))+' on '+str(len(DirToCompress)))
        if(subdir.find('.')==-1):
            compressNovelDirectory(dir+'/'+subdir,outputDir)
    return(DirToCompress)


def background():
    import subprocess
    subprocess.Popen("archive_updater.py launchTrayMode")



def backgroundExe():
    import pystray


    from SysTray import setup
    SysTray.setup()

    def localDownload(systray='0'):
        download()
    def localUpdate(systray='0'):
        archiveUpdate()

    #image=create_image()
    #menu = (item('download', download), item('update', archiveUpdate))
    #icon = pystray.Icon("name", image, "title", menu)
    #icon.run()
    #icon.icon = create_image()

### background call
def backgroundExeinfi():
    from infi.systray import SysTrayIcon
    import asyncio
    import threading
    async def say_hello(systray):
        print("Hello, World!")
    def localDownload(systray='0'):
        download()
    def localUpdate(systray='0'):
        archiveUpdate()

        #x = threading.Thread(target=thread_function, args=(1,))
        #x.start()
        #x.join()


    print("test")
    print ('Hello, World!')
    menu_options = (
        ("Say Hello", None, say_hello),
        ('Download',None,localDownload),
        ('Update',None,localUpdate)
        )
    systray = SysTrayIcon("icon.ico", "Example tray icon", menu_options)
    systray.start()
