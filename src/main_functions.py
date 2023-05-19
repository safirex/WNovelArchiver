import os
import re
import logging
from typing import List

from src.Downloaders import *
import zipfile


factory = NovelFactory()

factory.registerObject( N18SyosetuNovel )
factory.registerObject( SyosetuNovel    )
factory.registerObject( KakuyomuNovel   )



def archiveUpdate(dirList=[],keep_text_format=False):
    if not dirList:
        dirList=os.listdir('./novel_list')
    print("list=")
    print(dirList)

    for novel_folder in dirList:
        print()
        novelInfo=getNovelInfoFromFolderName(novel_folder)
        #change the fetching process following the site it's hosted on
        novel = factory.getNovel(novelInfo[1],novelInfo[0], keep_text_format)
        #novel=Novel(novelInfo[1],novelInfo[0],keep_text_format)
        #novel=novel.updateObject()
        if(novel==0):
            print(novel_folder+' couldnt be updated because the code doesnt match known formats')
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
        print(type(novel))
        novel.processNovel()


def archiveFullUpdate(dirList=[],force=False):
    if not dirList:
        dirList=os.listdir('./novel_list')
    for novel_folder in dirList:
        print()
        NFs=getNovelInfoFromFolderName(novel_folder)
        novel_name=NFs[0]   #novel_folder[code:]
        code=NFs[1]         #novel_folder[:code]
        #here we got the novel code and our folder name

        #we adapt the fetching process behaviour following the site it's hosted on
        novel = factory.getNovel(code, novel_name, False)
        #novel=Novel(code,novel_name)
        #novel=novel.updateObject()
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

            if '%s'%i not in code_list or force==True:
                print('no '+str(i))
                if int(i) == 0 and isinstance(novel,SyosetuNovel) :
                    novel.processTocResume()
                    continue
                elif isinstance(novel,SyosetuNovel) :
                    novel.setLastChapter(int(i)) #work around cause conception is shit
                    chap=int(i)
                    novel.processChapter(chap)
                    continue
                #TODO:
                elif isinstance(novel,KakuyomuNovel):
                    novel.setLastChapter(last_downloaded)
                    novel.setDir('./novel_list/'+novel_folder)
                    novel.processNovel()
        novel.setLastChapter(int(last_downloaded))
        #now that we have the number of the last chapter and the novel code
        #let's update the archive
        novel.processNovel()



def getInputFile() -> List[str]:
    """return code and novel name from input.txt"""
    inputfile=open('input.txt','r+', encoding='utf-8')
    line=inputfile.readline()
    novel_list=[]
    while line:
        print("{}".format(line.strip()))
        separator=line.find(';')
        code=line[:separator]
        novel_name=line[separator+1:] #delete carriage return
        novel_name=novel_name.strip()
        novel_list.append([code,novel_name])
        line = inputfile.readline()
    inputfile.close()
    return novel_list


def getNovelInfoFromFolderName(folderName) :
    """return code and novel name from the local novel folder """
    code=       folderName.find(' ')
    novel_name= folderName[code+1:].strip()
    code=       folderName[:code]
    return [novel_name,code]




def download(keep_text_format=False):
    if('novel_list' not in os.listdir('.')):
        os.mkdir('novel_list')
    novel_list=getInputFile()
    for novel_info in novel_list:
        code=novel_info[0]
        if code=='':
            continue
        
        title=novel_info[1]
        #print('i '+title)
        
        print('Working on:', code, 'Title:', title, 'Keep Format:', keep_text_format)
        #novel=Novel(code,name,keep_text_format)
        #novel=novel.updateObject()
        novel = factory.getNovel(code, title, keep_text_format)
        if(novel==0):
            print(code,title,"doesn't match any defined novel")
            continue

        #detect if the novel has already been downloaded
        match=findNovel(code)
        if (len(match)>0):
            print(match[0][:25]+'... \t folder already exists')
            continue

        try:
            dir_path=''
            if (title==''):
                title=novel.getNovelTitle()

            title=checkFileName(title)
            print(title)
            dir_path='./novel_list/'+code+' '+title
            dir_path = checkFilePathLength(dir_path)
            
            if code+' '+title not in match:
                try :
                    os.mkdir('%s'%dir_path)
                except FileExistsError:
                    print("the folder already exists")
                    continue
            else:
                print(code+' '+title+' folder already imported, update to fetch updates')
                continue

            print("dir_path=  "+dir_path)
            
            #dir_path='./novel_list/'+code+' '+name
            novel.setDir(dir_path)
            novel.setLastChapter(0)
            novel.processNovel()
        except Exception as err:
            # log = logging.getLogger(__name__)
            # log.exception("")
            print("novel ",code," hasn't been downloaded" )
            raise(err)


