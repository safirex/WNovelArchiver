import Downloaders
import os

def archiveUpdate(dirList=[],keep_text_format=False):
    if not dirList:
        dirList=os.listdir('./novel_list')
    print("list=")
    print(dirList)

    for novel_folder in dirList:
        print()
        novelInfo=getNovelInfoFromFolderName(novel_folder)
        #change the fetching process following the site it's hosted on
        
        novel=Downloaders.Novel(novelInfo[1],novelInfo[0],keep_text_format)
        novel=novel.updateObject()
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

            if '%s'%i not in code_list or force==True:
                print('no '+str(i))
                if int(i) == 0 and isinstance(novel,Downloaders.SyosetuNovel) :
                    novel.processTocResume()
                    continue
                elif isinstance(novel,Downloaders.SyosetuNovel) :
                    novel.setLastChapter(int(i)) #work around cause conception is shit
                    chap=int(i)
                    novel.processChapter(chap)
                    continue
                #TODO:
                elif isinstance(novel,Downloaders.KakuyomuNovel):
                    novel.setLastChapter(last_downloaded)
                    novel.setDir('./novel_list/'+novel_folder)
                    novel.processNovel()
        novel.setLastChapter(int(last_downloaded))
        #now that we have the number of the last chapter and the novel code
        #let's update the archive
        novel.processNovel()


#return code and novel name from input.txt
def getInputFile():
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

#return code and novel name from novel folder 
def getNovelInfoFromFolderName(folderName):
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
        
        name=novel_info[1]
        #print('i '+name)
        
        print(keep_text_format)
        novel=Downloaders.Novel(code,name,keep_text_format)
        novel=novel.updateObject()
        if(novel==0):
            continue

        #detect if the novel has already been downloaded
        match=findNovel(code)
        if (len(match)>0):
            print(match[0][:25]+'... \t folder already exists')
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
        if code+' '+name not in match:
            try :
                os.mkdir('%s'%dir)
            except FileExistsError:
                print("the folder already exists")
                continue
        else:
            print(code+' '+name+' folder already imported, update to fetch updates')
            continue

        print("dir=  "+dir)
        
        #dir='./novel_list/'+code+' '+name
        novel.setDir(dir)
        novel.setLastChapter(0)
        novel.processNovel()

#register as csv every folder name and the number of chapter
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

#overwrite the file with tab content
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

#compress in zip format every novel folder found
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

#find in the novels folder every regex match
def findNovel(regex,dir='./novel_list'):
    import re
    liste=[]
    regex=  re.compile(regex)
    novel_folders=os.listdir(dir)
    liste=list(filter(regex.match, novel_folders))
    return liste
