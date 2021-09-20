# coding: utf-8
from argparse import RawDescriptionHelpFormatter
import sys
sys.path.append('.\src')

import main_functions as mf


updateInput='u'
fullupdateInput='fu'
downloadInput='d'
statusInput='s'
compressInput='c'



def parser():
    import argparse
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
            mf.download(keep_text_format)
            
        elif(args.mode==updateInput):
            
            
            mf.archiveUpdate(mf.findNovel(regex),keep_text_format)

        elif(args.mode==statusInput):
            mf.getFolderStatus()

        elif(args.mode==fullupdateInput):

            if hasattr(args, 'f'):
                mf.archiveFullUpdate(mf.findNovel(regex),True)
            else:
                mf.archiveFullUpdate(mf.findNovel(regex))

        elif(args.mode==compressInput):
            print('compression')
            print(args)
            out=''
            if hasattr(args, 'o'):
                out=args.o
            mf.compressAll(regex,out)


parser()