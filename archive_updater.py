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

def option_download(args):
    keep_text_format=args.md
    if args.i:
        print(args.i)
        download_cli(args.i)
    else: 
        print("downloading")
        download(keep_text_format)
    

def option_update(args):
    keep_text_format=args.md
    regex=args.r
    archiveUpdate(findNovel(regex),keep_text_format)
       
def option_zip(args):
    regex=args.r
    out=args.o
    compressAll(regex,out)

def option_test(args):
    print("test")

def option_status():
    getFolderStatus()
    
    
def parser():
    parser = argparse.ArgumentParser(argument_default="--help")
    # parser.add_argument("mode",
    #     help="put the letter of argument c/d/s/u",
    #     type=str,
    #     default=argparse.SUPPRESS)
    subparsers = parser.add_subparsers()
    
    
    parser_download = subparsers.add_parser('download',aliases='d', help='download novels found in input.txt')
    parser_download.add_argument('-i', type=str, help='change data source to CLI (next arg should be a novel line code;name)')
    parser_download.add_argument('-md', action='store_true', help='change text format to html/md')
    parser_download.set_defaults(func=option_download)
    
    parser_update = subparsers.add_parser('update',aliases="u", help='update novel folders found in novel_list')
    parser_update.add_argument('-r', type=str, help='set a regex filtering the novels', default='')
    parser_update.add_argument('-md', action='store_true', help='change text format to html/md')
    parser_update.set_defaults(func=option_update)
    
    parser_zip = subparsers.add_parser('zip', help='zip help')
    parser_zip.add_argument('-o', type=str, help='output directory')
    parser_zip.add_argument('-r', type=str, help='set a regex filtering the novels', default='')
    parser_zip.set_defaults(func=option_zip)
    
    parser_zip = subparsers.add_parser('test',aliases="t", help='for development tests')
    parser_zip.set_defaults(func=option_test)
    
    parser_zip = subparsers.add_parser('status',aliases="s", help='set status of every local novel in csv file')
    parser_zip.set_defaults(func=option_status)
    
    
    args = parser.parse_args()
    print(args)
    if(hasattr(args,"func")):
        print(args.func(args))
    else :
        parser.print_help()
    
if __name__ == '__main__':
    check_env()
    parser()

