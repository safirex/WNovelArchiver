import sys
import os

sys.path.append("src/gui")

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget,  QListWidget, QVBoxLayout, QLabel, QPushButton, QListWidgetItem, \
    QHBoxLayout
    
from src.main_functions import *
from controllers.NovelController import NovelController

class MainWindow(QWidget):
    listWidget:QListWidget
    
    def __init__(self):
        super().__init__()
        self.load_ui()
        self.init()

    def load_ui(self):
        uic.loadUi("src/gui/forms/form.ui", self)
        styleSheetStr = str(open("src/gui/css/style.scss","r").read())
        self.setStyleSheet(styleSheetStr) 

    def init(self):
        print('init')
        self.controller = NovelController.getInstance()
        self.controller.register(self)
        self.populate_listview()
        self.pushButtonUpdate.clicked.connect(self.controller.update_novels)


    def populate_listview(self):
        for novel in self.controller.getNovelList():
            
            # add item to the listview
            listItem = QListWidgetItem(self.listWidget)
            item_widget = ListItemFromUI(novel)
            listItem.setSizeHint(item_widget.sizeHint())
            self.listWidget.addItem(listItem)
            self.listWidget.setItemWidget(listItem, item_widget)
            
    def novel_update_notice(self,nb_novel,nb_novel_to_update):
        self.progressBarGlobal.setValue( nb_novel/nb_novel_to_update *100)

    def chapter_update_notice(self,nb_chap,nb_chap_to_update):
        self.progressBarLocal.setValue( nb_chap/nb_chap_to_update *100)

    def update_novel(self,count,max):
        self.progressBarGlobal.setValue( count/max *100)



class ListItemFromUI(QWidget):
    def __init__(self,novel:Novel):
        super().__init__()
        self.novel = novel
        self.text = novel.titre
        
        uic.loadUi("src/gui/forms/listItem.ui", self)
        self.init()

    def init(self):
        self.label_2.setText(self.text)
        self.label.setText("test")

