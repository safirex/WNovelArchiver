# coding: utf-8
import os
import sys
cwd=os.getcwd()
sys.path.insert(1,cwd+'\\src')

import Downloaders


def archiveUpdate(dirList=[]):
    if not dirList:
        dirList=os.listdir('./novel_list')


    for novel_folder in dirList:
        print()
        code=       novel_folder.find(' ')
        novel_name= novel_folder[code+1:]
        code=       novel_folder[:code]
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
        novel.setDir('./novel_list/'+novel_folder)
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
    novel_list=[]
    while line:
        print("{}".format(line.strip()))
        separator=line.find(';')
        code=line[:separator]
        upperLim=len(line)
        if('\n' in line[separator+1:upperLim]):
            upperLim=len(line)-1
        print(line[len(line)-1])
        novel_name=line[separator+1:upperLim] #delete carriage return
        novel_list.append([code,novel_name])
        line = inputfile.readline()
    inputfile.close()
    #print('list= ')

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
            print(code+' '+name+' folder already imported, update to fetch updates')
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
    for tab in os.walk(novelDirectory):
        for file in tab[2]:
            zipf.write(os.path.join(tab[0], file))
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



updateInput='u'
fullupdateInput='fu'
downloadInput='d'
statusInput='s'
compressInput='c'


def entree():
    type=''
    for arg in sys.argv:
        type=arg
        print(arg)

    if(type=='' or type == 'archive_updater.py'):
        print('el ye')
        input=input("update archive (%s) or download (%s) ?  "%(updateInput,downloadInput))
        if (input==updateInput):
            archiveUpdate()
        elif (input==downloadInput):
            download()
        elif (input==statusInput):
            getFolderStatus()
        elif (input==fullupdateInput):
            getFolderStatus()
    if(type==downloadInput):
        download()
    if(type==updateInput):
        archiveUpdate()
    if(type==statusInput):
        getFolderStatus()
    if(type==fullupdateInput):
        archiveFullUpdate()


def parser():
    import argparse
    parser = argparse.ArgumentParser(description=''' c to compress novels in zip\n
        d to download input.txt list
        s to update status.csv
        u to update novels''')
    parser.add_argument("mode",
        help="put the letter of argument c/d/s/u",
        type=str,default=argparse.SUPPRESS)

    parser.add_argument("-r", help="regex of entree for compression selection (select * containing regex)",
        type=str,default=argparse.SUPPRESS)
    parser.add_argument("-o", help="output directory (only works for compression)",
        type=str,default=argparse.SUPPRESS)
    

    args = parser.parse_args()
    print(args)
    if args.mode:
        if(args.mode==downloadInput):
            print("downloading")
            download()
        elif(args.mode==updateInput):
            archiveUpdate()
        elif(args.mode==statusInput):
            getFolderStatus()
        elif(args.mode==fullupdateInput):
            archiveFullUpdate()
        elif(args.mode==compressInput):
            print('compression')
            print(args)
            regex=''
            out=''
            if hasattr(args, 'r'):
                regex=args.r
            if hasattr(args, 'o'):
                out=args.o
            compressAll(regex,out)
        elif(args.mode=='t'):
            mylist=os.listdir('./novel_list')
            obje=[1]
            for obj in mylist:
                if(obj.find('wuxiaworld Trash of the Counts Family')!=-1):
                    obje[0]=obj
            archiveUpdate(obje)



parser()
