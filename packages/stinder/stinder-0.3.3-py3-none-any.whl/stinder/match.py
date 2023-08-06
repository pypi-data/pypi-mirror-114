# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Match.ui'
##
## Created by: Qt User Interface Compiler version 6.1.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

from stinder.stinder_images_rc import *
from stinder.home import *

class Ui_LikeDialog(object):
    def setupUi(self, LikeDialog):
        if not LikeDialog.objectName():
            LikeDialog.setObjectName(u"LikeDialog")
        LikeDialog.resize(646, 457)
        LikeDialog.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(134, 179, 255, 255), stop:1 rgba(14, 103, 255, 255));\n"
"color: black;\n font:100 10px \"Nexa\";")
        self.MatchVerticalLayout = QVBoxLayout(LikeDialog)
        self.MatchVerticalLayout.setObjectName(u"MatchVerticalLayout")
        self.MatchTitle = QLabel(LikeDialog)
        self.MatchTitle.setObjectName(u"MatchTitle")
        font = QFont()
        font.setPointSize(60)
        font.setBold(True)
        font.setItalic(False)
        self.MatchTitle.setFont(font)
        self.MatchTitle.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"padding-top:24px;\n"
"font: 1000 60pt \"Nexa\";")
        self.MatchTitle.setScaledContents(True)
        self.MatchTitle.setAlignment(Qt.AlignCenter)

        self.MatchVerticalLayout.addWidget(self.MatchTitle)

        self.InfoLabel = QLabel(LikeDialog)
        self.InfoLabel.setObjectName(u"InfoLabel")
        self.InfoLabel.setLayoutDirection(Qt.LeftToRight)
        self.InfoLabel.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"font: 300 18pt \"Nexa\";")
        self.InfoLabel.setAlignment(Qt.AlignCenter)
        self.InfoLabel.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.MatchVerticalLayout.addWidget(self.InfoLabel)

        self.LogoImage = QLabel(LikeDialog)
        self.LogoImage.setObjectName(u"LogoImage")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LogoImage.sizePolicy().hasHeightForWidth())
        self.LogoImage.setSizePolicy(sizePolicy)
        self.LogoImage.setStyleSheet(u"padding: 30px 70px;\n"
"background-color: transparent;")
        self.LogoImage.setPixmap(QPixmap(u":/logo/images/stinder_book_logo.png"))
        self.LogoImage.setScaledContents(True)
        self.LogoImage.setAlignment(Qt.AlignCenter)
        self.LogoImage.setMargin(0)
        self.LogoImage.setIndent(-2)

        self.MatchVerticalLayout.addWidget(self.LogoImage, 0, Qt.AlignHCenter)

        self.buttonSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.MatchVerticalLayout.addItem(self.buttonSpacer)

        self.OKButton = QPushButton(LikeDialog, clicked=lambda: LikeDialog.close())
        self.OKButton.setObjectName(u"OKButton")
        self.OKButton.setStyleSheet(u"QPushButton{font: 500 13pt \"NexaBold\";\n"
"background-color: rgb(98, 214, 81);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 5px; border: 2px rgb(33, 33, 34);\n"
"border-bottom: 3px solid rgb(72, 156, 59);\n"
"border-left:  1px solid rgb(72, 156, 59);\n"
"border-right:  1px solid rgb(72, 156, 59);\n"
"padding: 6px;}\n QPushButton:hover{background-color: rgb(99, 255, 179); \n border-bottom: 3px solid rgb(45, 160, 104);\n border-left: 2px solid rgb(45, 160, 104);\n border-right: 2px solid rgb(45, 160, 104);}"
"QPushButton:pressed{background-color: rgb(30, 94, 31);\n border-bottom: 3px solid rgb(22, 50, 22);\n border-left: 2px solid rgb(22, 50, 22);\n border-right: 2px solid rgb(22, 50, 22);}")

        self.MatchVerticalLayout.addWidget(self.OKButton)


        self.retranslateUi(LikeDialog)

        QMetaObject.connectSlotsByName(LikeDialog)
    # setupUi

    def retranslateUi(self, LikeDialog):
        LikeDialog.setWindowTitle(QCoreApplication.translate("LikeDialog", u"Dialog", None))
        self.MatchTitle.setText(QCoreApplication.translate("LikeDialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:36pt;\">You've got a match!</span></p></body></html>", None))
        self.InfoLabel.setText(QCoreApplication.translate("LikeDialog", u"<html><head/><body><p align=\"center\">TextLabel</p></body></html>", None))
        self.LogoImage.setText("")
        self.OKButton.setText(QCoreApplication.translate("LikeDialog", u"OK", None))
    # retranslateUi