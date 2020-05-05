# coding: utf-8

import os
import sys

cwd=os.getcwd()
sys.path.insert(1,cwd+'\\src')

import syosetuDL





def updateArchive():
    for novel_directory in os.listdir('./novel_list'):
        print()
        code=novel_directory.find(' ')
        novel_name=novel_directory[code:]
        code=novel_directory[:code]
        chapter_list=os.listdir('./novel_list/%s'%novel_directory)
        last_downloaded=0
        for chap in chapter_list:
            n=chap.find('_')
            tmp=chap[:n]
            tmp=int(tmp)
            if(last_downloaded<tmp):
                last_downloaded=tmp
        print('last chapter: '+str(last_downloaded))

        #now that we have the last chapter and the novel code let's update the archive

        if(len(code)==7 and code.find('n')==0):
            print("sysosetu novel "+novel_name)
            novel_name='novel_list\\'+code+novel_name
            syosetuDL.processSyosetuNovel(code,novel_name,last_downloaded)








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
    print('list= ')

    # novel_list[]= [code,name]
    print(novel_list)
    return novel_list


def download():
    novel_list=getInputFile()
    for novel_info in novel_list:

        code=novel_info[0]
        if code=='':
            continue

        name=novel_info[1]
        print('i '+name)
        if (name==''):
            name='./novel_list/'
            #name+=novel.getname
        else:
            name='./novel_list/'+code+' '+name


        dirlist=os.listdir('./novel_list/')
        if name not in dirlist:
            os.mkdir('%s'%name)



        if (len(code)==7):
            #syosetu code/directory+novelname/last chapter downloaded
            syosetuDL.processSyosetuNovel(code,name,0)



type=''
for arg in sys.argv:
    type=arg

updateInput='u'
downloadInput='d'



if(type==''):
    input=input("update archive (a) or download (d) ?  ")
    if (input==updateInput):
        updateArchive()
    elif (input==downloadInput):
        download()

if(type==updateInput):
    updateArchive()

if(type==downloadInput):
    download()
