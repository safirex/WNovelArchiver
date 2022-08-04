# coding: utf-8

import argparse
from argparse import RawDescriptionHelpFormatter
import sys
import os
sys.path.append('.\src')
sys.path.append('..\src')


from src.main_functions import *



updateInput='u'
fullupdateInput='fu'
downloadInput='d'
statusInput='s'
compressInput='c'


def dev_tests():
    x = Novel('n6912eh', 'My Skills Are Too Strong to Be a Heroine')
    x = x.updateObject()
    print(type(x))
    x.setLastChapter(0)
    x.processNovel()
def check_env():
    try: 
        os.listdir('novel_list')
    except FileNotFoundError: 
        os.mkdir('novel_list')


def parser():
    parser = argparse.ArgumentParser(description="""        c to compress novels in zip
        d to download input.txt list
        s to update status.csv
        u to update novels""",
        formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("mode",
        help="put the letter of argument c/d/s/u",
        type=str,default=argparse.SUPPRESS)

    parser.add_argument("-r", help="regex of entree for compression selection (select * containing regex)",
        type=str,default=argparse.SUPPRESS)
    parser.add_argument("-o", help="output directory (only works for compression)",
        type=str,default=argparse.SUPPRESS)
    parser.add_argument("-f", help="force",action='store_true'
        ,default=argparse.SUPPRESS)
    parser.add_argument("-md", help="format",action='store_true'
        ,default=argparse.SUPPRESS)   

    args = parser.parse_args()
    print(args)
    regex=''
    keep_text_format=False

    if args.mode:
        if hasattr(args, 'md'):
            keep_text_format=True

        if hasattr(args, 'r'):
            regex=args.r

        if(args.mode==downloadInput):
            print("downloading")
            download(keep_text_format)
            
        elif(args.mode==updateInput):
            archiveUpdate(findNovel(regex),keep_text_format)


        elif(args.mode==statusInput):
            getFolderStatus()

        elif(args.mode==fullupdateInput):
            if hasattr(args, 'f'):
                archiveFullUpdate(findNovel(regex),True)
            else:
                archiveFullUpdate(findNovel(regex))
        elif(args.mode=='t'):
            dev_tests()
            

        elif(args.mode==compressInput):
            print('compression')
            print(args)
            out=''
            if hasattr(args, 'o'):
                out=args.o
            compressAll(regex,out)

if __name__ == '__main__':
    check_env()
    parser()