def download_cli(userInput:str):
    novel_info = userInput.strip().split(';')
    if(len(novel_info)<2):
        novel_info.append('')
    title = novel_info[1]
    novel = factory.getNovel(novel_info[0], title, False)
    #novel=Novel(novel_info[0],novel_info[1])
    #novel=novel.updateObject()
    if(novel==0):
        return
    #detect if the novel has already been downloaded
    match=findNovel(novel.code)
    if (len(match)>0):
        print(match[0][:25]+'... \t folder already exists')
        return

    if (title==''):
        title=novel.getNovelTitle()
    
    title=checkFileName(title)
    print(title)
    path='./novel_list/'+novel.code+' '+title
    path = checkFilePathLength(path)
    
    if novel.code+' '+title not in match:
        try :
            os.mkdir('%s'%path)
        except FileExistsError:
            print("the folder already exists")
            return
    else:
        print(novel.code+' '+title+' folder already imported, update to fetch updates')
        return

    print("dir=  "+path)
    
    #path='./novel_list/'+code+' '+name
    novel.setDir(path)
    novel.setLastChapter(0)
    novel.processNovel()


def getFolderStatus():
    """register as csv every folder name and the number of chapter"""
    path='./novel_list'
    statusList=[]
    for novel_folder in os.listdir(path):
        code=novel_folder.find(' ')
        if code==-1:
            print(code)
            continue
        novel_name=novel_folder[code:]
        code=novel_folder[:code]
        lastchap=0
        for file in os.listdir(path+'/'+novel_folder):
            chapnum=file.find('_')
            chapnum=int(file[:chapnum])
            if(chapnum>lastchap):
                lastchap=chapnum
        statusList.append([code,lastchap,novel_name])
        print('%s %s %s'%(code,lastchap,novel_name))
    enterInCSV(path+'/status.csv',statusList)


def enterInCSV(filename,tab):
    """overwrite the file with tab content"""
    file = open(filename, 'w+', encoding='utf-8')
    for line in tab:
        file.write('%1s %1s %2s\n'%(line[0],line[1],line[2]))
    file.close()



def compressNovelDirectory(novelDirectory,parentFolder='./',outputDir='./'):
    novelname = novelDirectory[novelDirectory.rfind('/')+1 :]
    outputZipName = os.path.join(outputDir,novelname + '.zip')
    zipf = zipfile.ZipFile(outputZipName, 'w', zipfile.ZIP_DEFLATED)
    
    for tab in os.walk(parentFolder + novelDirectory):
        for file in tab[2]:
            folder_name = str(tab[0]).replace("./novel_list/","")
            zipf.write( os.path.join(tab[0], file),
                        os.path.join(folder_name,file)
                       )
    print()
    zipf.close()


def compressAll(regex='',outputDir=''):
    """compress in zip format every novel folder found"""
    if (outputDir==''):
        dirlist=os.listdir('./')
        print(dirlist)
        outputDir='./zip'
        if 'zip' not in dirlist :
            os.mkdir('zip')
    path='./novel_list'
    DirToCompress=[]
    for novel_folder in os.listdir(path):
        if novel_folder.find(regex)!=-1:
            DirToCompress.append(novel_folder)

    for subdir in DirToCompress:
        print('done at', DirToCompress.index(subdir)+1, 'on', len(DirToCompress))
        if(subdir.find('.')==-1):
            compressNovelDirectory(subdir,path+'/',outputDir)
    return(DirToCompress)


def findNovel(regex,path='./novel_list'):
    """find in the novels folder every regex match"""
    regex=  re.compile(regex)
    novel_folders=os.listdir(path)
    liste=list(filter(regex.match, novel_folders))
    return liste
