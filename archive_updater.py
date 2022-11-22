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
    # x = Novel('n6912eh', 'My Skills Are Too Strong to Be a Heroine')
    # x = Novel("1177354054882979595", "She Is a Quiet Girl, But a Noisy Telepath")
    # x = NovelPia(Novel('49942',"Omniscient First Person View "))
    # # x = x.updateObject()
    # print(type(x))
    # x.setLastChapter(0)
    # x.processNovel()

    # test_novelpia()
    test_novelpia2()

def test_novelpia2():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.firefox.options import Options
    from bs4 import BeautifulSoup

    gecko = os.path.normpath(os.path.join(os.path.dirname(__file__)+"/libs", 'geckodriver'))
    # binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')
    # driver = webdriver.Firefox(firefox_binary=binary, executable_path=gecko+'.exe')
    Options = Options()
    Options.headless = True
    driver = webdriver.Firefox( options=Options,executable_path=gecko+'.exe')
    driver.get("https://novelpia.com/viewer/351337")

    

def test_novelpia():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.firefox.options import Options
    from bs4 import BeautifulSoup

    gecko = os.path.normpath(os.path.join(os.path.dirname(__file__)+"/libs", 'geckodriver'))
    # binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')
    # driver = webdriver.Firefox(firefox_binary=binary, executable_path=gecko+'.exe')
    Options = Options()
    Options.headless = True
    driver = webdriver.Firefox( options=Options,executable_path=gecko+'.exe')
    driver.get("https://novelpia.com/novel/29912")
    # driver.execute_script('document.title')
    # print(driver)
    elem = driver.find_element(By.ID, "episode_list")
    # print(elem.get_attribute("innerHTML"))
    soup = BeautifulSoup(elem.get_attribute("innerHTML"), 'html.parser')
    print(soup)

    driver.close()
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
    parser.add_argument("-i", help="for a command line download input",
        type=str, default=argparse.SUPPRESS)  

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
            if hasattr(args, 'i'):
                print(args.i)
                download_cli(args.i)
            else: 
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

