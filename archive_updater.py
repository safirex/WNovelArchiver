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
        novelInfo=getNovelInfoFromFolderName(novel_folder)
        #change the fetching process following the site it's hosted on
        novel=Downloaders.Novel(novelInfo[1],novelInfo[0])
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
        NFs=getNovelInfoFromFolderName(novel_folder)
        novel_name=NFs[0]   #novel_folder[code:]
        code=NFs[1]         #novel_folder[:code]
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
        novel_name=line[separator+1:] #delete carriage return
        novel_name=novel_name.strip()
        novel_list.append([code,novel_name])
        line = inputfile.readline()
    inputfile.close()
    #print('list= ')

    return novel_list


def getNovelInfoFromFolderName(folderName):
    code=       folderName.find(' ')
    novel_name= folderName[code+1:].strip()
    code=       folderName[:code]
    return [novel_name,code]




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

def findNovel(regex,dir='./novel_list'):
    liste=[]
    for novel_folder in os.listdir(dir):
        if novel_folder.find(regex)!=-1:
            liste.append(novel_folder)
    return liste


updateInput='u'
fullupdateInput='fu'
downloadInput='d'
statusInput='s'
compressInput='c'



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
            if hasattr(args, 'r'):
                regex=args.r
                archiveUpdate(findNovel(regex))
            else:
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


#parser()
"""
novel=Downloaders.Novel("n5947eg","Boukensha ni naritai")
novel=novel.updateObject()"""

