import sys
import os


# from PySide2.QtWidgets import QApplication, QWidget
# from PySide2.QtCore import QFile
# from PySide2.QtUiTools import QUiLoader

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget,  QListWidget, QVBoxLayout, QLabel, QPushButton, QListWidgetItem, \
    QHBoxLayout
#from regex import D
from src.main_functions import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.load_ui()
        self.init()

    def load_ui(self):
        uic.loadUi("forms/form.ui", self)
        styleSheetStr = str(open("./css/style.scss","r").read())
        self.setStyleSheet(styleSheetStr) 

    def init(self):
        print('init');
        self.populate_listview()
        self.pushButtonUpdate.clicked.connect(self.updateNovels)


    def populate_listview(self):
        novelList  = findNovel('')

        for novel in novelList:
            novelInfo = getNovelInfoFromFolderName(novel)
            novel=Novel(novelInfo[1],novelInfo[0],False)
            
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

    def updateNovels(self):
        print('updatesing')
        for novel in self.listWidget:
            pass


class ListItemFromUI(QWidget):
    def __init__(self,novel:Novel):
        super().__init__()
        self.novel = Novel;
        self.text = novel.titre
        uic.loadUi("forms/listItem.ui", self)
        self.init()

    def init(self):
        self.label_2.setText(self.text)




if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())

# app = QtWidgets.QApplication(sys.argv)

# window = uic.loadUi("form.ui")
# window.show()
# # app.exec()
# sys.exit(app.exec_())