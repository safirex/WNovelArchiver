

updateInput='u'
fullupdateInput='fu'
downloadInput='d'
statusInput='s'
compressInput='c'
autoMode='auto'


import archive_updater

def parse():
    import argparse
    from argparse import RawTextHelpFormatter
    parser = argparse.ArgumentParser(description=" WNovelArchiver",formatter_class=RawTextHelpFormatter)
    parser.add_argument("mode",
        help=
        """
        c Compiles all folders in different zip files
        d Downloads all novels listed in the input text file
        s Updates the csv file listing the novel_subtitle
        u Udpates all the novels present in novel_list""",
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
            archive_updater.download()
        if(args.mode==updateInput):
            archive_updater.archiveUpdate()
        if(args.mode==statusInput):
            archive_updater.getFolderStatus()
        if(args.mode==fullupdateInput):
            archive_updater.archiveFullUpdate()
        if(args.mode==compressInput):
            print('compression')
            print(args)
            regex=''
            out=''
            if hasattr(args, 'r'):
                regex=args.r
            if hasattr(args, 'o'):
                out=args.o
            archive_updater.compressAll(regex,out)
        if(args.mode==autoMode):
            archive_updater.background()
        if(args.mode=='launchTrayMode'):
                archive_updater.backgroundExe()
        if(args.mode=='T'):
            import asyncio
            async def localUpdate(systray='0'):
                archiveUpdate()
            asyncio.run(localUpdate())
    else:
        archive_updater.backgroundExe()

parse()
