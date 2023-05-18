import sys

from src.Downloaders import Novel
from src.main_functions import *


class NovelController : 
    instance=None
    novel_list:list[Novel]
    
    @staticmethod
    def getInstance():
        if(NovelController.instance == None):
            return NovelController()
        return NovelController.instance
    
    def __init__(self) -> None:
        NovelController.instance = self
        self.listeners = []
        self.novel_list = []
        novelList  = findNovel('')
        for novel in novelList:
            novelInfo = getNovelInfoFromFolderName(novel)
            novel=Novel(novelInfo[1],novelInfo[0],False)
            self.novel_list.append(novel)
    
    def getNovelList(self):
        return self.novel_list
    
    def register(self,listener):
        self.listeners.append(listener)
    
    def fire_update_novel(self,count):
        for listener in self.listeners:
            listener.update_novel(count,len(self.novel_list))
    
    def update_novels(self):
        i=0
        for novel in self.novel_list:
            print("noovel",novel,i,len(self.novel_list))
            i+=1
            self.fire_update_novel(i)