import Chapters
chapter=Chapters.WuxiaWorldChapter("https://www.wuxiaworld.com/novel/the-second-coming-of-gluttony",131)
html="""<!DOCTYPE html>
<html lang="en" class="no-js">
<head prefix="og: http://ogp.me/ns# article: http://ogp.me/ns/article#">
<meta charset="utf-8" />
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SCOG - Chapter 12. Top Record - WuxiaWorld</title>
<meta name="description" content="The Second Coming of Gluttony - Chapter 12. Top Record">
<link rel="dns-prefetch" href="//cdnjs.cloudflare.com">
<link rel="dns-prefetch" href="//cdn.jsdelivr.net">
<link rel="dns-prefetch" href="//cdn.wuxiaworld.com">
<link rel="preconnect" href="https://fonts.gstatic.com/" crossorigin>
<link rel="canonical" href="https://www.wuxiaworld.com/novel/the-second-coming-of-gluttony/scog-chapter-12">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png?v=jwEkKXw8PY">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png?v=jwEkKXw8PY">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png?v=jwEkKXw8PY">
<link rel="manifest" href="/site.webmanifest?v=jwEkKXw8PY">
<link rel="mask-icon" href="/safari-pinned-tab.svg?v=jwEkKXw8PY" color="#5b5b5b">
<link rel="shortcut icon" href="/favicon.ico?v=jwEkKXw8PY">
<meta name="msapplication-TileColor" content="#5b5b5b">
<meta name="theme-color" content="#ffffff">
<meta name="apple-mobile-web-app-title" content="Wuxiaworld">
<meta name="application-name" content="Wuxiaworld">
<link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,600,700,800&display=swap" rel="stylesheet">
<script src="/js/modernizr.js?v=QqwOvVrpWvoR-sQKfhc2L-PFhSBhC-AECmi5PesXQAA"></script>
<link rel="stylesheet" href="/build/css/main-c072334c1f.min.css?v=PVXxeKWYi9P3dQbKT0sZHDxNREOQ4rCEbs8I-Fsigno" />
<meta name="x-stylesheet-fallback-test" content="" class="main-style" /><script>!function(a,b,c,d){var e,f=document,g=f.getElementsByTagName("SCRIPT"),h=g[g.length-1].previousElementSibling,i=f.defaultView&&f.defaultView.getComputedStyle?f.defaultView.getComputedStyle(h):h.currentStyle;if(i&&i[a]!==b)for(e=0;e<c.length;e++)f.write('<link href="'+c[e]+'" '+d+"/>")}("visibility","hidden",["/css/main.css?v=PVXxeKWYi9P3dQbKT0sZHDxNREOQ4rCEbs8I-Fsigno"], "rel=\u0022stylesheet\u0022 ");</script>

<!--[if IE 10]>
        <link rel="stylesheet" href="~/css/ie10-viewport-bug-workaround.min.css" asp-append-version="true" />
    <![endif]-->
<script defer src="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@5.8.2/js/all.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@5.8.2/js/v4-shims.min.js"></script>

<link rel="stylesheet" href="/build/css/custom-cab348d8aa.min.css?v=0YiU04F6_pIFf9C-ead4NjAYLu3XSELQ3f4kGthNwkw" />
<meta name="x-stylesheet-fallback-test" content="" class="custom-style" /><script>!function(a,b,c,d){var e,f=document,g=f.getElementsByTagName("SCRIPT"),h=g[g.length-1].previousElementSibling,i=f.defaultView&&f.defaultView.getComputedStyle?f.defaultView.getComputedStyle(h):h.currentStyle;if(i&&i[a]!==b)for(e=0;e<c.length;e++)f.write('<link href="'+c[e]+'" '+d+"/>")}("visibility","hidden",["/css/custom.css?v=0YiU04F6_pIFf9C-ead4NjAYLu3XSELQ3f4kGthNwkw"], "rel=\u0022stylesheet\u0022 ");</script>
<link rel="stylesheet" href="/css/bootstrap-notifications.css" />
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/froala-editor@3.2.0/css/froala_style.min.css" />

<!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
        <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
<script type="text/javascript">
            var USER = {"id":"e4220ac5-bf3a-4051-8aa3-3ca279661799","userName":"Xxsafirex","avatar":null,"isVip":false};
        </script>
<script src="/dist/devicedetection.min.js?v=vefZpNIkYyMCAqewBcVA2endwsrYJvh2gJoRIxUrt0o"></script>
<script src="//m2d.m2.ai/m2d.wuxiaworld.offpage.js" async></script>
<script async src="https://cdn.insurads.com/bootstrap/2CZCCRP8.js"></script>
<script type="text/javascript">
        (function(i, s, o, g, r, a, m) {
            i['GoogleAnalyticsObject'] = r;
            i[r] = i[r] ||
                function() {
                    (i[r].q = i[r].q || []).push(arguments)
                }, i[r].l = 1 * new Date();
            a = s.createElement(o),
                m = s.getElementsByTagName(o)[0];
            a.async = 1;
            a.src = g;
            m.parentNode.insertBefore(a, m)
        })(window, document, 'script', 'https://www.google-analytics.com/analytics.js', 'ga');

        ga('create', 'UA-57967886-1', 'auto');
        ga('set', 'transport', 'beacon');

            ga('set', 'userId', 'Xxsafirex');

        ga('set', 'dimension5', 'free');
        ga('set', 'dimension6', 'yes');
    </script>
<script>
  (function(w, d, e, u, c, g, a, b){
    w["SSJSConnectorObj"] = w["SSJSConnectorObj"] || {ss_cid : c, domain_info: g};
    a = d.createElement(e);
    a.async = true;
    a.src = u;
    b = d.getElementsByTagName(e)[0];
    b.parentNode.insertBefore(a, b);
  })(window,document,"script","https://cdn.perfdrive.com/aperture/aperture.js","9829","auto");
</script>
<script>
        ga('send',
            'pageview',
            {
                'dimension2': "FudgeNouget",
                'dimension4': "the-second-coming-of-gluttony"
            });
    </script>
<link rel="prev" href="/novel/the-second-coming-of-gluttony/scog-chapter-11" />
<link rel="next" href="/novel/the-second-coming-of-gluttony/scog-chapter-13" />
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap" />
<meta property="og:title" content="Chapter 12. Top Record">
<meta property="og:type" content="article">
<meta property="og:url" content="https://www.wuxiaworld.com/novel/the-second-coming-of-gluttony/scog-chapter-12">
<meta property="og:image" content="https://www.wuxiaworld.com/Wu-Black-192.jpg">
<meta property="og:image:secure_url" content="https://www.wuxiaworld.com/Wu-Black-192.jpg">
<meta property="article:expiration_time" content="01/01/0001 00:00:00">
<meta property="article:modified_time" content="01/01/0001 00:00:00">
<meta property="article:published_time" content="11/03/2019 04:42:00">
<meta property="article:section" content="The Second Coming of Gluttony">
<meta property="article:tag" content="The Second Coming of Gluttony">
<meta property="article:tag" content="Chapter 12. Top Record">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebPage","name":"Chapter 12. Top Record","author":{"@type":"Person","name":"FudgeNouget"},"datePublished":"2019-11-03","headline":"The Second Coming of Gluttony","publisher":{"@type":"Organization","name":"WuxiaWorld","logo":"https://www.wuxiaworld.com/img/logo.png"}}</script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","name":"Books","item":{"@type":"WebPage","@id":"https://www.wuxiaworld.com/novels","name":"Books","url":"https://www.wuxiaworld.com/novels"},"position":1},{"@type":"ListItem","name":"The Second Coming of Gluttony","item":{"@type":"Book","@id":"https://www.wuxiaworld.com/novel/the-second-coming-of-gluttony","name":"The Second Coming of Gluttony","url":"https://www.wuxiaworld.com/novel/the-second-coming-of-gluttony","author":{"@type":"Person","name":"FudgeNouget"},"publisher":{"@type":"Organization","name":"WuxiaWorld","logo":"https://www.wuxiaworld.com/img/logo.png"}},"position":2}]}</script>
<meta name="twitter:card" content="summary">
<meta name="twitter:site" content="@Wuxiaworld_Ltd">
<meta name="twitter:title" content="Chapter 12. Top Record">
<meta name="twitter:description" content="The Second Coming of Gluttony - Chapter 12">
<meta name="twitter:creator:id" content="844677854080090112">
<meta name="twitter:image" content="https://www.wuxiaworld.com/Wu-Black-192.jpg">
<script>
        var CHAPTER = {"id":86813,"name":"Chapter 12. Top Record","slug":"scog-chapter-12","novelSlug":"the-second-coming-of-gluttony","novelIsSneakPeek":false,"isTeaser":false,"isKarmaLocked":false,"prevChapter":"/novel/the-second-coming-of-gluttony/scog-chapter-11","nextChapter":"/novel/the-second-coming-of-gluttony/scog-chapter-13","siteAnnouncements":[{"id":114989,"important":true}],"novelAnnouncementId":null,"isAdwalled":false,"adwallTag":null};
    </script>
<script src="/dist/chapter.layout.min.js?v=UB1KFKGrw0RTDuoLQ2IvF63ekmlqVB2OYP7oCH43uJo"></script>
<style>
        .chapter-nav {
            display: block;
            height: 0;
            opacity: 0;
            pointer-events: none;
        }
    </style>
<script type="text/javascript">
        _atrk_opts = { atrk_acct: "Q6vrl1aQpu23mh", domain: "wuxiaworld.com", dynamic: true };
        (function () {
            var as = document.createElement('script');
            as.type = 'text/javascript';
            as.async = true;
            as.src = "https://d31qbv1cthcecs.cloudfront.net/atrk.js";
            var s = document.getElementsByTagName('script')[0];
            s.parentNode.insertBefore(as, s);
        })();
    </script>
<noscript>
        <img src="https://d5nxst8fruw4z.cloudfront.net/atrk.gif?account=Q6vrl1aQpu23mh" style="display: none" height="1" width="1" alt=""/>
    </noscript>
<link rel="manifest" href="/manifest.json" />
<script src="https://cdn.onesignal.com/sdks/OneSignalSDK.js" async=""></script>
<script>
            var OneSignal = window.OneSignal || [];
            OneSignal.push(function() {
                OneSignal.init({
                    appId: "7c171fc0-36b8-48dc-8907-00fbe7bb6181",
                    autoRegister: false,
                    welcomeNotification: {
                        disable: true
                    }
                });
            });
        </script>

<script>
          !function(f,b,e,v,n,t,s)
          {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
          n.callMethod.apply(n,arguments):n.queue.push(arguments)};
          if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
          n.queue=[];t=b.createElement(e);t.async=!0;
          t.src=v;s=b.getElementsByTagName(e)[0];
          s.parentNode.insertBefore(t,s)}(window, document,'script',
          'https://connect.facebook.net/en_US/fbevents.js');
          fbq('init', '2110477142432381');
          fbq('track', 'PageView');
        </script>
<noscript>
            <img height="1" width="1" style="display:none"
                 src="https://www.facebook.com/tr?id=2110477142432381&ev=PageView&noscript=1"/>
        </noscript>

</head>
<body class="pp">
<script type="text/javascript">
        (function () {
            if (window.localStorage) {
                var darkmode = localStorage.getItem('darkmode') === "true";

                if (darkmode) {
                    document.body.classList.add('darkmode');
                }
            }
        })();
    </script>

<nav class="navbar navbar-inverse">
<div class="container">
<div class="navbar-header">
<a href="#" class="navbar-toggle collapsed pull-left nav-icon" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
<i class="fas fa-bars fa-3x fa-fw" data-fa-transform="shrink-8.0" data-fa-mask="fas fa-circle" style="color: #696969"></i>
</a>
<a style="text-decoration: none; color: #fff" class="navbar-brand" href="/">
<img style="display: inline" height="60" width="42" src="/Wu-White.svg" /> Wuxiaworld
</a>
<div class="navbar-link visible-xs-inline pull-right">
</div>
</div>
<div id="navbar" class="navbar-collapse collapse">
<ul class="nav navbar-nav nav-public">
<li class="">
<a href="/profile/bookmarks">
Bookmarks
</a>
</li>
<li class="dropdown">
<a href="/novels">
Series
</a>
<ul class="dropdown-menu"></ul></li>
<li class="dropdown">
<a href="/profile/audiobooks">
Audiobooks
</a>
<ul class="dropdown-menu"></ul></li>
<li class="dropdown">
<a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" data-name="Resources" aria-haspopup="true" aria-expanded="false">
<i class="fas fa-chevron-down icon-rotate" aria-hidden="true"></i> Resources
</a>
<ul class="dropdown-menu"><li>
<a href="/page/about">About</a>
<ul class="dropdown-menu"></ul></li><li>
<a href="/page/contact-us">Contact Us</a>
<ul class="dropdown-menu"></ul></li><li>
<a href="/page/general-faq">General FAQ</a>
<ul class="dropdown-menu"></ul></li><li>
<a href="/page/what-dao-heck">Basic Dao Primer</a>
<ul class="dropdown-menu"></ul></li><li>
<a href="http://forum.wuxiaworld.com">Forums</a>
<ul class="dropdown-menu"></ul></li><li>
<a href="/page/deathblade-learning-chinese-faq">Deathblade's Learning Chinese FAQ</a>
<ul class="dropdown-menu"></ul></li><li>
<a href="/page/general-glossary-of-terms">General Glossary of Terms</a>
<ul class="dropdown-menu"></ul></li><li>
<a href="/page/chinese-idiom-glossary">Chinese Idiom Glossary</a>
<ul class="dropdown-menu"></ul></li><li>
<a href="/page/wuxia-xianxia-terms-of-address">Wuxia-Xianxia Terms of Address</a>
<ul class="dropdown-menu"></ul></li><li>
<a href="/page/cores-in-chinese-cultivation-novels">"Cores" in Chinese Cultivation Novels</a>
<ul class="dropdown-menu"></ul></li><li>
<a href="/page/terms-of-service">Terms of Service</a>
<ul class="dropdown-menu"></ul></li><li>
<a href="/page/author-biographies">Author Biographies</a>
<ul class="dropdown-menu"></ul></li></ul></li></ul>
<ul class="nav navbar-nav nav-private navbar-right">
<li id="searchbox"></li>
<li style="display: inline-block">
<a class="nav-icon" href="/profile/vip">
<span class="fa-layers fa-3x">
<i class="fas fa-circle" style="color: #696969"></i>
<span class="fa-layers-text" style="color: #303030 !important; font-weight: 800; font-size: 20px">VIP</span>
<noscript>
                        <img src="/images/vip239.png" alt="vip" />
                    </noscript>
</span>
</a>
</li>
<li style="display: inline-block">
<a id="light-btn" href="javascript:" class="darkmode-btn nav-icon hidden">
<i class="far fa-lightbulb fa-3x" data-fa-transform="shrink-3.5" data-fa-mask="fas fa-circle" style="color: #696969"></i>
</a>
<a id="dark-btn" href="javascript:" class="darkmode-btn nav-icon hidden">
<i class="fas fa-moon fa-3x" data-fa-transform="shrink-3.5" data-fa-mask="fas fa-circle" style="color: #696969"></i>
</a>
</li>
<li id="notifications-list" class="dropdown dropdown-notifications sw-open">
<a href="#" id="notifications-btn" class="dropdown-toggle nav-icon" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">
<span class="fa-layers fa-3x">
<i class="fas fa-flag" data-fa-transform="shrink-3.5" data-fa-mask="fas fa-circle" style="color: #696969"></i>
</span>
</a>
<div class="dropdown-menu dropdown-container dropdown-position-bottomright">
<div class="dropdown-toolbar">
<div class="dropdown-toolbar-actions">
<a id="enable-push-notifications" class="hidden" href="#">Enable push notifications</a>
<a id="mark-notifications-read" href="#">Mark all as read</a>
</div>
<h3 class="dropdown-toolbar-title">Notifications (<span class="notifications-count">0</span>)</h3>
</div>
<ul id="notifications-dropdown" class="dropdown-menu notifications"></ul>
<div class="dropdown-footer text-center">
<a href="/profile/notifications">View All</a>
</div>
</div>
</li>
<li class="dropdown">
<a href="#" class="dropdown-toggle nav-icon" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">
<i class="fas fa-bars fa-3x hidden-xs" data-fa-transform="shrink-8.0" data-fa-mask="fas fa-circle" style="color: #696969"></i>
<span class="visible-xs-inline sbold">
Xxsafirex
</span>
</a>
<ul class="dropdown-menu">
<li class="karma">
<div class="karma-amount">
<span>
<i style="color: #c0c0c0" class="fas fa-fw fa-yin-yang"></i> <span>0</span>
</span>
</div>
<div class="karma-amount">
<span>
<i style="color: #ffd700" class="fas fa-fw fa-yin-yang"></i> <span>0</span>
</span>
</div>
</li>
<li>
<a id="submitLoginMission" class="" href="javascript:">
Check-in (0/1)
</a>
</li>
<li>
<a href="/profile/sponsor">My Sponsorships</a>
</li>
<li>
<a href="/profile/karma">My Karma</a>
</li>
<li>
<a href="/profile/ebooks">My Ebooks</a>
</li>
<li>
<a href="/profile/audiobooks">My Audiobooks</a>
</li>
<li>
<a href="/profile">My Settings</a>
</li>
<li>
<a href="/profile/bookmarks">Bookmarks</a>
</li>
<li>
<a id="logout-btn" href="javascript:" data-returnurl="/">
Logout
</a>
</li>
</ul>
</li>
</ul>
</div>
</div>
</nav>
<div class="main">
<div class="container ">

<div class="content space-0">
<div>
<div id="content-container" class="space-0 col-lg-9 col-md-8">
<div><div class="IBItBErC" id="wuxiaworld_ATF1"></div></div>
<script id="remove-wuxiaworld_ATF1-IBItBErC" type="text/javascript">
        (function(id, type, placement) {
            var self = document.querySelector('#remove-' + id + '-IBItBErC');
            var el = document.querySelector('#' + id + '.IBItBErC');
            MainApp.devicedetection.checkAd(28, self, el, type, placement);
        })('wuxiaworld_ATF1', 'desktoptablet', 'header');
    </script>
<div><div class="sticky-foot wDEGAEtv" id="wuxiaworld_1x1"></div></div>
<script id="remove-wuxiaworld_1x1-wDEGAEtv" type="text/javascript">
        (function(id, type, placement) {
            var self = document.querySelector('#remove-' + id + '-wDEGAEtv');
            var el = document.querySelector('#' + id + '.wDEGAEtv');
            MainApp.devicedetection.checkAd(34, self, el, type, placement);
        })('wuxiaworld_1x1', 'mobile', 'header');
    </script>
<div><div class="p-20 tJHDDCtr" id="wuxiaworld_ATF1"></div></div>
<script id="remove-wuxiaworld_ATF1-tJHDDCtr" type="text/javascript">
        (function(id, type, placement) {
            var self = document.querySelector('#remove-' + id + '-tJHDDCtr');
            var el = document.querySelector('#' + id + '.tJHDDCtr');
            MainApp.devicedetection.checkAd(39, self, el, type, placement);
        })('wuxiaworld_ATF1', 'mobile', 'header');
    </script>
<div class="section">
<div class="section-content">
<noscript>
            <div class="panel panel-success">
                <div class="panel-heading">
                    <a href="/announcement/audiobooks-live-two-new-novels">
                        <h4 class="panel-title pull-left" style="color: #a94442 !important">
                            <strong>Audiobooks Live!  Two New Novels!</strong>
                        </h4>
                    </a>
                    <div class="clearfix"></div>
                </div>
                    <div class="fr-view panel-body">
                        <p>Hi everyone, two sets of announcements here with many more coming into the holiday break! &nbsp;At long last, the first batch of audiobooks mentioned <a href="https://www.wuxiaworld.com/announcement/rise-of-audiobooks-new-novel-audiobook-previews">in this post</a> are here! &nbsp;You can find them at the top of the navbar, or <a href="https://www.wuxiaworld.com/profile/audiobooks">directly at this link</a>! &nbsp;Our launch titles are <strong>Coiling Dragon</strong> books 2 and 3, <strong>ISSTH</strong> Book 1, and <strong>Desolate Era</strong> Book 1. &nbsp;They'll be Wuxiaworld exclusives for a period of 1 month at a discounted price, after which point we'll be putting them up for sale on Amazon as well. &nbsp;The reason we're doing this and...</p>
                        <p>
                            <a href="/announcement/audiobooks-live-two-new-novels">Read More...</a>
                        </p>
                    </div>
            </div>
        </noscript>
<div id="announcement-114989" class="panel panel-success hidden">
<div class="panel-heading">
<a href="/announcement/audiobooks-live-two-new-novels">
<h4 class="panel-title pull-left" style="color: #a94442 !important">
<strong>Audiobooks Live! Two New Novels!</strong>
</h4>
</a>
<button id="announcement-close-114989" type="button" class="close pull-right" data-target="#announcement-body-114989" data-dismiss="alert">
<i class="fas fa-times"></i><span class="sr-only">Close</span>
</button>
<div class="clearfix"></div>
</div>
<div id="announcement-body-114989" class="fr-view panel-body hidden">
<p>Hi everyone, two sets of announcements here with many more coming into the holiday break! &nbsp;At long last, the first batch of audiobooks mentioned <a href="https://www.wuxiaworld.com/announcement/rise-of-audiobooks-new-novel-audiobook-previews">in this post</a> are here! &nbsp;You can find them at the top of the navbar, or <a href="https://www.wuxiaworld.com/profile/audiobooks">directly at this link</a>! &nbsp;Our launch titles are <strong>Coiling Dragon</strong> books 2 and 3, <strong>ISSTH</strong> Book 1, and <strong>Desolate Era</strong> Book 1. &nbsp;They'll be Wuxiaworld exclusives for a period of 1 month at a discounted price, after which point we'll be putting them up for sale on Amazon as well. &nbsp;The reason we're doing this and...</p>
<p>
<a href="/announcement/audiobooks-live-two-new-novels">Read More...</a>
</p>
</div>
</div>
<div class="top-bar-area">
<ul class="list-inline">
<li class="prev">
<a href="/novel/the-second-coming-of-gluttony/scog-chapter-11" class="btn btn-link">
<img src="/images/arrow-left.png" alt="older" />
</a>
</li>
<li class="caption">
<a href="/novel/the-second-coming-of-gluttony">
<h4>The Second Coming of Gluttony</h4>
</a>
</li>
<li class="next">
<a href="/novel/the-second-coming-of-gluttony/scog-chapter-13" class="btn btn-link">
<img src="/images/arrow-right.png" alt="newer" />
</a>
</li>
</ul>
</div>
<div class="panel panel-default">
<div id="chapter-bar"></div>
<div id="chapter-outer" class="p-15">
<div class="caption clearfix">
<div class="font-resize">
<a href="javascript:void(0);" id="fs-minus">
<img src="/images/font-minus.png" alt="size minus">
</a>
<a href="javascript:void(0);" id="fs-normal">
<img src="/images/font-normal.png" alt="size normal">
</a>
<a href="javascript:void(0);" id="fs-plus">
<img src="/images/font-plus.png" alt="size plus">
</a>
</div>
<div id="sidebar-toggler-container" style="margin-right: 10px" class="hidden visible-md pull-right">
<a href="javascript:" id="sidebar-toggle" class="btn btn-sm btn-inverse">
</a>
</div>
<div>
<img src="/images/title-icon.png">
<h4 class="">Chapter 12. Top Record</h4>
</div>
</div>
<div class="clearfix"></div>
<div id="chapter-content" class="fr-view">
<script>
        (function() {
            if (window.localStorage) {
                var fontSize = parseFloat(localStorage.getItem('fontsize'));

                if (!isNaN(fontSize)) {
                    document.getElementById("chapter-content").style.fontSize = fontSize + "px";
                }
            }
        })();
    </script>
<p>“Are you crazy?! Open the barrier right now!!”</p><p>“Why should I? This here is my doorway. I decide what to do with it.”</p><p>“Why are you acting like this? Do you have any idea just what we had to go through to get here?”</p><p>“Aigoo~. So, you had to go through so much, huh? But, what should I do? According to a certain someone, I'm an egocentric, petty son of a bitch.”</p><p>Shin Sang-Ah gritted her teeth while listening to Kang Seok's sarcastic remarks. She could more or less tell why this asshole was acting this way. Clearly, he was still holding a grudge against her for that verbal spat back in the assembly hall.</p><p>She held back her anger and spoke to him in a level voice.</p><p>“I apologize. I apologize for calling you names when we were in the assembly hall, so please open this barrier. It's not just me here, too. These people haven't done anything to you. You shouldn't treat people's lives as a joke.”</p><p>“Ooh… now that’s not what I expected to hear from you. Are you being honest?”</p><p>“…Of course.”</p><p>“Well, I guess I don't have much choice here then. Fine. Prove it to me.”</p><p>“Prove it?”</p><p>“The other four with you, I'll let them in. You stand back.”</p><p>Shin Sang-Ah's jaw dropped to the floor. Her expression screamed, ‘what kind of an asshole would act like this?’ Unfortunately for her, Kang Seok's expression showed how relaxed he was.</p><p>“You….. You…..”</p><p>“What are you going to do? That monster might show up soon, you know~.”</p><p>Shin Sang-Ah didn't expect Kang Seok to behave like this, and her face reddened up considerably as a result. However, with the exception of Yi Sungjin, the other three were looking at her with pleading eyes. Their stares were laden with a certain pressure. She gritted her teeth and took three, four steps back.</p><p>“Oh, wow, a martyr, aren’t you?”</p><p>Kang Seok exclaimed out loud as he pressed the release button. As soon as the barrier was lowered, the three rushed inside. Yi Sungjin stared at Shin Sang-Ah for a bit before belatedly trudging past the barrier as well. Only afterwards did the trio begin calling out to her, crying out her name out in a helpless manner. The barrier closed shut regardless.</p><p>However, Yi Sungjin suddenly reached out towards the button to press it. He'd been watching Kang Seok's hand quite intently just now.</p><p>Of course, nothing happened. Seeing this, Kang Seok broke out in laughter.</p><p>“Don’t waste your time. Didn't I tell you? Only I can open the barrier.”</p><p>Yi Sungjin suddenly pounced on Kang Seok. However, it couldn't even be called a fight from the get-go. The teen boy got easily subdued by Yi Hyungsik and Jeong Minwoo, and he could only glare at Kang Seok in rage.</p><p>“Bastard, do you have a death wish? What, did that bitch tell you she'll become your new sister or something?”</p><p>“Open… the barrier!”</p><p>“That's up to me, and I kept my end of the deal.”</p><p>“….”</p><p>“Good job. You can go look for another path or something now. Good luck.”</p><p>Shin Sang-Ah couldn't bring herself to leave just like that. She scanned the inside of the waiting room, hoping for something or someone to save her, but that turned out to be a waste of time. The people inside were either spectating or looking unconcerned.</p><p>In the end, she turned around helplessly.</p><p>“Should I let you in?”</p><p>Hearing this, Shin Sang-Ah's steps came to a halt. She abruptly spun her head and shot Kang Seok a murderous look.</p><p>“Do you actually enjoy toying with people?”</p><p>“Yup. When would I ever get to have fun like this if it's not today?”</p><p>Kang Seok nonchalantly replied and gestured her to come closer.</p><p>“Stop being difficult and come over here. You saw me letting people in just now, right? I'm the kind of guy who keeps his promises.”</p><p>Hearing his words of keeping promises, Shin Sang-Ah was gripped by an intense bout of doubt and uncertainty. But thinking about the hardships she suffered to get here, she couldn’t imagine looking for another path.</p><p>Plus, even if there was another path, she had to search for it alone. She figured it'd be better to get bitten by a rabid dog once.</p><p>She made up her mind and turned around to face him.</p><p>“….What do you want me to do?”</p><p>“I'm not asking for much. Just apologize for the things you said back in the assembly hall.”</p><p>“But I already did….”</p><p>“No, no, it was clear to anyone watching that you weren’t sincere. Besides, I'm not the type to believe in apologies coming out of a person's mouth.”</p><p>“Then what do you want me to do?”</p><p>Shin Sang-Ah raised her voice when Kang Seok remained sarcastic to the end. He rubbed his chin as his eyes scanned her lecherously. Shin Sang-Ah did not possess the same sort of ‘fresh’ appeal as Yi Seol-Ah, but her skin was pale and smooth, and her rack was commendably voluptuous.</p><p>A sinister smirk formed on Kang Seok's lips.<br><br>“First, take them off.”</p><p>“….What?”</p><p>Shin Sang-Ah couldn't help but question her own hearing.</p><p>“Take your clothes off. Ah, I'm a nice guy, so I'll let you keep your panties. Cool?”</p><p>Hearing Kang Seok's 'benevolent' tone of voice, Shin Sang-Ah even forgot to close her wide-open mouth.</p><p>“I think I’ll feel a little better if you perform a little show with a nude dance…. How about you twerk for me?”</p><p>“You… you insane… son of a bitch!”</p><p>“Don't wanna do it? Fine. Fuck off, then.”</p><p>Kang Seok shrugged his shoulders.</p><p>Shin Sang-Ah bit her lower lip until one could clearly see the teeth mark on her flesh. She inwardly mumbled, ‘This crazy son of a bitch.’</p><p>Then, her body shook from the belated sense of humiliation. Tears welled up in her eyes, ready to fall at any moment.</p><p>Unfortunately for her, that moment when her group ran into the monster still played heavily on her mind. What if, she went downstairs now and ended up encountering the monster again….?</p><p>“What are you waiting for? As I said, you can fuck off if you don't wanna do it.”</p><p>“…I'll do it.”</p><p>“Then hurry the hell up. I'll give you ten seconds to take your pants off. Starting now.”</p><p>When Kang Seok really started counting down, Shin Sang-Ah had no choice but to hurriedly undo her buttons. She hesitated when it came to pulling her pants down, but after hearing the rapid countdown, she still forced her jeans down all the while shaking like a leaf in the wind.</p><p>Kang Seok made a catcalling whistle as Shin Sang-Ah’s bare thighs were revealed to the cold air.</p><p>“Hiyaa~, you’ve got a great figure. Your underwear is pretty cute too.”</p><p>Shin Sang-Ah squeezed her eyes shut, hoping this would lessen the humiliation she felt even by a tiny amount.</p><p>“What are you doing? Keep stripping, girl. I'm gonna count down again… Huh? Huuuuh!? It's the monster!! The monster!!”</p><p>Kang Seok suddenly cried out in alarm and pointed at the staircase behind her while hurriedly taking a step back. Shin Sang-Ah's eyes shot open in shock. She screamed in terror and tumbled forward in an ungainly fashion.</p><p>“Mommy!”</p><p>Out of reflex, she looked behind her, only to find nothing there. Rather than the monster, the staircase was as empty as it could possibly get. Sure enough, she could hear several loud and detestable chortles coming from beyond the barrier.</p><p>“Did you hear that? You heard that, right? She said Mommy! Mommy!! Hahahaha!!”</p><p>“Haha, that was fucking adorable. Kyak! Mommy!”</p><p>When Yi Hyungsik imitated Shin Sang-Ah’s cries, Kang Seok and Jeong Minwoo burst into laughter. Lost for words, all Shin Sang-Ah could do was to let tears accumulate around the edges of her eyes.</p><p>“Sorry, sorry. I was just teasing you a bit. You looked really cute just now.”</p><p><em>Too much.</em></p><p>“Well~ now. It's time to remove your top, right?”</p><p><em>This is too much.</em></p><p>In the end, she couldn't hold it in any longer and broke down in tears.</p><p>“You're crying? Hey, now. You shouldn't cry, you know~. You gotta take your clothes off and dance for me before….”</p><p>Kang Seok clapped his hands boisterously and laughed before suddenly shutting his mouth. Unknowingly, a dark shadow was looming over him.</p><p>*</p><p>Seol wasn't angry from the beginning. He initially planned to ignore the matter.</p><p>He was neither a saint nor a man of justice. Like most people, he was disinclined to interfere in other people's business. Even if he saw something he considered unjust, he would only frown and think, ‘Isn’t that going too far?’</p><p>Unless it was someone he knew, Seol would never personally get up and do something for a total stranger.</p><p>However….</p><p>When his eyes landed on Yi Sungjin, or more specifically when he heard him whisper ‘help us’ as he was pinned down to the ground, he had a change of heart.</p><p>Perhaps it was a coincidence, but the scene happened to remind him of the time Yi Seol-Ah asked for help in the assembly hall.</p><p>Seol's emotions trembled. The small tremor soon spread out like some sort of a mutated butterfly effect and it violently quaked, eventually transforming into a rage.</p><p>That was why he stood up.</p><p>…Just like the day he had that dream.<br>…Just like the experience he had in the assembly hall.</p><p>[Innate Ability, Future Vision, has been activated.]</p><p>…Just like the way his emotions were leading him to.</p><p>“What? You also want to join in on the fun….?”</p><p>“That’s enough. Open the barrier please.”</p><p>Kang Seok dazedly stared up at Seol. He hadn't realized it until now, but Seol was taller than him.</p><p>“I'll open it. When I feel like it.”</p><p>“Open. The. Barrier.”</p><p>Kang Seok shut his mouth. Judging from his expression, it seemed like he just couldn’t understand.</p><p>“Did you inhale something weird? Who the hell are you to order me around?”</p><p>“Open it.”</p><p>Kang Seok's complexion hardened.</p><p>For some strange reason, he found it difficult to meet Seol's gaze. Even his balls seemed to shrink a bit. He didn't want to admit it out loud, but Kang Seok was scared. It was as if he was staring at a choice of whether he should cross a line he should never even consider crossing in the first place.</p><p>His instincts forced him to press the button. However, just before he actually did that, Kang Seok's defiant streak reared its head. He couldn’t help but think, ‘Why should I listen to this son of a bitch? Because he has a Gold Mark? What a fucking joke.’</p><p>Kang Seok arrogantly leaned his head back.</p><p>“I don't want to.”</p><p>The corners of his lips slowly wiggled and twitched.</p><p>“Listen here, I’m trying to stay friendly with all the Invited. Don’t be an asshat and go away.”</p><p>Seol slowly raised his arm up, which prompted Yi Hyungsik and Jeong Minwoo to move as well. However, Kang Seok confidently stopped them by raising his own hand.</p><p>“What? You’re gonna hit me? Fine, go ahead. If Almighty Gold Mark-nim wants to hit me, this lowly Silver Mark should just obediently get hit, no?”</p><p>“….”</p><p>“But remember this. The more you try to show off, the lesser I'll be inclined to open the…. Kuk!”</p><p><em>Thwack!</em></p><p>Seol's fist slammed into Kang Seok's nose. Yi Hyungsik and Jeong Minwoo were taken by surprise but even they had to cry out in pain while grasping their noses. The speed at which Seol's fist flew was so scarily fast, they couldn't even see it.</p><p>“Y-you son of a….. Kuaaaak!!”</p><p>Kang Seok reflexively threw a fist of his own, but Seol simply snatched it off the air and twisted it hard. The force was so severe that Kang Seok's knees gave out in one go. Seol then proceeded to drag his arm and forcibly pressed the button.</p><p>The barrier slid open.</p><p>“Come in.”</p><p>Shin Sang-Ah carried a dazed expression as she stumbled into the waiting area, not even thinking of putting her pants back on. Only then did Seol release Kang Seok's arm.</p><p>[Miss Shin Sang-Ah has arrived on the second-floor waiting area.]</p><p>[The first Tutorial mission, 'Escape from the Assembly Hall', has concluded. Number of remaining survivors: 12.]</p><p>[A new message from the Guide has arrived.]</p><p>[The second mission of the Tutorial, 'Breaking Through Traps' has begun.]</p><p>They all heard the new announcements, and at the same time, the sturdy locked gate at the end of the corridor automatically undid itself. It seemed that, regardless of the remaining time, the next mission would be triggered right away once all the survivors arrived at the waiting area.</p><p>“Kuuuuk!”</p><p>Kang Seok rolled on the floor in a fit of pain. Then, he used the wall to support himself and got up. Still holding his twisted arm, he glared at Seol with murderous intent.</p><p>“You…!”</p><p>Kang Seok was about to shout out something, but then simply spun on his heels to leave.</p><p>“We'll see what happens later, you fucking son of a bitch!”</p><p>He picked up his own bag and hastily escaped through the now-open passage. Seeing him retreat, both Yi Hyungsik and Jeong Minwoo slinked away from sight.</p><p>Next, Yun Seora, who had been watching Seol silently, turned to leave.</p><p>“T…. Thank you. Thank you so much….”</p><p>Thick teardrops fell from Shin Sang-Ah's eyes as she began to wail. Next to her, Yi Sungjin's head also dropped low.</p><p>However, the recipient of their gratitude, Seol, wasn't feeling all that good. He knew his actions were not entirely from his own will.</p><p>His rage failing to cool down drove him further into an even greater frenzy. He felt like destroying, rampaging, and making an utter mess of everything.</p><p>[Sender: The Guide.]<br>[1. Enter the classroom “3-1” on the fourth floor of the main building via annex's third floor before time runs out.]<br>[Remaining time: 01:57:56]</p><p>Two hours, and a time-limit type mission. After confirming the details of the next mission, Seol’s eyes burned with a dangerous light.</p><p>“H-hey! Hold up!”</p><p>Seol unhesitatingly walked forward, and Hyun Sangmin hurriedly chased after him with two bags.</p><p>*</p><p>[Area 1. The second mission is now commencing.]</p><p>A robotic voice made an announcement as images flickered on a massive semi-transparent screen. Several men and women were sitting in front of this screen, watching the proceedings unfold.</p><p>“It's only the second mission but…. Damn it, I'm gonna lose my mind at this rate.”</p><p>“24 people died in the first stage? How does that even make sense? Why is every one of them such goddamn trash this time?”</p><p>When a bald, giant of a man spat out in anger, a woman wearing a purple robe next to him grumbled unhappily as well. However, when another woman wearing a business suit sitting in front swept her icy gaze over them, the duo shut their mouths up rather quickly.</p><p>“Really now. At this rate, the name 'Area 1' will become a huge joke. With March's overall assessment looking this bad, how are we supposed to endure until September?”</p><p>The bald giant couldn't resist and added a couple more sentences, but fearing that the business-suit woman would glare at him again, he hurriedly turned his attention to her.</p><p>“Anyone know what's going on in the other areas? Anyone hear anything?”</p><p>“Me.”</p><p>A young man with curly hair raised his hand.</p><p>“I overheard something while I was outside…. As far as clear speed is concerned, I hear Area 2 and Area 7 are neck and neck for the first place.”</p><p>“2 and 7? I get the Europeans, but what’s up with those Chinese bastards?”</p><p>“What’s the point in even asking? You already know what dirty tricks they are using over there. Their Invited all conspire together, and as soon as the Tutorial starts, they take all the Contracted hostage. I'm sure they are passing the missions while sacrificing the Contracted whenever necessary.”</p><p>The balding giant spat out a groan.</p><p>“….Fine. What about 2?”</p><p>“I heard they are the very example of perfection itself. A French girl named Odelette Delphine has taken over the show. With just pure skills, too. Well, her killing the phantom in front of everyone with the starting bonus she got during the first mission proved to be the decisive factor.”</p><p>“Huh. What's her Mark?”</p><p>“Silver. Also, as soon as the second mission began, she succeeded in opening up the path to the computer classroom. She's bulldozing everything in her way. I think she won't even need an hour to get to the end. Maybe 50 minutes tops?”</p><p>“Wow, what is she, a monster? Europe really found a good seedling this time. What about the rest?”</p><p>“Area 5 is doing decent… but, it's so-so. They’ve had a 30-minute head start for the second mission compared us, so there's that.”</p><p>The giant groaned out again.</p><p>“God damn it. At this rate, we aren't gonna have a single one remaining at the end of the Tutorial.”</p><p>“No way. Don’t forget, we have a Gold Mark. It looks like he even has the Diary of the Unknown Student. Surely he’ll be able to clear it with no problems.”</p><p>“You think so?”</p><p>“I mean, he chased that phantom away with nothing more than his glare, right?”</p><p>The curly-haired youth spoke with the aim of consoling the giant man, but the bald giant's face continued to show how disappointed he was as his eyes remained locked on the screen. Seol, as shown on the screen, was entering the annex via the pedestrian overpass connecting the two buildings.</p><p>“Hey, doesn't that guy look a bit pissed off right now? What the hell? What's the matter with him all of a sudden?”</p><p>The curly-haired youth raised a shrill voice of surprise.</p><p>As the mission name suggested, the location reserved for the 'Breaking Through Traps' wasn't supposed to be tackled willy-nilly. Yet, Seol didn't even stop to take a look at his phone and simply strolled right in.</p><p>“….Can we really trust a guy like that?”</p><p>The bald giant tapped the woman wearing the business suit.</p><p>“Hey, say something, Kim Hannah.”</p><p>“Shut your damn mouth for once, okay?”</p><p>Kim Hannah spat out in a voice full of undisguised irritation. The giant man immediately realized that if he tried to provoke her any further, he'd be on the painful receiving end of the hysteria of an unmarried spinster.</p><p>The giant licked his lips as if he found the whole thing unsatisfactory, then got up from his seat. He figured he would rather go out for a smoke break than sit here and get pissed off at what was happening on screen.</p><p>*</p><p>The bald, big guy wasted around 15 minutes smoking outside. But, when he was about to enter the room again….</p><p><em>Clang! Clang!</em></p><p>He spat out a disappointed groan after hearing the noisy metallic clangs coming from inside. He thought that a brainless idiot was repeatedly stepping into traps, activating them inadvertently. While shaking his head, he opened the door to enter.</p><p><em>Clang!</em></p><p>Then, he tilted his head, wondering if his eyes were playing tricks on him.</p><p>In truth, the second mission wasn't at all difficult for someone like this bald man. A highly trained Earthling would be able to clear it in around 30 minutes even if he was taking his time.</p><p>However, the ones doing the mission right now weren't trained Earthlings, but a bunch of weak, powerless civilians. These people hadn't even experienced a proper war.</p><p>The goal of the mission was simple enough <span style="color: rgba(0, 0, 0, 1); background-color: rgba(0, 0, 0, 0); font-weight: 400; font-style: normal; font-variant: normal; text-decoration: none; vertical-align: baseline; white-space: pre-wrap">—</span> to stop the activation of various traps by fulfilling a set of conditions beforehand. Or, leave it to lady luck to decide. That should have been the case. However….</p><p>'He's evading, blocking, and deflecting!?'</p><p>Not only did Seol not stop after performing those actions, he even deliberately triggered the traps that hadn't been activated yet. He was progressing forward while… destroying everything. It was like looking at an Earthling, not a powerless civilian.</p><p>A look of disbelief was etched on the bald man's face as he hurriedly got closer to the screen. At the same time, three sharp metal spears were shooting out towards Seol from the ceiling and from both the right and left sides.</p><p><em>Clang! Claaaang!!</em></p><p>It was unknown where Seol had acquired a steel beam, but regardless, he spun it like a cartwheel; soon, the audience was treated to the cacophony of metallic clangs as well as a beam of cold silvery light flickering on the screen.</p><p>The result was all there to see. The moment the spears from the right and left were sent flying, the spear from the ceiling brushed past Seol and pierced the ground. The woman wearing the purple robe stood up reflexively, her fists clenched in anticipation.</p><p>“Is he dead? No, did it miss?”</p><p>“No, he dodged.”</p><p>The bald man closely watched the proceedings unfold, then confidently declared out loud.</p><p>“I'm sure of it. He slapped away the spears coming from both of his sides, and he was about to do the same to the one coming from the ceiling, but….”</p><p>“But?”</p><p>“….Dunno. It's like, his body couldn't keep up with what he wanted to do. In any case, I definitely saw him tilt his head out of the way…. Oi, Kim Hannah! Just what's up with that guy?!”</p><p>The bald guy seemed to be shocked by his own words and belatedly shouted at Kim Hannah.</p><p>Kim Hannah remained quiet for a long while before suddenly opening her mouth.</p><p>“For the second mission…. what’s the record for the fastest clear time?”</p><p>“The record? You mean, Sung Shihyun-nim’s legendary 29 minutes and 38 seconds?”</p><p><em>Mm, mm.</em> The bald giant nodded his head as if he was proud of something. Meanwhile, Kim Hannah's head dropped low, and eventually, she began rubbing her face as if she was feeling quite fatigued all of a sudden.</p><p>“….This is crazy.”</p><p>“What's crazy?”</p><p>[Area 1's second mission has been cleared.]</p><p>The expressions of everyone present became dumbfounded by the sudden announcement.</p><p>16 minutes, 24 seconds….</p><p>This was precisely the moment when history was rewritten.</p> <a href="/novel/the-second-coming-of-gluttony/scog-chapter-11" class="chapter-nav">
Previous Chapter
</a>
<a href="/novel/the-second-coming-of-gluttony/scog-chapter-13" class="chapter-nav">
Next Chapter
</a>
</div><div><div class="p-20 BEuEwBEH" id="wuxiaworld_BTF1"></div></div>
<script id="remove-wuxiaworld_BTF1-BEuEwBEH" type="text/javascript">
        (function(id, type, placement) {
            var self = document.querySelector('#remove-' + id + '-BEuEwBEH');
            var el = document.querySelector('#' + id + '.BEuEwBEH');
            MainApp.devicedetection.checkAd(29, self, el, type, placement);
        })('wuxiaworld_BTF1', 'mobile', 'belowcontent');
    </script>
<div><div class="p-20 tAIBsIEG" id="wuxiaworld_BTF5"></div></div>
<script id="remove-wuxiaworld_BTF5-tAIBsIEG" type="text/javascript">
        (function(id, type, placement) {
            var self = document.querySelector('#remove-' + id + '-tAIBsIEG');
            var el = document.querySelector('#' + id + '.tAIBsIEG');
            MainApp.devicedetection.checkAd(40, self, el, type, placement);
        })('wuxiaworld_BTF5', 'desktoptablet', 'belowcontent');
    </script>
</div>
<div class="p-15">
<a id="bookmark-chapter" href="javascript:">
<span class="icon-bookmark"></span> Bookmark
</a>
</div>
<div class="panel-footer dark space-0">
<ul class="nav nav-pills nav-justified">
</ul>
</div>
</div>
<div class="nav-bar-area">
<ul class="list-inline">
<li class="prev pull-left">
<a href="/novel/the-second-coming-of-gluttony/scog-chapter-11" class="btn btn-link">
<img src="/images/arrow-left.png" alt="older" />
</a>
</li>
<li class="caption">
<a href="/novel/the-second-coming-of-gluttony">
<h4>The Second Coming of Gluttony</h4>
</a>
</li>
<li class="next pull-right">
<a href="/novel/the-second-coming-of-gluttony/scog-chapter-13" class="btn btn-link">
<img src="/images/arrow-right.png" alt="newer" />
</a>
</li>
</ul>
</div>
</div>
</div>
<div><div class="p-20 vusFAGst" id="wuxiaworld_BTF5"></div></div>
<script id="remove-wuxiaworld_BTF5-vusFAGst" type="text/javascript">
        (function(id, type, placement) {
            var self = document.querySelector('#remove-' + id + '-vusFAGst');
            var el = document.querySelector('#' + id + '.vusFAGst');
            MainApp.devicedetection.checkAd(30, self, el, type, placement);
        })('wuxiaworld_BTF5', 'mobile', 'abovecomments');
    </script>
<div><div class="text-center CIEJGICw" id="wuxiaworld_BTF3"></div></div>
<script id="remove-wuxiaworld_BTF3-CIEJGICw" type="text/javascript">
        (function(id, type, placement) {
            var self = document.querySelector('#remove-' + id + '-CIEJGICw');
            var el = document.querySelector('#' + id + '.CIEJGICw');
            MainApp.devicedetection.checkAd(41, self, el, type, placement);
        })('wuxiaworld_BTF3', 'desktoptablet', 'abovecomments');
    </script>
<div id="comments"></div>
<div><div class="CBDtHJrC" id="wuxiaworld_BTF4_hardcoded"></div><div class="pg-lazy" data-gpt-parent="wuxiaworld_BTF4"></div></div>
<script id="remove-wuxiaworld_BTF4_hardcoded-CBDtHJrC" type="text/javascript">
        (function(id, type, placement) {
            var self = document.querySelector('#remove-' + id + '-CBDtHJrC');
            var el = document.querySelector('#' + id + '.CBDtHJrC');
            MainApp.devicedetection.checkAd(42, self, el, type, placement);
        })('wuxiaworld_BTF4_hardcoded', 'mobile', 'belowcomments');
    </script>
</div>
<div id="sidebar" class="col-lg-3 col-md-4">
<div id="placement-36" class="panel panel-default">
<div class="panel-heading">Sponsored Links</div>
<div><div class="sBIIwBJJ" id="wuxiaworld_ATF2"></div></div>
<script id="remove-wuxiaworld_ATF2-sBIIwBJJ" type="text/javascript">
        (function(id, type, placement) {
            var self = document.querySelector('#remove-' + id + '-sBIIwBJJ');
            var el = document.querySelector('#' + id + '.sBIIwBJJ');
            MainApp.devicedetection.checkAd(36, self, el, type, placement);
        })('wuxiaworld_ATF2', 'desktoptablet', 'sidebar');
    </script>
</div>
<div id="widget_72" class="panel panel-default">
<div class="panel-heading">Novel Announcements</div>
<div class="panel-body">
<div class="media">
<div class="media-heading">
<h5>Letter from the Author </h5>
</div>
<div class="media-body">
<p>Below is a letter from the author, Ro Yu-Jin, to you guys, the readers!</p><p>=================</p><p>Dear WuxiaWorld Readers,&nbsp;</p><p>Hello, this is Ro Yu-Jin. To be honest, I am nervous as I am writing this letter, and everything feels so surreal. I never imagined a day would...</p>
<div class="text-right">
<a href="/post/the-second-coming-of-gluttony/letter-from-the-author">Read More...</a>
</div>
</div>
</div>
</div>
</div>

<div id="placement-37" class="panel panel-default">
<div class="panel-heading">Sponsored Links</div>
<div><div class="JGsEtCJH" id="wuxiaworld_BTF1"></div></div>
<script id="remove-wuxiaworld_BTF1-JGsEtCJH" type="text/javascript">
        (function(id, type, placement) {
            var self = document.querySelector('#remove-' + id + '-JGsEtCJH');
            var el = document.querySelector('#' + id + '.JGsEtCJH');
            MainApp.devicedetection.checkAd(37, self, el, type, placement);
        })('wuxiaworld_BTF1', 'desktoptablet', 'sidebar');
    </script>
</div>
<div id="widget_1" class="panel panel-default">
<div class="panel-heading">Recent Chapters</div>
<div class="panel-body">
<ul class="media-list">
<li class="media">
<div class="media-body">
<a href="/novel/fields-of-gold/fog-chapter-576">
Fields of Gold - Chapter 576 - Sneaking into the Horse Herd
</a>
</div>
</li>
</ul>
<ul class="media-list">
<li class="media">
<div class="media-body">
<a href="/novel/star-odyssey/so-chapter-253">
Star Odyssey - Chapter 253: Third Nightking
</a>
</div>
</li>
</ul>
<ul class="media-list">
<li class="media">
<div class="media-body">
<a href="/novel/everyone-is-young-except-for-me/eyem-chapter-292">
Everyone is Young Except for Me - Chapter 292
</a>
</div>
</li>
</ul>
<ul class="media-list">
<li class="media">
<div class="media-body">
<a href="/novel/rankers-return/rr-chapter-290">
Ranker&#x27;s Return - Chapter 290
</a>
</div>
</li>
</ul>
<ul class="media-list">
<li class="media">
<div class="media-body">
<a href="/novel/love-code-at-the-end-of-the-world/lcew-chapter-407">
Love Code at the End of the World - Book 4, Chapter 139 - Raffles Became Devious
</a>
</div>
</li>
</ul>
<ul class="media-list">
<li class="media">
<div class="media-body">
<a href="/novel/i-am-overlord/iao-chapter-502">
I Am Overlord - Chapter 502: Nether Shadow Evanescence
</a>
</div>
</li>
</ul>
<ul class="media-list">
<li class="media">
<div class="media-body">
<a href="/novel/i-am-overlord/iao-chapter-501">
I Am Overlord - Chapter 501: Extorting the Old Nether Prison Devil
</a>
</div>
</li>
</ul>
<ul class="media-list">
<li class="media">
<div class="media-body">
<a href="/novel/invincible/inv-chapter-1817">
Invincible - &#x1F42F;Chapter 1817: Everyone, Don’t Panic!&#x1F42F;
</a>
</div>
</li>
</ul>
<ul class="media-list">
<li class="media">
<div class="media-body">
<a href="/novel/vrmmo-the-unrivaled/vrtu-chapter-523">
VRMMO: The Unrivaled - Chapter 523: King of the Underground
</a>
</div>
</li>
</ul>
<ul class="media-list">
<li class="media">
<div class="media-body">
<a href="/novel/lord-of-all-realms/loar-chapter-1704">
Lord of All Realms - &#x1F37A;Chapter 1704: The Fortune And Rules of Heaven And Earth&#x1F37A;
</a>
</div>
</li>
</ul>
<ul class="media-list">
<li class="media">
<div class="media-body">
<a href="/novel/spirit-vessel/sv-chapter-809">
Spirit Vessel - Chapter 809: Late Ninth-level Heaven’s Mandate
</a>
</div>
</li>
</ul>
<ul class="media-list">
<li class="media">
<div class="media-body">
<a href="/novel/almighty-sword-domain/asd-chapter-776">
Almighty Sword Domain - Chapter 776 – Work Together?
</a>
</div>
</li>
</ul>
<ul class="media-list">
<li class="media">
<div class="media-body">
<a href="/novel/almighty-sword-domain/asd-chapter-775">
Almighty Sword Domain - Chapter 775 – The Heaven Dao Falls!
</a>
</div>
</li>
</ul>
<ul class="media-list">
<li class="media">
<div class="media-body">
<a href="/novel/genius-detective/gd-chapter-497">
Genius Detective - Chapter 497: Chen Shi&#x27;s Hypothesis
</a>
</div>
</li>
</ul>
<ul class="media-list">
<li class="media">
<div class="media-body">
<a href="/novel/phoenixs-requiem/pr-chapter-59">
Phoenix&#x27;s Requiem - Chapter 59: It’s Him!
</a>
</div>
</li>
</ul>
<ul class="media-list">
<li class="media">
<div class="media-body">
<a href="/novel/tomb-raider-king/trk-chapter-251">
Tomb Raider King - &#x1F451; Chapter 251: The Monarch’s Tomb (1) &#x1F451;
</a>
</div>
</li>
</ul>
<ul class="media-list">
<li class="media">
<div class="media-body">
<a href="/novel/emperors-domination/emperor-chapter-3313">
Emperor’s Domination - Chapter 3313: Ninety-nine
</a>
</div>
</li>
</ul>
<ul class="media-list">
<li class="media">
<div class="media-body">
<a href="/novel/emperors-domination/emperor-chapter-3312">
Emperor’s Domination - Chapter 3312: Difficult Climb
</a>
</div>
</li>
</ul>
<ul class="media-list">
<li class="media">
<div class="media-body">
<a href="/novel/necropolis-immortal/necro-chapter-441-2">
Necropolis Immortal - &#x1F409; Chapter 441.2: Hunting Lords
</a>
</div>
</li>
</ul>
<ul class="media-list">
<li class="media">
<div class="media-body">
<a href="/novel/rise/rise-chapter-170">
Rise - Chapter 170 - Marching Time Drew On, and Wore Him Numb
</a>
</div>
</li>
</ul>
<ul class="media-list">
<li class="media">
<div class="media-body">
<a href="/novel/martial-god-asura/mga-chapter-4557">
Martial God Asura - Chapter 4557: Destined For Greatness
</a>
</div>
</li>
</ul>
<ul class="media-list">
<li class="media">
<div class="media-body">
<a href="/novel/heavens-devourer/hd-chapter-1155">
Heaven&#x27;s Devourer - Chapter 1155: Nine-Starred Dragon&#x27;s Well
</a>
</div>
</li>
</ul>
<ul class="media-list">
<li class="media">
<div class="media-body">
<a href="/novel/tranxending-vision/tv-chapter-1018">
TranXending Vision - Chapter 1018 - Prisoner and Food
</a>
</div>
</li>
</ul>
<ul class="media-list">
<li class="media">
<div class="media-body">
<a href="/novel/immortal-devil-transformation/idt-chapter-521">
Immortal Devil Transformation - Book 12 Chapter 6 - Arrow Sounds Everywhere
</a>
</div>
</li>
</ul>
<ul class="media-list">
<li class="media">
<div class="media-body">
<a href="/novel/the-charm-of-soul-pets/tcosp-book-2-chapter-1673">
The Charm of Soul Pets - Chapter 1673: The Possessed Bai Yu
</a>
</div>
</li>
</ul>
</div>
</div>

<div id="placement-38" class="panel panel-default">
<div class="panel-heading">Sponsored Links</div>
<div><div class="AsGCtBHD" id="wuxiaworld_BTF2"></div></div>
<script id="remove-wuxiaworld_BTF2-AsGCtBHD" type="text/javascript">
        (function(id, type, placement) {
            var self = document.querySelector('#remove-' + id + '-AsGCtBHD');
            var el = document.querySelector('#' + id + '.AsGCtBHD');
            MainApp.devicedetection.checkAd(38, self, el, type, placement);
        })('wuxiaworld_BTF2', 'desktoptablet', 'sidebar');
    </script>
</div>
</div>
</div>
</div> 
</div>
</div>
<div class="footer">
<div class="container text-center">
<div style="font-size: 13px" class="col-xs-12 col-sm-5">
<div class="row">
<div class="col-xs-4 col-sm-4">
<a href="/page/contact-us">
<i style="color: #F7F7F7" class="fas fa-envelope fa-4x" data-fa-mask="fas fa-circle" data-fa-transform="shrink-6.0"></i>
</a>
<p>Contact Us</p>
</div>
<div class="col-xs-4 col-sm-4">
<a href="/page/terms-of-service-and-privacy-policy">
<i style="color: #F7F7F7" class="fas fa-lock fa-4x" data-fa-mask="fas fa-circle" data-fa-transform="shrink-6.0"></i>
</a>
<p>Privacy Policy</p>
</div>
<div class="col-xs-4 col-sm-4">
<a href="/feed">
<i style="color: #F7F7F7" class="fas fa-rss fa-4x" data-fa-mask="fas fa-circle" data-fa-transform="shrink-6.0"></i>
</a>
<p>RSS</p>
</div>
</div>
</div>
<div class="col-xs-12 col-sm-2">
<img class="hidden-xs" src="/images/vline.png" alt="line" />
<div class="visible-xs space15"></div>
<img class="visible-xs" src="/images/hline.png" alt="line" />
<div class="visible-xs space30"></div>
</div>
<div style="font-size: 13px" class="col-xs-12 col-sm-5">
<div class="row">
<div class="col-xs-4">
<a href="https://twitter.com/Wuxiaworld_Ltd" target="_blank" rel="noopener">
<i style="color: #F7F7F7" class="fab fa-twitter fa-4x" data-fa-mask="fas fa-circle" data-fa-transform="shrink-6.0"></i>
</a>
<p>Twitter</p>
</div>
<div class="col-xs-4">
<a href="https://www.facebook.com/WuxiaworldWebnovels/" target="_blank" rel="noopener">
<i style="color: #F7F7F7" class="fab fa-facebook-f fa-4x" data-fa-mask="fas fa-circle" data-fa-transform="shrink-6.0"></i>
</a>
<p>Facebook</p>
</div>
<div class="col-xs-4">
<a href=" https://discord.gg/wuxiaworld" target="_blank" rel="noopener">
<i style="color: #F7F7F7" class="fab fa-discord fa-4x" data-fa-mask="fas fa-circle" data-fa-transform="shrink-6.0"></i>
</a>
<p>Discord</p>
</div>
</div>
</div>
<div class="col-xs-12">
<p class="legal">Copyright &copy; 2018-2020 WuxiaWorld. All rights reserved.</p>
</div>
</div>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.2.4/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.23.0/moment.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/axios/0.18.0/axios.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>
<script src="/js/plugins.min.js?v=dwdxXIvyyPRHjCXCg_f8PErGAWlIR33Z0cXSCuS_wuc"></script>
<script src="/build/app/vendor.5345d6ae37fa9f0f455d.min.js"></script>
<script src="/build/app/runtime.c94739f1b98e73af2364.min.js"></script>
<script src="/build/app/app.e6bc5edb618e64073673.min.js"></script>
<script src="/build/app/chapter.7dc7b1777b0c82e2d533.min.js"></script>
<script src="/build/app/chapters.e0aa5ec7b6ef69dbca5c.min.js"></script>
<script type="text/javascript">
    var COMMENTS_SETTINGS = {"id":86813,"enabled":true,"maxDepth":8,"commentsPerPage":25,"defaultAvatar":"/images/profile.png"};
</script>
<script src="/build/app/comments.2e5cff6f413c68a2f091.min.js"></script>
</body>
</html>"""
print(chapter)
print(chapter.getContent2(html))