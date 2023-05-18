# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.gridLayout_2 = QGridLayout(MainWindow)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_2 = QPushButton(MainWindow)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.pushButtonUpdate = QPushButton(MainWindow)
        self.pushButtonUpdate.setObjectName(u"pushButtonUpdate")

        self.horizontalLayout.addWidget(self.pushButtonUpdate)

        self.pushButton_3 = QPushButton(MainWindow)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout.addWidget(self.pushButton_3)


        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.LabelLocalProgress = QLabel(MainWindow)
        self.LabelLocalProgress.setObjectName(u"LabelLocalProgress")

        self.gridLayout_3.addWidget(self.LabelLocalProgress, 2, 0, 1, 1)

        self.LabelGlobalProgress = QLabel(MainWindow)
        self.LabelGlobalProgress.setObjectName(u"LabelGlobalProgress")

        self.gridLayout_3.addWidget(self.LabelGlobalProgress, 1, 0, 1, 1)

        self.progressBarGlobal = QProgressBar(MainWindow)
        self.progressBarGlobal.setObjectName(u"progressBarGlobal")
        self.progressBarGlobal.setValue(0)

        self.gridLayout_3.addWidget(self.progressBarGlobal, 1, 2, 1, 1)

        self.progressBarLocal = QProgressBar(MainWindow)
        self.progressBarLocal.setObjectName(u"progressBarLocal")
        self.progressBarLocal.setValue(0)

        self.gridLayout_3.addWidget(self.progressBarLocal, 2, 2, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_3, 3, 0, 1, 1)

        self.listWidget = QListWidget(MainWindow)
        self.listWidget.setObjectName(u"listWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButtonUpdate.setText(QCoreApplication.translate("MainWindow", u"update", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.LabelLocalProgress.setText(QCoreApplication.translate("MainWindow", u"Local Progress", None))
        self.LabelGlobalProgress.setText(QCoreApplication.translate("MainWindow", u"Global Progress", None))
    # retranslateUi

