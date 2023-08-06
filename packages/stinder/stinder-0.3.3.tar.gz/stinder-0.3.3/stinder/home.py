# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Home.ui'
##
## Created by: Qt User Interface Compiler version 6.1.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

import os
import sqlite3

from pkg_resources import resource_filename

from PySide6 import QtWidgets
import numpy
from os import linesep
from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

from stinder.match import *

from stinder.stinder_images_rc import *

class Ui_Stinder(object):
    def __init__(self):
        self.counter = 0
        self.students = []
        self.s_length = 0
        self.c_user = []
        
        self.matchWindow = QDialog()
        self.matchUi = Ui_LikeDialog()
        self.matchUi.setupUi(self.matchWindow)

        self.matches = []
        self.m_length = 0
        self.m_counter = 0

    def setupUi(self, Stinder):
        self.students, self.s_length = self.list()
        if not Stinder.objectName():
            Stinder.setObjectName(u"Stinder")
        Stinder.resize(903, 641)
        Stinder.setAutoFillBackground(False)
        Stinder.setStyleSheet(u"background-color:qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(56, 0, 83, 255), stop:1 rgba(75, 0, 149, 255))")
        Stinder.setAnimated(True)
        self.actionTemp_Button = QAction(Stinder)
        self.actionTemp_Button.setObjectName(u"actionTemp_Button")
        self.actionTemp_Button_2 = QAction(Stinder)
        self.actionTemp_Button_2.setObjectName(u"actionTemp_Button_2")
        self.actionTemp_Button_3 = QAction(Stinder)
        self.actionTemp_Button_3.setObjectName(u"actionTemp_Button_3")
        self.centralwidget = QWidget(Stinder)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setStyleSheet(u"background-color:rgb(33, 33, 34)")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.ProfileButton = QPushButton(self.frame_2, clicked=lambda: self.likes_counter())
        self.ProfileButton.setObjectName(u"ProfileButton")
        self.ProfileButton.setStyleSheet(u"QPushButton{font: 500 13pt \"Nexa Bold\";\n"
"background-color: rgb(98, 214, 81);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 5px; border: 2px rgb(33, 33, 34);\n"
"border-bottom: 3px solid rgb(72, 156, 59);\n"
"border-left:  1px solid rgb(72, 156, 59);\n"
"border-right:  1px solid rgb(72, 156, 59);\n"
"padding: 6px;}\n QPushButton:hover{background-color: rgb(99, 255, 179); \n border-bottom: 3px solid rgb(45, 160, 104);\n border-left: 2px solid rgb(45, 160, 104);\n border-right: 2px solid rgb(45, 160, 104);}"
"QPushButton:pressed{background-color: rgb(30, 94, 31);\n border-bottom: 3px solid rgb(22, 50, 22);\n border-left: 2px solid rgb(22, 50, 22);\n border-right: 2px solid rgb(22, 50, 22);}")

        self.gridLayout.addWidget(self.ProfileButton, 2, 0, 1, 1)

        self.BrowseButton = QPushButton(self.frame_2, clicked=lambda: self.handleAlgo())
        self.BrowseButton.setObjectName(u"BrowseButton")
        self.BrowseButton.setStyleSheet(u"QPushButton{font: 500 13pt \"Nexa Bold\";\n"
"background-color: rgb(98, 214, 81);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 5px; border: 2px rgb(33, 33, 34);\n"
"border-bottom: 3px solid rgb(72, 156, 59);\n"
"border-left:  1px solid rgb(72, 156, 59);\n"
"border-right:  1px solid rgb(72, 156, 59);\n"
"padding: 6px;}\n QPushButton:hover{background-color: rgb(99, 255, 179); \n border-bottom: 3px solid rgb(45, 160, 104);\n border-left: 2px solid rgb(45, 160, 104);\n border-right: 2px solid rgb(45, 160, 104);}"
"QPushButton:pressed{background-color: rgb(30, 94, 31);\n border-bottom: 3px solid rgb(22, 50, 22);\n border-left: 2px solid rgb(22, 50, 22);\n border-right: 2px solid rgb(22, 50, 22);}")

        self.gridLayout.addWidget(self.BrowseButton, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 3, 0, 1, 1)

        self.logo = QLabel(self.frame_2)
        self.logo.setObjectName(u"logo")
        self.logo.setMinimumSize(QSize(81, 41))
        self.logo.setMaximumSize(QSize(120, 42))
        self.logo.setPixmap(QPixmap(u":/logo/images/stinder_logo.png"))
        self.logo.setScaledContents(True)

        self.gridLayout.addWidget(self.logo, 4, 0, 1, 1)

        self.AboutButton = QPushButton(self.frame_2)
        self.AboutButton.setObjectName(u"AboutButton")
        self.AboutButton.setStyleSheet(u"QPushButton{font: 500 13pt \"Nexa Bold\";\n"
"background-color: rgb(98, 214, 81);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 5px; border: 2px rgb(33, 33, 34);\n"
"border-bottom: 3px solid rgb(72, 156, 59);\n"
"border-left:  1px solid rgb(72, 156, 59);\n"
"border-right:  1px solid rgb(72, 156, 59);\n"
"padding: 6px;}\n QPushButton:hover{background-color: rgb(99, 255, 179); \n border-bottom: 3px solid rgb(45, 160, 104);\n border-left: 2px solid rgb(45, 160, 104);\n border-right: 2px solid rgb(45, 160, 104);}"
"QPushButton:pressed{background-color: rgb(30, 94, 31);\n border-bottom: 3px solid rgb(22, 50, 22);\n border-left: 2px solid rgb(22, 50, 22);\n border-right: 2px solid rgb(22, 50, 22);}")

        self.gridLayout.addWidget(self.AboutButton, 0, 0, 1, 1)

        self.LogoutBtn = QPushButton(self.frame_2)
        self.LogoutBtn.setObjectName(u"LogoutBtn")
        self.LogoutBtn.setStyleSheet(u"QPushButton{font: 500 13pt \"Nexa Bold\";\n"
"background-color: rgb(98, 214, 81);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 5px; border: 2px rgb(33, 33, 34);\n"
"border-bottom: 3px solid rgb(72, 156, 59);\n"
"border-left:  1px solid rgb(72, 156, 59);\n"
"border-right:  1px solid rgb(72, 156, 59);\n"
"padding: 6px;}\n QPushButton:hover{background-color: rgb(99, 255, 179); \n border-bottom: 3px solid rgb(45, 160, 104);\n border-left: 2px solid rgb(45, 160, 104);\n border-right: 2px solid rgb(45, 160, 104);}"
"QPushButton:pressed{background-color: rgb(30, 94, 31);\n border-bottom: 3px solid rgb(22, 50, 22);\n border-left: 2px solid rgb(22, 50, 22);\n border-right: 2px solid rgb(22, 50, 22);}")

        self.gridLayout.addWidget(self.LogoutBtn, 3, 0, 1, 1, Qt.AlignTop)

        self.gridLayout_2.addWidget(self.frame_2, 0, 0, 1, 1)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.AboutPage = QWidget()
        self.AboutPage.setObjectName(u"AboutPage")
        self.gridLayout_31 = QGridLayout(self.AboutPage)
        self.gridLayout_31.setObjectName(u"gridLayout_31")
        self.aboutouterframe = QFrame(self.AboutPage)
        self.aboutouterframe.setObjectName(u"aboutouterframe")
        self.aboutouterframe.setStyleSheet(u"background-color: transparent;")
        self.aboutouterframe.setFrameShape(QFrame.StyledPanel)
        self.aboutouterframe.setFrameShadow(QFrame.Raised)
        self.gridLayout_10 = QGridLayout(self.aboutouterframe)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.aboutinnerframe = QFrame(self.aboutouterframe)
        self.aboutinnerframe.setObjectName(u"aboutinnerframe")
        self.aboutinnerframe.setMinimumSize(QSize(250, 150))
        self.aboutinnerframe.setFrameShape(QFrame.StyledPanel)
        self.aboutinnerframe.setFrameShadow(QFrame.Raised)
        self.gridLayout_11 = QGridLayout(self.aboutinnerframe)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setVerticalSpacing(6)
        self.gridLayout_11.setContentsMargins(-1, 0, -1, -1)
        self.aboutlogo = QLabel(self.aboutinnerframe)
        self.aboutlogo.setObjectName(u"aboutlogo")
        self.aboutlogo.setMinimumSize(QSize(240, 120))
        self.aboutlogo.setMaximumSize(QSize(81, 41))
        self.aboutlogo.setPixmap(QPixmap(u":/logo/images/stinder_logo.png"))
        self.aboutlogo.setScaledContents(True)

        self.gridLayout_11.addWidget(self.aboutlogo, 0, 1, 1, 1)

        self.horizSpacerLogoRight = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_11.addItem(self.horizSpacerLogoRight, 0, 2, 1, 1)

        self.horizSpacerLogoLeft = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_11.addItem(self.horizSpacerLogoLeft, 0, 0, 1, 1)


        self.gridLayout_10.addWidget(self.aboutinnerframe, 0, 0, 1, 1)

        self.aboutscroll = QScrollArea(self.aboutouterframe)
        self.aboutscroll.setObjectName(u"aboutscroll")
        self.aboutscroll.setMinimumSize(QSize(600, 450))
        self.aboutscroll.setStyleSheet("""QScrollBar:vertical {
	border: none;
    background: rgb(45, 45, 68);
    width: 15px;
    margin: 16px 0 16px 0;
 }
QScrollBar::handle:vertical {	
	background-color: rgb(33, 33, 34);
	border-radius: 4px;
	min-height: 10px;
}
QScrollBar::handle:vertical:hover{	
	background-color:  rgb(98, 214, 81);
}
QScrollBar::handle:vertical:pressed {	
	background-color: rgb(24, 24, 32);
}
QScrollBar::sub-line:vertical {
     border: none;
     background: none;
}
QScrollBar::add-line:vertical {
    border: none;
    background: none;
}
QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
	background: none;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
	background: none;
}
""")
        self.aboutscroll.setFrameShape(QFrame.Box)
        self.aboutscroll.setFrameShadow(QFrame.Plain)
        self.aboutscroll.setLineWidth(5)
        self.aboutscroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.aboutscroll.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, -2468, 724, 3030))
        self.gridLayout_12 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.AboutTextP2 = QFrame(self.scrollAreaWidgetContents)
        self.AboutTextP2.setObjectName(u"AboutTextP2")
        self.AboutTextP2.setFrameShape(QFrame.StyledPanel)
        self.AboutTextP2.setFrameShadow(QFrame.Raised)
        self.gridLayout_13 = QGridLayout(self.AboutTextP2)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setVerticalSpacing(0)
        self.horizSpacerAT2Left = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_13.addItem(self.horizSpacerAT2Left, 0, 0, 1, 1)

        self.abouttextp2 = QLabel(self.AboutTextP2)
        self.abouttextp2.setObjectName(u"abouttextp2")
        self.abouttextp2.setStyleSheet(u"font: 500 13pt \"Nexa\";")

        self.gridLayout_13.addWidget(self.abouttextp2, 0, 1, 1, 1)

        self.horizSpacerAT2Right = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_13.addItem(self.horizSpacerAT2Right, 0, 2, 1, 1)


        self.gridLayout_12.addWidget(self.AboutTextP2, 2, 0, 1, 1)

        self.FAQsFrame = QFrame(self.scrollAreaWidgetContents)
        self.FAQsFrame.setObjectName(u"FAQsFrame")
        self.FAQsFrame.setFrameShape(QFrame.StyledPanel)
        self.FAQsFrame.setFrameShadow(QFrame.Raised)
        self.gridLayout_14 = QGridLayout(self.FAQsFrame)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.horizSpacerFAQRight = QSpacerItem(154, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_14.addItem(self.horizSpacerFAQRight, 0, 2, 1, 1)

        self.horizSpacerFAQLeft = QSpacerItem(155, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_14.addItem(self.horizSpacerFAQLeft, 0, 0, 1, 1)

        self.FAQsText = QLabel(self.FAQsFrame)
        self.FAQsText.setObjectName(u"FAQsText")
        self.FAQsText.setMinimumSize(QSize(0, 0))
        self.FAQsText.setStyleSheet(u"font: 500 13pt \"Nexa Bold\";")
        self.FAQsText.setFrameShape(QFrame.NoFrame)
        self.FAQsText.setFrameShadow(QFrame.Plain)
        self.FAQsText.setLineWidth(4)
        self.FAQsText.setMidLineWidth(0)
        self.FAQsText.setTextFormat(Qt.RichText)
        self.FAQsText.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_14.addWidget(self.FAQsText, 0, 1, 1, 1)


        self.gridLayout_12.addWidget(self.FAQsFrame, 4, 0, 1, 1)

        self.TeamSectionFrame = QFrame(self.scrollAreaWidgetContents)
        self.TeamSectionFrame.setObjectName(u"TeamSectionFrame")
        self.TeamSectionFrame.setFrameShape(QFrame.StyledPanel)
        self.TeamSectionFrame.setFrameShadow(QFrame.Raised)
        self.gridLayout_21 = QGridLayout(self.TeamSectionFrame)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.horizSpacerTSLeft = QSpacerItem(115, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_21.addItem(self.horizSpacerTSLeft, 0, 0, 1, 1)

        self.horizSpacerTSRight = QSpacerItem(114, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_21.addItem(self.horizSpacerTSRight, 0, 2, 1, 1)

        self.TSText = QLabel(self.TeamSectionFrame)
        self.TSText.setObjectName(u"TSText")
        self.TSText.setStyleSheet(u"font: 500 13pt \"Nexa Bold\";")

        self.gridLayout_21.addWidget(self.TSText, 0, 1, 1, 1)


        self.gridLayout_12.addWidget(self.TeamSectionFrame, 11, 0, 1, 1)

        self.AboutTextP3 = QFrame(self.scrollAreaWidgetContents)
        self.AboutTextP3.setObjectName(u"AboutTextP3")
        self.AboutTextP3.setStyleSheet(u"font: 500 13pt \"Nexa\";")
        self.AboutTextP3.setFrameShape(QFrame.StyledPanel)
        self.AboutTextP3.setFrameShadow(QFrame.Raised)
        self.gridLayout_15 = QGridLayout(self.AboutTextP3)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setVerticalSpacing(0)
        self.horizSpacerAT3Left = QSpacerItem(89, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_15.addItem(self.horizSpacerAT3Left, 0, 0, 1, 1)

        self.abouttextp3 = QLabel(self.AboutTextP3)
        self.abouttextp3.setObjectName(u"abouttextp3")
        self.abouttextp3.setMinimumSize(QSize(0, 0))

        self.gridLayout_15.addWidget(self.abouttextp3, 0, 2, 1, 1)

        self.horizSpacerAT3Right = QSpacerItem(88, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_15.addItem(self.horizSpacerAT3Right, 0, 3, 1, 1)


        self.gridLayout_12.addWidget(self.AboutTextP3, 3, 0, 1, 1)

        self.Question6Frame = QFrame(self.scrollAreaWidgetContents)
        self.Question6Frame.setObjectName(u"Question6Frame")
        self.Question6Frame.setFrameShape(QFrame.StyledPanel)
        self.Question6Frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_20 = QGridLayout(self.Question6Frame)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.horizSpacerQ6Left = QSpacerItem(80, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_20.addItem(self.horizSpacerQ6Left, 0, 0, 1, 1)

        self.Q6Text = QLabel(self.Question6Frame)
        self.Q6Text.setObjectName(u"Q6Text")
        self.Q6Text.setMinimumSize(QSize(0, 0))
        self.Q6Text.setStyleSheet(u"font: 500 13pt \"Nexa\";")

        self.gridLayout_20.addWidget(self.Q6Text, 0, 1, 1, 1)

        self.horizSpacerQ6Right = QSpacerItem(67, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_20.addItem(self.horizSpacerQ6Right, 0, 2, 1, 1)


        self.gridLayout_12.addWidget(self.Question6Frame, 10, 0, 1, 1)

        self.Question2Frame = QFrame(self.scrollAreaWidgetContents)
        self.Question2Frame.setObjectName(u"Question2Frame")
        self.Question2Frame.setFrameShape(QFrame.StyledPanel)
        self.Question2Frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_16 = QGridLayout(self.Question2Frame)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.horizSpacerQ2Left = QSpacerItem(76, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_16.addItem(self.horizSpacerQ2Left, 0, 0, 1, 1)

        self.Q2Text = QLabel(self.Question2Frame)
        self.Q2Text.setObjectName(u"Q2Text")
        self.Q2Text.setStyleSheet(u"font: 500 13pt \"Nexa\";")

        self.gridLayout_16.addWidget(self.Q2Text, 0, 1, 1, 1)

        self.horizSpacerQ2Right = QSpacerItem(75, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_16.addItem(self.horizSpacerQ2Right, 0, 2, 1, 1)


        self.gridLayout_12.addWidget(self.Question2Frame, 6, 0, 1, 1)

        self.TeamMemberP1_EG = QFrame(self.scrollAreaWidgetContents)
        self.TeamMemberP1_EG.setObjectName(u"TeamMemberP1_EG")
        self.TeamMemberP1_EG.setFrameShape(QFrame.StyledPanel)
        self.TeamMemberP1_EG.setFrameShadow(QFrame.Raised)
        self.gridLayout_22 = QGridLayout(self.TeamMemberP1_EG)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.EG_ProfilePic = QLabel(self.TeamMemberP1_EG)
        self.EG_ProfilePic.setObjectName(u"EG_ProfilePic")
        self.EG_ProfilePic.setMaximumSize(QSize(256, 256))
        self.EG_ProfilePic.setPixmap(QPixmap(u":/logo/images/eg_pfp.jpg"))
        self.EG_ProfilePic.setScaledContents(True)

        self.gridLayout_22.addWidget(self.EG_ProfilePic, 0, 1, 1, 1)

        self.horizSpacerP1_EGLeft = QSpacerItem(113, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_22.addItem(self.horizSpacerP1_EGLeft, 0, 0, 1, 1)

        self.horizSpacerP1_EGRight = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_22.addItem(self.horizSpacerP1_EGRight, 0, 4, 1, 1)

        self.EG_NameRoleAnswer = QLabel(self.TeamMemberP1_EG)
        self.EG_NameRoleAnswer.setObjectName(u"EG_NameRoleAnswer")
        self.EG_NameRoleAnswer.setMinimumSize(QSize(256, 256))
        self.EG_NameRoleAnswer.setStyleSheet(u"font: 500 13pt \"Nexa\";")

        self.gridLayout_22.addWidget(self.EG_NameRoleAnswer, 0, 3, 1, 1)

        self.horizSpacerP1_EGCenter = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_22.addItem(self.horizSpacerP1_EGCenter, 0, 2, 1, 1)


        self.gridLayout_12.addWidget(self.TeamMemberP1_EG, 12, 0, 1, 1)

        self.TeamMemberP2_WT = QFrame(self.scrollAreaWidgetContents)
        self.TeamMemberP2_WT.setObjectName(u"TeamMemberP2_WT")
        self.TeamMemberP2_WT.setFrameShape(QFrame.StyledPanel)
        self.TeamMemberP2_WT.setFrameShadow(QFrame.Raised)
        self.gridLayout_23 = QGridLayout(self.TeamMemberP2_WT)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.WT_NameRoleAnswer = QLabel(self.TeamMemberP2_WT)
        self.WT_NameRoleAnswer.setObjectName(u"WT_NameRoleAnswer")
        self.WT_NameRoleAnswer.setMinimumSize(QSize(256, 256))
        self.WT_NameRoleAnswer.setMaximumSize(QSize(256, 256))
        self.WT_NameRoleAnswer.setStyleSheet(u"font: 500 13pt \"Nexa\";")

        self.gridLayout_23.addWidget(self.WT_NameRoleAnswer, 0, 1, 1, 1)

        self.WT_ProfilePic = QLabel(self.TeamMemberP2_WT)
        self.WT_ProfilePic.setObjectName(u"WT_ProfilePic")
        self.WT_ProfilePic.setMinimumSize(QSize(0, 0))
        self.WT_ProfilePic.setMaximumSize(QSize(256, 256))
        self.WT_ProfilePic.setPixmap(QPixmap(u":/logo/images/wt-profile.png"))
        self.WT_ProfilePic.setScaledContents(True)

        self.gridLayout_23.addWidget(self.WT_ProfilePic, 0, 3, 1, 1)

        self.horizSpacerP2_WTRight = QSpacerItem(45, 253, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_23.addItem(self.horizSpacerP2_WTRight, 0, 5, 1, 1)

        self.horizSpacerP2_WTLeft = QSpacerItem(46, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_23.addItem(self.horizSpacerP2_WTLeft, 0, 0, 1, 1)

        self.horizSpacerP2_EGCenter = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_23.addItem(self.horizSpacerP2_EGCenter, 0, 2, 1, 1)


        self.gridLayout_12.addWidget(self.TeamMemberP2_WT, 13, 0, 1, 1)

        self.Question5Frame = QFrame(self.scrollAreaWidgetContents)
        self.Question5Frame.setObjectName(u"Question5Frame")
        self.Question5Frame.setFrameShape(QFrame.StyledPanel)
        self.Question5Frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_19 = QGridLayout(self.Question5Frame)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.horizSpacerQ5Left = QSpacerItem(80, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_19.addItem(self.horizSpacerQ5Left, 0, 0, 1, 1)

        self.Q5Text = QLabel(self.Question5Frame)
        self.Q5Text.setObjectName(u"Q5Text")
        self.Q5Text.setMinimumSize(QSize(0, 0))
        self.Q5Text.setStyleSheet(u"font: 500 13pt \"Nexa\";")

        self.gridLayout_19.addWidget(self.Q5Text, 0, 1, 1, 1)

        self.horizSpacerQ5Right = QSpacerItem(78, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_19.addItem(self.horizSpacerQ5Right, 0, 2, 1, 1)


        self.gridLayout_12.addWidget(self.Question5Frame, 9, 0, 1, 1)

        self.Question3Frame = QFrame(self.scrollAreaWidgetContents)
        self.Question3Frame.setObjectName(u"Question3Frame")
        self.Question3Frame.setFrameShape(QFrame.StyledPanel)
        self.Question3Frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_17 = QGridLayout(self.Question3Frame)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.horizSpacerQ3Left = QSpacerItem(53, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_17.addItem(self.horizSpacerQ3Left, 0, 0, 1, 1)

        self.Q3Text = QLabel(self.Question3Frame)
        self.Q3Text.setObjectName(u"Q3Text")
        self.Q3Text.setStyleSheet(u"font: 500 13pt \"Nexa\";")

        self.gridLayout_17.addWidget(self.Q3Text, 0, 1, 1, 1)

        self.horizSpacerQ3Right = QSpacerItem(53, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_17.addItem(self.horizSpacerQ3Right, 0, 2, 1, 1)


        self.gridLayout_12.addWidget(self.Question3Frame, 7, 0, 1, 1)

        self.TeamMemberP3_CE = QFrame(self.scrollAreaWidgetContents)
        self.TeamMemberP3_CE.setObjectName(u"TeamMemberP3_CE")
        self.TeamMemberP3_CE.setFrameShape(QFrame.StyledPanel)
        self.TeamMemberP3_CE.setFrameShadow(QFrame.Raised)
        self.gridLayout_24 = QGridLayout(self.TeamMemberP3_CE)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.CE_ProfilePic = QLabel(self.TeamMemberP3_CE)
        self.CE_ProfilePic.setObjectName(u"CE_ProfilePic")
        self.CE_ProfilePic.setMaximumSize(QSize(256, 256))
        self.CE_ProfilePic.setPixmap(QPixmap(u":/logo/images/ce-profile.jpg"))
        self.CE_ProfilePic.setScaledContents(True)

        self.gridLayout_24.addWidget(self.CE_ProfilePic, 0, 1, 1, 1)

        self.horizSpacerP3_CELeft = QSpacerItem(62, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_24.addItem(self.horizSpacerP3_CELeft, 0, 0, 1, 1)

        self.horizSpacerP3_CERight = QSpacerItem(61, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_24.addItem(self.horizSpacerP3_CERight, 0, 4, 1, 1)

        self.CE_NameRoleAnswer = QLabel(self.TeamMemberP3_CE)
        self.CE_NameRoleAnswer.setObjectName(u"CE_NameRoleAnswer")
        self.CE_NameRoleAnswer.setStyleSheet(u"font: 500 13pt \"Nexa\";")

        self.gridLayout_24.addWidget(self.CE_NameRoleAnswer, 0, 3, 1, 1)

        self.horizSpacerP3_CECenter = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_24.addItem(self.horizSpacerP3_CECenter, 0, 2, 1, 1)


        self.gridLayout_12.addWidget(self.TeamMemberP3_CE, 14, 0, 1, 1)

        self.MissionStatementFrame = QFrame(self.scrollAreaWidgetContents)
        self.MissionStatementFrame.setObjectName(u"MissionStatementFrame")
        self.MissionStatementFrame.setMinimumSize(QSize(0, 0))
        self.MissionStatementFrame.setFrameShape(QFrame.StyledPanel)
        self.MissionStatementFrame.setFrameShadow(QFrame.Raised)
        self.gridLayout_18 = QGridLayout(self.MissionStatementFrame)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_18.setVerticalSpacing(0)
        self.horizSpacerMSRight = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_18.addItem(self.horizSpacerMSRight, 0, 2, 1, 1)

        self.horizspacerMSLeft = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_18.addItem(self.horizspacerMSLeft, 0, 0, 1, 1)

        self.MissionStatement = QLabel(self.MissionStatementFrame)
        self.MissionStatement.setObjectName(u"MissionStatement")
        self.MissionStatement.setMinimumSize(QSize(0, 0))
        self.MissionStatement.setStyleSheet(u"font: 500 13pt \"Nexa Bold\";")
        self.MissionStatement.setFrameShape(QFrame.NoFrame)
        self.MissionStatement.setFrameShadow(QFrame.Plain)
        self.MissionStatement.setLineWidth(1)
        self.MissionStatement.setMidLineWidth(0)
        self.MissionStatement.setTextFormat(Qt.RichText)
        self.MissionStatement.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_18.addWidget(self.MissionStatement, 0, 1, 1, 1)


        self.gridLayout_12.addWidget(self.MissionStatementFrame, 0, 0, 1, 1)

        self.AboutTextP1 = QFrame(self.scrollAreaWidgetContents)
        self.AboutTextP1.setObjectName(u"AboutTextP1")
        self.AboutTextP1.setFrameShape(QFrame.StyledPanel)
        self.AboutTextP1.setFrameShadow(QFrame.Raised)
        self.gridLayout_25 = QGridLayout(self.AboutTextP1)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.gridLayout_25.setVerticalSpacing(9)
        self.horizSpacerAT1Right = QSpacerItem(36, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_25.addItem(self.horizSpacerAT1Right, 0, 0, 1, 1)

        self.horizSpacerAT1Left = QSpacerItem(36, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_25.addItem(self.horizSpacerAT1Left, 0, 2, 1, 1)

        self.abouttextp1 = QLabel(self.AboutTextP1)
        self.abouttextp1.setObjectName(u"abouttextp1")
        self.abouttextp1.setMinimumSize(QSize(0, 0))
        self.abouttextp1.setStyleSheet(u"font: 500 13pt \"Nexa\";")
        self.abouttextp1.setScaledContents(False)

        self.gridLayout_25.addWidget(self.abouttextp1, 0, 1, 1, 1)


        self.gridLayout_12.addWidget(self.AboutTextP1, 1, 0, 1, 1)

        self.Question4Frame = QFrame(self.scrollAreaWidgetContents)
        self.Question4Frame.setObjectName(u"Question4Frame")
        self.Question4Frame.setFrameShape(QFrame.StyledPanel)
        self.Question4Frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_26 = QGridLayout(self.Question4Frame)
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.horizSpacerQ4Left = QSpacerItem(80, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_26.addItem(self.horizSpacerQ4Left, 0, 0, 1, 1)

        self.Q4Text = QLabel(self.Question4Frame)
        self.Q4Text.setObjectName(u"Q4Text")
        self.Q4Text.setStyleSheet(u"font: 500 13pt \"Nexa\";")

        self.gridLayout_26.addWidget(self.Q4Text, 0, 1, 1, 1)

        self.horizSpacerQ4Right = QSpacerItem(29, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_26.addItem(self.horizSpacerQ4Right, 0, 2, 1, 1)


        self.gridLayout_12.addWidget(self.Question4Frame, 8, 0, 1, 1)

        self.Question1Frame = QFrame(self.scrollAreaWidgetContents)
        self.Question1Frame.setObjectName(u"Question1Frame")
        self.Question1Frame.setFrameShape(QFrame.StyledPanel)
        self.Question1Frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_27 = QGridLayout(self.Question1Frame)
        self.gridLayout_27.setObjectName(u"gridLayout_27")
        self.horizSpacerQ1Left = QSpacerItem(84, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_27.addItem(self.horizSpacerQ1Left, 0, 0, 1, 1)

        self.Q1Text = QLabel(self.Question1Frame)
        self.Q1Text.setObjectName(u"Q1Text")
        self.Q1Text.setStyleSheet(u"font: 500 13pt \"Nexa\";")

        self.gridLayout_27.addWidget(self.Q1Text, 0, 1, 1, 1)

        self.horizSpacerQ1Right = QSpacerItem(84, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_27.addItem(self.horizSpacerQ1Right, 0, 2, 1, 1)


        self.gridLayout_12.addWidget(self.Question1Frame, 5, 0, 1, 1)

        self.TeamMemberP4_AD = QFrame(self.scrollAreaWidgetContents)
        self.TeamMemberP4_AD.setObjectName(u"TeamMemberP4_AD")
        self.TeamMemberP4_AD.setFrameShape(QFrame.StyledPanel)
        self.TeamMemberP4_AD.setFrameShadow(QFrame.Raised)
        self.gridLayout_28 = QGridLayout(self.TeamMemberP4_AD)
        self.gridLayout_28.setObjectName(u"gridLayout_28")
        self.horizSpacerP4_ADRight = QSpacerItem(177, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_28.addItem(self.horizSpacerP4_ADRight, 0, 0, 1, 1)

        self.AD_ProfilePic = QLabel(self.TeamMemberP4_AD)
        self.AD_ProfilePic.setObjectName(u"AD_ProfilePic")
        self.AD_ProfilePic.setMaximumSize(QSize(256, 256))
        self.AD_ProfilePic.setPixmap(QPixmap(u":/logo/images/AD-profile.png"))
        self.AD_ProfilePic.setScaledContents(True)

        self.gridLayout_28.addWidget(self.AD_ProfilePic, 0, 3, 1, 1)

        self.AD_NameRoleAnswer = QLabel(self.TeamMemberP4_AD)
        self.AD_NameRoleAnswer.setObjectName(u"AD_NameRoleAnswer")
        self.AD_NameRoleAnswer.setMaximumSize(QSize(256, 256))
        self.AD_NameRoleAnswer.setStyleSheet(u"font: 500 13pt \"Nexa\";")

        self.gridLayout_28.addWidget(self.AD_NameRoleAnswer, 0, 1, 1, 1)

        self.horizSpacerP4_ADLeft = QSpacerItem(176, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_28.addItem(self.horizSpacerP4_ADLeft, 0, 4, 1, 1)

        self.horizSpacerP4_ADCenter = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_28.addItem(self.horizSpacerP4_ADCenter, 0, 2, 1, 1)


        self.gridLayout_12.addWidget(self.TeamMemberP4_AD, 15, 0, 1, 1)

        self.aboutscroll.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_10.addWidget(self.aboutscroll, 1, 0, 1, 1)


        self.gridLayout_31.addWidget(self.aboutouterframe, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.AboutPage)
        self.BrowsePage = QWidget()
        self.BrowsePage.setObjectName(u"BrowsePage")
        self.gridLayout_4 = QGridLayout(self.BrowsePage)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_5, 1, 0, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_6, 1, 2, 1, 1)

        self.frame_4 = QFrame(self.BrowsePage)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 0))
        self.frame_4.setMaximumSize(QSize(1200, 600))
        self.frame_4.setBaseSize(QSize(0, 0))
        self.frame_4.setStyleSheet(u"background-color: transparent;")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.frame_7 = QFrame(self.frame_4)
        self.frame_7.setObjectName(u"frame_7")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy)
        self.frame_7.setMinimumSize(QSize(600, 350))
        self.frame_7.setStyleSheet(u"border-radius: 15px;\n"
"border-top: 2px solid rgb(73, 73, 75);\n"
"border-left: 2px solid rgb(73, 73, 75);\n"
"background-color:rgb(33, 33, 34);\n"
"padding: 10px;\n"
"border-bottom: 4px solid rgb(222, 221, 223);\n"
"border-right:  4px solid rgb(222, 221, 223);")
        self.frame_7.setFrameShape(QFrame.Box)
        self.frame_7.setFrameShadow(QFrame.Plain)
        self.frame_7.setLineWidth(15)
        self.frame_7.setMidLineWidth(22)

        self.verticalLayout_3 = QVBoxLayout(self.frame_7)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetFixedSize)
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetMaximumSize)

        self.Discover_FirstName = QLabel(self.frame_7)
        self.Discover_FirstName.setObjectName(u"Discover_FirstName")
        self.Discover_FirstName.setMinimumSize(QSize(189, 42))
        self.Discover_FirstName.setStyleSheet(u"color: white; \n"
"font: 1000 60pt \"Nexa\";\n"
"background-color: rgb(97, 165, 85);\n"
"padding:0px;\n"
"\n"
"border-top: 0px solid rgb(125, 125, 125);\n"
"border-left :0px;\n"
"border-right:0px;\n"
"border-bottom:0px;\n"
"\n"
"background-color:transparent;")

        self.verticalLayout.addWidget(self.Discover_FirstName)

        self.Discover_LastName = QLabel(self.frame_7)
        self.Discover_LastName.setObjectName(u"Discover_LastName")
        self.Discover_LastName.setMinimumSize(QSize(189, 42))
        self.Discover_LastName.setStyleSheet(u"color: white; \n"
"font: 1000 60pt \"Nexa\";\n"
"background-color: rgb(97, 165, 85);\n"
"padding:0px;\n"
"\n"
"border-top: 0px solid rgb(125, 125, 125);\n"
"border-left :0px;\n"
"border-right:0px;\n"
"border-bottom:0px;\n"
"\n"
"background-color:transparent;")

        self.verticalLayout.addWidget(self.Discover_LastName)

        self.horizontalLayout_14.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout_14)

        self.Discover_Major = QLabel(self.frame_7)
        self.Discover_Major.setObjectName(u"Discover_Major")
        self.Discover_Major.setMinimumSize(QSize(189, 42))
        self.Discover_Major.setStyleSheet(u"color: rgb(145, 251, 141);\n"
"font: 1000 15pt \"Nexa\";\n"
"background-color: rgb(97, 165, 85);\n"
"border-radius: 5px;\n"
"border-top: 0px solid rgb(125, 125, 125);\n"
"border-left :0px;\n"
"border-right:0px;\n"
"border-bottom:2px solid rgb(145, 251, 141);\n"
"padding: 10px;\n"
"background-color:transparent;")

        self.verticalLayout_2.addWidget(self.Discover_Major)


        self.Discover_Email = QLabel(self.frame_7)
        self.Discover_Email.setObjectName(u"Discover_Email")
        self.Discover_Email.setMinimumSize(QSize(189, 42))
        self.Discover_Email.setStyleSheet(u"color: rgb(145, 251, 141); \n"
"font: 1000 15pt \"Nexa\";\n"
"background-color: rgb(97, 165, 85);\n"
"border-radius: 5px;\n"
"border-top: 0px solid rgb(125, 125, 125);\n"
"border-left :0px;\n"
"border-right:0px;\n"
"border-bottom:2px solid rgb(145, 251, 141);\n"
"padding: 10px;\n"
"background-color:transparent;")

        self.verticalLayout_2.addWidget(self.Discover_Email)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.gridLayout_5.addWidget(self.frame_7, 1, 0, 1, 1)

        self.Discover_Year = QLabel(self.frame_7)
        self.Discover_Year.setObjectName(u"Discover_Year")
        self.Discover_Year.setMinimumSize(QSize(189, 42))
        self.Discover_Year.setStyleSheet(u"color: rgb(145, 251, 141);; \n"
"font: 1000 15pt \"Nexa\";\n"
"background-color: rgb(97, 165, 85);\n"
"border-radius: 5px;\n"
"border-top: 0px solid rgb(125, 125, 125);\n"
"border-left :0px;\n"
"border-right:0px;\n"
"border-bottom:2px solid rgb(145, 251, 141);\n"
"padding: 10px;\n"
"background-color:transparent;")

        self.verticalLayout_2.addWidget(self.Discover_Year)

        self.BrowseHeader = QLabel(self.frame_4)
        self.BrowseHeader.setObjectName(u"BrowseHeader")
        self.BrowseHeader.setStyleSheet(u"color: white; \n"
"font: 800 50pt \"Nexa\";\n"
"background: transparent;\n"
"")
        self.BrowseHeader.setScaledContents(False)

        self.gridLayout_5.addWidget(self.BrowseHeader, 0, 0, 1, 1)

        self.gridLayout_4.addWidget(self.frame_4, 0, 1, 1, 1)

        self.frame_5 = QFrame(self.BrowsePage)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(50, 0))
        self.frame_5.setMaximumSize(QSize(1000, 200))
        self.frame_5.setStyleSheet(u"background-color: transparent;")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_5)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.FilterButton = QPushButton(self.frame_5, clicked=lambda: self.handleFilter())
        self.FilterButton.setObjectName(u"FilterButton")
        self.FilterButton.setMaximumSize(QSize(500, 16777215))
        self.FilterButton.setStyleSheet(u"QPushButton{font: 500 13pt \"Nexa Bold\";\n"
"background-color: rgb(98, 214, 81);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 5px; border: 2px rgb(33, 33, 34);\n"
"border-bottom: 3px solid rgb(72, 156, 59);\n"
"border-left:  1px solid rgb(72, 156, 59);\n"
"border-right:  1px solid rgb(72, 156, 59);\n"
"padding: 6px;}\n QPushButton:hover{background-color: rgb(99, 255, 179); \n border-bottom: 3px solid rgb(45, 160, 104);\n border-left: 2px solid rgb(45, 160, 104);\n border-right: 2px solid rgb(45, 160, 104);}"
"QPushButton:pressed{background-color: rgb(30, 94, 31);\n border-bottom: 3px solid rgb(22, 50, 22);\n border-left: 2px solid rgb(22, 50, 22);\n border-right: 2px solid rgb(22, 50, 22);}")

        self.gridLayout_6.addWidget(self.FilterButton, 5, 4, 1, 1)

        self.NextButton = QPushButton(self.frame_5, clicked=lambda: self.next_user(self.students, self.s_length))
        self.NextButton.setObjectName(u"NextButton")
        self.NextButton.setMinimumSize(QSize(150, 0))
        self.NextButton.setStyleSheet(u"QPushButton{font: 500 13pt \"Nexa Bold\";\n"
"background-color: rgb(180, 18, 223);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 5px; border: 2px rgb(129, 13, 159);\n"
"border-bottom: 3px solid rgb(129, 13, 159);\n"
"border-left:  1px solid rgb(129, 13, 159);\n"
"border-right:  1px solid rgb(129, 13, 159);\n"
"padding: 6px;}\n QPushButton:hover{background-color: rgb(206, 20, 255); \n border-bottom: 3px solid rgb(180, 18, 223);\n border-left: 2px solid rgb(180, 18, 223);\n border-right: 2px solid rgb(180, 18, 223);}"
"QPushButton:pressed{background-color: rgb(77, 8, 96);\n border-bottom: 3px solid rgb(52, 5, 64);\n border-left: 2px solid rgb(52, 5, 64);\n border-right: 2px solid rgb(52, 5, 64);}")

        self.gridLayout_6.addWidget(self.NextButton, 0, 4, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_4, 0, 5, 1, 1)

        self.LikeButton = QPushButton(self.frame_5, clicked=lambda: self.handleLike())
        self.LikeButton.setObjectName(u"LikeButton")
        self.LikeButton.setStyleSheet(u"QPushButton{font: 500 13pt \"Nexa Bold\";\n"
"background-color: rgb(18, 172, 207);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 5px; border: 2px rgb(18, 172, 207);\n"
"border-bottom: 4px solid rgb(13, 123, 147);\n"
"border-left:  2px solid rgb(13, 123, 147);\n"
"border-right:  2px solid rgb(13, 123, 147);\n"
"min-height: 40px;\n"
"padding: 6px;}\n QPushButton:hover{background-color: rgb(20, 235, 255); \n border-bottom: 4px solid rgb(15, 176, 191);\n border-left: 2px solid rgb(15, 176, 191);\n border-right: 2px solid rgb(15, 176, 191);}"
"QPushButton:pressed{background-color: rgb(8, 74, 88);\n border-bottom: 3px solid rgb(5, 49, 59);\n border-left: 2px solid rgb(5, 49, 59);\n border-right: 2px solid rgb(5, 49, 59);}")

        self.gridLayout_6.addWidget(self.LikeButton, 0, 2, 1, 2)

        self.FilterDropdown = QComboBox(self.frame_5)
        self.FilterDropdown.addItem("")
        self.FilterDropdown.addItem("")
        self.FilterDropdown.addItem("")
        self.FilterDropdown.addItem("")
        self.FilterDropdown.setObjectName(u"FilterDropdown")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.FilterDropdown.sizePolicy().hasHeightForWidth())
        self.FilterDropdown.setSizePolicy(sizePolicy1)
        self.FilterDropdown.setMinimumSize(QSize(150, 0))
        self.FilterDropdown.setStyleSheet(u"""
        QComboBox{
                border: 1px solid rgb(73, 73, 75); 
                border-radius: 4px; 
                padding: 1px 18px 1px 4px; 
                color: rgb(255, 255, 255);
                font: 15px \"Nexa\";
                background: rgb(33, 33, 34);
                }
        QComboBox::hover{
                background: rgb(73, 73, 75);
                }
        QComboBox QAbstractItemView {
                outline: 0px solid gray; 
                border: none; 
                color: rgb(255, 255, 255);
                font: 15px \"Nexa\";
                background-color: rgb(73, 73, 75); 
                selection-background-color: rgb(103, 103, 108); 
                }
        """)
        self.gridLayout_6.addWidget(self.FilterDropdown, 5, 2, 1, 2)

        self.PreviousButton = QPushButton(self.frame_5, clicked=lambda: self.prev_user(self.students, self.s_length))
        self.PreviousButton.setObjectName(u"PreviousButton")
        self.PreviousButton.setMinimumSize(QSize(150, 0))
        self.PreviousButton.setStyleSheet(u"QPushButton{font: 500 13pt \"Nexa Bold\";\n"
"background-color: rgb(180, 18, 223);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 5px; border: 2px rgb(129, 13, 159);\n"
"border-bottom: 3px solid rgb(129, 13, 159);\n"
"border-left:  1px solid rgb(129, 13, 159);\n"
"border-right:  1px solid rgb(129, 13, 159);\n"
"padding: 6px;}\n QPushButton:hover{background-color: rgb(206, 20, 255); \n border-bottom: 3px solid rgb(180, 18, 223);\n border-left: 2px solid rgb(180, 18, 223);\n border-right: 2px solid rgb(180, 18, 223);}"
"QPushButton:pressed{background-color: rgb(77, 8, 96);\n border-bottom: 3px solid rgb(52, 5, 64);\n border-left: 2px solid rgb(52, 5, 64);\n border-right: 2px solid rgb(52, 5, 64);}")

        self.gridLayout_6.addWidget(self.PreviousButton, 0, 1, 1, 1)

        self.FilterLine = QLineEdit(self.frame_5)
        self.FilterLine.setObjectName(u"FilterLine")
        self.FilterLine.setLayoutDirection(Qt.LeftToRight)
        self.FilterLine.setStyleSheet(u"font: 500 13pt \"Nexa Bold\";\n"
"background-color: rgb(191, 255, 246);\n"
"color: black;\n"
"border-radius: 5px; border: 2px rgb(61, 172, 202);\n"
"border-bottom: 3px solid rgb(159, 255, 246);\n"
"border-left:  1px solid rgb(72, 156, 59);\n"
"border-right:  1px solid rgb(72, 156, 59);\n"
"padding: 6px;")
        self.FilterLine.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.FilterLine, 5, 1, 1, 1)


        self.gridLayout_4.addWidget(self.frame_5, 1, 1, 1, 1)

        self.stackedWidget.addWidget(self.BrowsePage) #END BROWSE
        self.ProfilePage = QWidget()
        self.ProfilePage.setObjectName(u"ProfilePage")
        self.horizontalLayout = QHBoxLayout(self.ProfilePage)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.frame = QFrame(self.ProfilePage)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(700, 0))
        self.frame.setStyleSheet(u"background: transparent;\n"
"")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_9 = QGridLayout(self.frame)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.lCourseListWidget = QListWidget(self.frame)
        self.lCourseListWidget.setObjectName(u"lCourseListWidget")
        self.lCourseListWidget.setStyleSheet(u"color: white;")

        self.gridLayout_9.addWidget(self.lCourseListWidget, 21, 0, 1, 1)
        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")
        font1 = QFont()
        font1.setPointSize(30)
        font1.setBold(False)
        font1.setItalic(False)
        self.label_4.setFont(font1)
        self.label_4.setAutoFillBackground(False)
        self.label_4.setStyleSheet(u"color: white; \n"
"font: 30pt \"Segoe UI\";\n"
"background: transparent;\n"
"\n"
"")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.label_4, 0, 0, 1, 1)

        self.courseinstructLabel = QLabel(self.frame)
        self.courseinstructLabel.setObjectName(u"courseinstructLabel")
        self.courseinstructLabel.setStyleSheet(u"color: white;\n"
"font: 10pt;\n"
"")

        self.gridLayout_9.addWidget(self.courseinstructLabel, 20, 0, 1, 1)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(150, 0))
        self.label.setStyleSheet(u"color: white; \n"
"font: 15pt \"Segoe UI\";\n"
"background: transparent;\n"
"\n"
"")

        self.gridLayout_9.addWidget(self.label, 1, 0, 1, 1)

        self.UserName = QLabel(self.frame)
        self.UserName.setObjectName(u"UserName")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.UserName.sizePolicy().hasHeightForWidth())
        self.UserName.setSizePolicy(sizePolicy2)
        self.UserName.setMinimumSize(QSize(300, 0))
        self.UserName.setStyleSheet(u"color: white; \n"
"font: 15pt \"Segoe UI\";\n"
"background: transparent;\n"
"border-bottom: 2px solid white;\n"
"\n"
"")

        self.gridLayout_9.addWidget(self.UserName, 2, 0, 1, 1)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(150, 0))
        self.label_2.setStyleSheet(u"color: white; \n"
"font: 15pt \"Segoe UI\";\n"
"background: transparent;\n"
"\n"
"")

        self.gridLayout_9.addWidget(self.label_2, 3, 0, 1, 1)

        self.UserEmail = QLabel(self.frame)
        self.UserEmail.setObjectName(u"UserEmail")
        sizePolicy2.setHeightForWidth(self.UserEmail.sizePolicy().hasHeightForWidth())
        self.UserEmail.setSizePolicy(sizePolicy2)
        self.UserEmail.setMinimumSize(QSize(300, 0))
        self.UserEmail.setStyleSheet(u"color: white; \n"
"font: 15pt \"Segoe UI\";\n"
"background: transparent;\n"
"border-bottom: 2px solid white;\n"
"\n"
"")

        self.gridLayout_9.addWidget(self.UserEmail, 4, 0, 1, 1)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(150, 0))
        self.label_3.setStyleSheet(u"color: white; \n"
"font: 15pt \"Segoe UI\";\n"
"background: transparent;\n"
"\n"
"")

        self.gridLayout_9.addWidget(self.label_3, 5, 0, 1, 1)

        self.CourseVertLayout = QHBoxLayout()
        self.CourseVertLayout.setObjectName(u"CourseVertLayout")
        self.AddBtn = QPushButton(self.frame)
        self.AddBtn.setObjectName(u"AddBtn")
        self.AddBtn.setStyleSheet(u"QPushButton{font: 500 13pt \"Nexa Bold\";\n"
"background-color: rgb(18, 172, 207);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 5px; border: 2px rgb(18, 172, 207);\n"
"border-bottom: 4px solid rgb(13, 123, 147);\n"
"border-left:  2px solid rgb(13, 123, 147);\n"
"border-right:  2px solid rgb(13, 123, 147);\n"
"padding: 2px;}\n QPushButton:hover{background-color: rgb(20, 235, 255); \n border-bottom: 3px solid rgb(15, 176, 191);\n border-left: 2px solid rgb(15, 176, 191);\n border-right: 2px solid rgb(15, 176, 191);}"
"QPushButton:pressed{background-color: rgb(8, 74, 88);\n border-bottom: 3px solid rgb(5, 49, 59);\n border-left: 2px solid rgb(5, 49, 59);\n border-right: 2px solid rgb(5, 49, 59);}")

        self.CourseVertLayout.addWidget(self.AddBtn)

        self.DoneBtn = QPushButton(self.frame)
        self.DoneBtn.setObjectName(u"DoneBtn")
        self.DoneBtn.setStyleSheet(u"QPushButton{font: 500 13pt \"Nexa Bold\";\n"
"background-color: rgb(98, 214, 81);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 5px; border: 2px rgb(33, 33, 34);\n"
"border-bottom: 3px solid rgb(72, 156, 59);\n"
"border-left:  1px solid rgb(72, 156, 59);\n"
"border-right:  1px solid rgb(72, 156, 59);\n"
"padding: 2px;}\n QPushButton:hover{background-color: rgb(99, 255, 179); \n border-bottom: 3px solid rgb(45, 160, 104);\n border-left: 2px solid rgb(45, 160, 104);\n border-right: 2px solid rgb(45, 160, 104);}"
"QPushButton:pressed{background-color: rgb(30, 94, 31);\n border-bottom: 3px solid rgb(22, 50, 22);\n border-left: 2px solid rgb(22, 50, 22);\n border-right: 2px solid rgb(22, 50, 22);}")

        self.CourseVertLayout.addWidget(self.DoneBtn)

        self.DeleteBtn = QPushButton(self.frame)
        self.DeleteBtn.setObjectName(u"DeleteBtn")
        self.DeleteBtn.setStyleSheet(u"QPushButton{font: 500 13pt \"Nexa Bold\";\n"
"background-color: rgb(255, 61, 50);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 5px; \n"
"border: 2px rgb(255, 61, 50);\n"
"border-bottom: 3px solid rgb(158, 37, 31);\n"
"border-left:  1px solid rgb(214, 50, 42);\n"
"border-right:  1px solid rgb(214, 50, 42);\n"
"padding: 2px;}\n QPushButton:hover{background-color: rgb(253, 128, 121); \n border-bottom: 3px solid rgb(223, 77, 68);\n border-left: 2px solid rgb(223, 77, 68);\n border-right: 2px solid rgb(223, 77, 68);}"
"QPushButton:pressed{background-color: rgb(128, 44, 39);\n border-bottom: 3px solid rgb(80, 19, 16);\n border-left: 2px solid rgb(80, 19, 16);\n border-right: 2px solid rgb(80, 19, 16);}")
        self.CourseVertLayout.addWidget(self.DeleteBtn)

        self.gridLayout_9.addLayout(self.CourseVertLayout, 25, 0, 1, 1)

        self.UserMajor = QLabel(self.frame)
        self.UserMajor.setObjectName(u"UserMajor")
        sizePolicy2.setHeightForWidth(self.UserMajor.sizePolicy().hasHeightForWidth())
        self.UserMajor.setSizePolicy(sizePolicy2)
        self.UserMajor.setMinimumSize(QSize(300, 0))
        self.UserMajor.setStyleSheet(u"color: white; \n"
"font: 15pt \"Segoe UI\";\n"
"background: transparent;\n"
"border-bottom: 2px solid white;\n"
"\n"
"")

        self.gridLayout_9.addWidget(self.UserMajor, 6, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_9.addItem(self.verticalSpacer_2)

        self.MatchTitle = QLabel(self.frame)
        self.MatchTitle.setObjectName(u"MatchTitle")
        self.MatchTitle.setStyleSheet(u"color: white; \n"
"font: 30pt \"Segoe UI\";\n"
"background: transparent;\n"
"")

        self.gridLayout_9.addWidget(self.MatchTitle, 8, 0, 1, 1)

        self.CourseInputEdit = QLineEdit(self.frame)
        self.CourseInputEdit.setObjectName(u"CourseInputEdit")
        self.CourseInputEdit.setStyleSheet(u"background-color: white;\n"
"border-radius: 10px;\n"
"padding: 0 8px;\n"
"color: black;")

        self.gridLayout_9.addWidget(self.CourseInputEdit, 24, 0, 1, 1)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_9.addItem(self.verticalSpacer_6, 9, 0, 1, 1)

        self.MatchName = QLabel(self.frame)
        self.MatchName.setObjectName(u"MatchName")
        self.MatchName.setStyleSheet(u"color: white; \n"
"font: 15pt \"Segoe UI\";\n"
"background: transparent;\n"
"border-bottom: 2px solid white;")

        self.gridLayout_9.addWidget(self.MatchName, 10, 0, 1, 1)

        self.AddCoursesBtn = QPushButton(self.frame)
        self.AddCoursesBtn.setObjectName(u"AddCoursesBtn")
        self.AddCoursesBtn.setStyleSheet(u"QPushButton{font: 500 13pt \"Nexa Bold\";\n"
"background-color: rgb(98, 214, 81);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 5px; border: 2px rgb(33, 33, 34);\n"
"border-bottom: 3px solid rgb(72, 156, 59);\n"
"border-left:  1px solid rgb(72, 156, 59);\n"
"border-right:  1px solid rgb(72, 156, 59);\n"
"padding: 6px;}\n QPushButton:hover{background-color: rgb(99, 255, 179); \n border-bottom: 3px solid rgb(45, 160, 104);\n border-left: 2px solid rgb(45, 160, 104);\n border-right: 2px solid rgb(45, 160, 104);}"
"QPushButton:pressed{background-color: rgb(30, 94, 31);\n border-bottom: 3px solid rgb(22, 50, 22);\n border-left: 2px solid rgb(22, 50, 22);\n border-right: 2px solid rgb(22, 50, 22);}")

        self.gridLayout_9.addWidget(self.AddCoursesBtn, 23, 0, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_9.addItem(self.verticalSpacer_5)

        self.MatchEmail = QLabel(self.frame)
        self.MatchEmail.setObjectName(u"MatchEmail")
        self.MatchEmail.setStyleSheet(u"color: white; \n"
"font: 15pt \"Segoe UI\";\n"
"background: transparent;\n"
"border-bottom: 2px solid white;")

        self.gridLayout_9.addWidget(self.MatchEmail, 12, 0, 1, 1)

        self.MatchLayout = QHBoxLayout()
        self.MatchLayout.setObjectName(u"MatchLayout")
        self.prevMatchButton = QPushButton(self.frame, clicked=lambda: self.prevMatch())
        self.prevMatchButton.setObjectName(u"prevMatchButton")
        self.prevMatchButton.setStyleSheet(u"QPushButton{font: 500 13pt \"Nexa Bold\";\n"
"background-color: rgb(180, 18, 223);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 5px; border: 2px rgb(129, 13, 159);\n"
"border-bottom: 3px solid rgb(129, 13, 159);\n"
"border-left:  1px solid rgb(129, 13, 159);\n"
"border-right:  1px solid rgb(129, 13, 159);\n"
"padding: 6px;}\n QPushButton:hover{background-color: rgb(206, 20, 255); \n border-bottom: 3px solid rgb(180, 18, 223);\n border-left: 2px solid rgb(180, 18, 223);\n border-right: 2px solid rgb(180, 18, 223);}"
"QPushButton:pressed{background-color: rgb(77, 8, 96);\n border-bottom: 3px solid rgb(52, 5, 64);\n border-left: 2px solid rgb(52, 5, 64);\n border-right: 2px solid rgb(52, 5, 64);}")

        self.MatchLayout.addWidget(self.prevMatchButton)

        self.nextMatchButton = QPushButton(self.frame, clicked=lambda: self.nextMatch())
        self.nextMatchButton.setObjectName(u"nextMatchButton")
        self.nextMatchButton.setLayoutDirection(Qt.LeftToRight)
        self.nextMatchButton.setStyleSheet(u"QPushButton{font: 500 13pt \"Nexa Bold\";\n"
"background-color: rgb(180, 18, 223);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 5px; border: 2px rgb(129, 13, 159);\n"
"border-bottom: 3px solid rgb(129, 13, 159);\n"
"border-left:  1px solid rgb(129, 13, 159);\n"
"border-right:  1px solid rgb(129, 13, 159);\n"
"padding: 6px;}\n QPushButton:hover{background-color: rgb(206, 20, 255); \n border-bottom: 3px solid rgb(180, 18, 223);\n border-left: 2px solid rgb(180, 18, 223);\n border-right: 2px solid rgb(180, 18, 223);}"
"QPushButton:pressed{background-color: rgb(77, 8, 96);\n border-bottom: 3px solid rgb(52, 5, 64);\n border-left: 2px solid rgb(52, 5, 64);\n border-right: 2px solid rgb(52, 5, 64);}")

        self.MatchLayout.addWidget(self.nextMatchButton)

        self.MatchSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.MatchLayout.addItem(self.MatchSpacer)


        self.gridLayout_9.addLayout(self.MatchLayout, 13, 0, 1, 1)

        self.CoursesTitle = QLabel(self.frame)
        self.CoursesTitle.setObjectName(u"CoursesTitle")
        self.CoursesTitle.setStyleSheet(u"color: white; \n"
"font: 30pt \"Segoe UI\";\n"
"background: transparent;")

        self.gridLayout_9.addWidget(self.CoursesTitle, 19, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_9.addItem(self.verticalSpacer_4)

        self.LikesTitle = QLabel(self.frame)
        self.LikesTitle.setObjectName(u"LikesTitle")
        self.LikesTitle.setStyleSheet(u"color: white; \n"
"font: 30pt \"Segoe UI\";\n"
"background: transparent;\n"
"")

        self.gridLayout_9.addWidget(self.LikesTitle, 15, 0, 1, 1)

        self.LikesLabel = QLabel(self.frame)
        self.LikesLabel.setObjectName(u"LikesLabel")
        self.LikesLabel.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"")
        
        self.gridLayout_9.addWidget(self.LikesLabel, 16, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_9.addItem(self.verticalSpacer_3)

        self.horizontalLayout.addWidget(self.frame)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.stackedWidget.addWidget(self.ProfilePage)

        self.gridLayout_2.addWidget(self.stackedWidget, 0, 1, 1, 1)

        Stinder.setCentralWidget(self.centralwidget)

        self.retranslateUi(Stinder)

        self.CoursesTitle.raise_()
        self.LikesLabel.raise_()
        self.UserEmail.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.UserName.raise_()
        self.UserMajor.raise_()
        self.label.raise_()
        self.label_4.raise_()
        self.courseinstructLabel.raise_()
        self.lCourseListWidget.raise_()
        self.CourseInputEdit.raise_()
        self.AddCoursesBtn.raise_()

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Stinder)
    # setupUi

    def retranslateUi(self, Stinder):
        a_user = self.students[0]
        Stinder.setWindowTitle(QCoreApplication.translate("Stinder", u"Stinder", None))
        self.actionTemp_Button.setText(QCoreApplication.translate("Stinder", u"Temp Button", None))
        self.actionTemp_Button_2.setText(QCoreApplication.translate("Stinder", u"Temp Button", None))
        self.actionTemp_Button_3.setText(QCoreApplication.translate("Stinder", u"Temp Button", None))
        self.ProfileButton.setText(QCoreApplication.translate("Stinder", u"Profile", None))
        self.BrowseButton.setText(QCoreApplication.translate("Stinder", u"Browse", None))
        self.logo.setText("")
        self.AboutButton.setText(QCoreApplication.translate("Stinder", u"About", None))
        self.LogoutBtn.setText(QCoreApplication.translate("Stinder", u"Logout", None))
        self.aboutlogo.setText("")
        self.abouttextp2.setText(QCoreApplication.translate("Stinder", u"<html><head/><body><p align=\"justify\"><span style=\" font-size:8pt; font-weight:600; font-style:italic; color:#ffffff;\">Stinder aims to solve those problems for those who would like to pair</span></p><p align=\"justify\"><span style=\" font-size:8pt; font-weight:600; font-style:italic; color:#ffffff;\">up with those with similar work ethic and motivations. </span></p><p align=\"justify\"><span style=\" font-size:8pt; font-weight:600; font-style:italic; color:#ffffff;\">Fill out your student information for your profile and browse through</span></p><p align=\"justify\"><span style=\" font-size:8pt; font-weight:600; font-style:italic; color:#ffffff;\">your class population for those with similar qualities to </span></p><p align=\"justify\"><span style=\" font-size:8pt; font-weight:600; font-style:italic; color:#ffffff;\">work as effectively as possible in a group setting! Filter students by</span></p><p align=\"justify\"><span style=\" font-size:8pt; font-weight:600; font-style:italic; color:#ffffff;\">major,"
                        " coursework, schedule and more to find your perfect</span></p><p align=\"justify\"><span style=\" font-size:8pt; font-weight:600; font-style:italic; color:#ffffff;\">match!</span></p></body></html>", None))
        self.FAQsText.setText(QCoreApplication.translate("Stinder", u"<html><head/><body><p align=\"center\"><span style=\" font-size:36pt; text-decoration: underline; color:#ffffff;\">FAQs</span></p></body></html>", None))
        self.TSText.setText(QCoreApplication.translate("Stinder", u"<html><head/><body><p><span style=\" font-size:24pt; text-decoration: underline; color:#ffffff;\">Meet Team Swipers</span></p></body></html>", None))
        self.abouttextp3.setText(QCoreApplication.translate("Stinder", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#ffffff;\">Stinder. Never have a bad (study) date again.</span></p><p align=\"center\"><br/></p></body></html>", None))
        self.Q6Text.setText(QCoreApplication.translate("Stinder", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:600; color:#ffffff;\">Q: </span><a name=\"docs-internal-guid-9a1ec44c-7fff-704f-472d-044e3c22d185\"/><span style=\" font-family:'Arial'; font-size:12pt; font-weight:600; color:#ffffff; background-color:transparent;\">C</span><span style=\" font-family:'Arial'; font-size:12pt; font-weight:600; color:#ffffff; background-color:transparent;\">an I match more than once? </span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">A: Of course! Our matching algorithm </span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">works so that it would continue to match </span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">your profile with other profiles similar to </span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:40"
                        "0; color:#ffffff; background-color:transparent;\">yours as long as you are using Stinder and </span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">liking profiles.</span></p></body></html>", None))
        self.Q2Text.setText(QCoreApplication.translate("Stinder", u"<html><head/><body><p><a name=\"docs-internal-guid-d6b8bf47-7fff-02bc-f938-e7ece8d2821a\"/><span style=\" font-family:'Arial'; font-size:12pt; font-weight:696; color:#ffffff; background-color:transparent;\">Q</span><span style=\" font-family:'Arial'; font-size:12pt; font-weight:696; color:#ffffff; background-color:transparent;\">: How do I edit my profile?</span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">A: </span><a name=\"docs-internal-guid-367ca894-7fff-569c-cbbf-45c85db7a4be\"/><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">Y</span><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">ou can edit your profile by clicking on the</span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">profile button on the left hand side of the</"
                        "span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">application and then clicking the edit profile</span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">button. </span></p></body></html>", None))
        self.EG_ProfilePic.setText("")
        self.EG_NameRoleAnswer.setText(QCoreApplication.translate("Stinder", u"<html><head/><body><p><span style=\" font-size:11pt; font-weight:700; text-decoration: underline; color:#ffffff;\">Eddie Gibbons | Project Lead</span></p><p><span style=\" font-size:11pt; color:#ffffff;\">&quot;A favorite study habit of mine is to</span></p><p><span style=\" font-size:11pt; color:#ffffff;\">collaborate on class notes with </span></p><p><span style=\" font-size:11pt; color:#ffffff;\">friends. There's always different </span></p><p><span style=\" font-size:11pt; color:#ffffff;\">interpretations and understandings</span></p><p><span style=\" font-size:11pt; color:#ffffff;\">of course material and it's great to</span></p><p><span style=\" font-size:11pt; color:#ffffff;\">learn by having everyone give their</span></p><p><span style=\" font-size:11pt; color:#ffffff;\">opinion and reasoning as to why they </span></p><p><span style=\" font-size:11pt; color:#ffffff;\">believe what they believe.&quot;</span></p></body></html>", None))
        self.WT_NameRoleAnswer.setText(QCoreApplication.translate("Stinder", u"<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; text-decoration: underline; color:#ffffff;\">Wyatt Townsend | Backend</span></p><p><span style=\" font-size:11pt; font-weight:400; color:#ffffff;\">&quot;Flash cards have always been an </span></p><p><span style=\" font-size:11pt; font-weight:400; color:#ffffff;\">effective study method for me. </span></p><p><span style=\" font-size:11pt; font-weight:400; color:#ffffff;\">They become much more effective </span></p><p><span style=\" font-size:11pt; font-weight:400; color:#ffffff;\">when I get to share flash cards </span></p><p><span style=\" font-size:11pt; font-weight:400; color:#ffffff;\">with others and use cards they </span></p><p><span style=\" font-size:11pt; font-weight:400; color:#ffffff;\">made to make sure I cover all </span></p><p><span style=\" font-size:11pt; font-weight:400; color:#ffffff;\">important material.&quot;</span></p></body></html>", None))
        self.WT_ProfilePic.setText("")
        self.Q5Text.setText(QCoreApplication.translate("Stinder", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:600; color:#ffffff;\">Q: </span><a name=\"docs-internal-guid-ac5f434d-7fff-f5d7-39ec-9f137ccebbd9\"/><span style=\" font-family:'Arial'; font-size:12pt; font-weight:600; color:#ffffff; background-color:transparent;\">H</span><span style=\" font-family:'Arial'; font-size:12pt; font-weight:600; color:#ffffff; background-color:transparent;\">ow does the like feature work </span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:600; color:#ffffff; background-color:transparent;\">on Stinder?</span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">A: </span><a name=\"docs-internal-guid-5279443d-7fff-235c-73b0-504c6371e233\"/><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">W</span><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\""
                        ">hen on the browse page you can use </span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">the slider to like a certain profile. If that </span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">student likes you back, then you two have</span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">a match! </span></p></body></html>", None))
        self.Q3Text.setText(QCoreApplication.translate("Stinder", u"<html><head/><body><p><a name=\"docs-internal-guid-d6b8bf47-7fff-02bc-f938-e7ece8d2821a\"/><span style=\" font-family:'Arial'; font-size:12pt; font-weight:696; color:#ffffff; background-color:transparent;\">Q</span><span style=\" font-size:12pt; font-weight:600; color:#ffffff;\">: </span><a name=\"docs-internal-guid-088e0566-7fff-4bbb-1e26-74fa49546a58\"/><span style=\" font-family:'Arial'; font-size:12pt; font-weight:600; color:#ffffff; background-color:transparent;\">H</span><span style=\" font-family:'Arial'; font-size:12pt; font-weight:600; color:#ffffff; background-color:transparent;\">ow do I message a person that I </span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:600; color:#ffffff; background-color:transparent;\">matched with?</span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">A: Once you get a match, the email of your </span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:4"
                        "00; color:#ffffff; background-color:transparent;\">match will then be displayed on your screen </span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">to contact them! </span></p></body></html>", None))
        self.CE_ProfilePic.setText("")
        self.CE_NameRoleAnswer.setText(QCoreApplication.translate("Stinder", u"<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; text-decoration: underline; color:#ffffff;\">Carlos Echenique | Frontend</span></p><p><span style=\" font-size:11pt; font-weight:400; color:#ffffff;\">&quot;My favorite study spot is usually</span></p><p><span style=\" font-size:11pt; font-weight:400; color:#ffffff;\">my place of residence or at least</span></p><p><span style=\" font-size:11pt; font-weight:400; color:#ffffff;\">close to home. I think it's the best</span></p><p><span style=\" font-size:11pt; font-weight:400; color:#ffffff;\">feeling ever to finish a long night</span></p><p><span style=\" font-size:11pt; font-weight:400; color:#ffffff;\">of studying and then jumping right</span></p><p><span style=\" font-size:11pt; font-weight:400; color:#ffffff;\">into bed!&quot; </span></p></body></html>", None))
        self.MissionStatement.setText(QCoreApplication.translate("Stinder", u"<html><head/><body><p align=\"center\"><span style=\" font-size:24pt; text-decoration: underline; color:#ffffff;\">Mission Statement</span><span style=\" font-size:24pt;\"><br/></span></p></body></html>", None))
        self.abouttextp1.setText(QCoreApplication.translate("Stinder", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600; color:#ffffff;\">Do you hate having to group up with students you don't know? </span></p><p align=\"center\"><span style=\" font-size:12pt; font-weight:600; color:#ffffff;\">Have you ever been stuck doing all the work?</span></p><p align=\"center\"><span style=\" font-size:12pt; font-weight:600; color:#ffffff;\">Us too.</span></p></body></html>", None))
        self.Q4Text.setText(QCoreApplication.translate("Stinder", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:600; color:#ffffff;\">Q: </span><a name=\"docs-internal-guid-2efe5ddc-7fff-8493-3a5a-d7bea65d3e43\"/><span style=\" font-family:'Arial'; font-size:12pt; font-weight:600; color:#ffffff; background-color:transparent;\">C</span><span style=\" font-family:'Arial'; font-size:12pt; font-weight:600; color:#ffffff; background-color:transparent;\">an I search for students </span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:600; color:#ffffff; background-color:transparent;\">with specific qualities? </span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">A: </span><a name=\"docs-internal-guid-a09ac3f7-7fff-19a0-9d0c-45e205b4e893\"/><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">C</span><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:trans"
                        "parent;\">urrently on the browse page you can </span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">filter the profiles by major, by year, or by </span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">course. Once you enter a search and click </span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">the filter button, all Stinder profiles are </span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">refreshed, giving you the profiles that </span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">match your filter search.</span></p></body></html>", None))
        self.Q1Text.setText(QCoreApplication.translate("Stinder", u"<html><head/><body><p><a name=\"docs-internal-guid-7b5fe8b8-7fff-9183-8138-f3d8823b0081\"/><span style=\" font-family:'Arial'; font-size:12pt; font-weight:600; color:#ffffff; background-color:transparent;\">Q</span><span style=\" font-family:'Arial'; font-size:12pt; font-weight:600; color:#ffffff; background-color:transparent;\">: How does Stinder work?</span></p><p><a name=\"docs-internal-guid-ccca6ff3-7fff-c106-1d28-2e3f845958f1\"/><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">A</span><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">: Stinder works by using the information </span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">you filled out in the sign up process in an </span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">al"
                        "gorithm that matches you with other </span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">students with similar study habits,</span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\"> behaviors, locations, major and</span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">coursework. After the algorithm has </span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">been run on your information, you can </span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">go to the browse page to view the students </span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">who we at Stinder believe"
                        " are your best </span></p><p><span style=\" font-family:'Arial'; font-size:12pt; font-weight:400; color:#ffffff; background-color:transparent;\">match as a study buddy. </span></p></body></html>", None))
        self.AD_ProfilePic.setText("")
        self.AD_NameRoleAnswer.setText(QCoreApplication.translate("Stinder", u"<html><head/><body><p><a name=\"docs-internal-guid-f7cd91fc-7fff-5fe1-50e4-815a388fcb13\"/><span style=\" font-family:'Arial'; font-size:11pt; font-weight:600; text-decoration: underline; color:#ffffff; background-color:transparent;\">A</span><span style=\" font-family:'Arial'; font-size:11pt; font-weight:600; text-decoration: underline; color:#ffffff; background-color:transparent;\">llison Denham | Backend/Frontend</span></p><p><span style=\" font-family:'Arial'; font-size:11pt; font-weight:400; color:#ffffff; background-color:transparent;\">My favorite place to study is definitely in </span></p><p><span style=\" font-family:'Arial'; font-size:11pt; font-weight:400; color:#ffffff; background-color:transparent;\">the libraries. During the pandemic I </span></p><p><span style=\" font-family:'Arial'; font-size:11pt; font-weight:400; color:#ffffff; background-color:transparent;\">realized how important my </span></p><p><span style=\" font-family:'Arial'; font-size:11pt; font-weight:400; color:#ffffff; background-"
                        "color:transparent;\">environment is to my study habits </span></p><p><span style=\" font-family:'Arial'; font-size:11pt; font-weight:400; color:#ffffff; background-color:transparent;\">and productivity when getting work </span></p><p><span style=\" font-family:'Arial'; font-size:11pt; font-weight:400; color:#ffffff; background-color:transparent;\">done. The libraries at UF are also </span></p><p><span style=\" font-family:'Arial'; font-size:11pt; font-weight:400; color:#ffffff; background-color:transparent;\">a great place to meet up and study </span></p><p><span style=\" font-family:'Arial'; font-size:11pt; font-weight:400; color:#ffffff; background-color:transparent;\">with a group or friend.</span><span style=\" color:#ffffff;\"><br/></span></p></body></html>", None))
        self.Discover_FirstName.setText("")
        self.Discover_LastName.setText("")
        self.Discover_Major.setText("")
        self.Discover_Email.setText("")
        self.Discover_Year.setText("")
        self.BrowseHeader.setText(QCoreApplication.translate("Stinder", u"<html><head/><body><p align=\"center\">Browse</p></body></html>", None))
        self.FilterButton.setText(QCoreApplication.translate("Stinder", u"Filter", None))
        self.NextButton.setText(QCoreApplication.translate("Stinder", u"Next", None))
#if QT_CONFIG(whatsthis)
        self.FilterLine.setWhatsThis(QCoreApplication.translate("Stinder", u"<html><head/><body><p align=\"center\"><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.FilterLine.setText("")
        self.FilterLine.setPlaceholderText(QCoreApplication.translate("Stinder", u"Search", None))
        self.PreviousButton.setText(QCoreApplication.translate("Stinder", u"Previous", None))
        self.LikeButton.setText(QCoreApplication.translate("Stinder", u"Like", None))
        self.FilterDropdown.setItemText(0, QCoreApplication.translate("Stinder", u"Filter By", None))
        self.FilterDropdown.setItemText(1, QCoreApplication.translate("Stinder", u"Major", None))
        self.FilterDropdown.setItemText(2, QCoreApplication.translate("Stinder", u"Year", None))
        self.FilterDropdown.setItemText(3, QCoreApplication.translate("Stinder", u"Course", None))

        self.FilterDropdown.setPlaceholderText(QCoreApplication.translate("Stinder", u"Filter By", None))
        self.MatchName.setText("")
        self.AddCoursesBtn.setText(QCoreApplication.translate("Stinder", u"Add Courses", None))
        self.LikesLabel.setText("")
        self.prevMatchButton.setText(QCoreApplication.translate("Stinder", u"Previous", None))
        self.nextMatchButton.setText(QCoreApplication.translate("Stinder", u"Next", None))
        self.UserName.setText("")
        self.CoursesTitle.setText(QCoreApplication.translate("Stinder", u"Courses", None))
        self.MatchEmail.setText("")
        self.label_2.setText(QCoreApplication.translate("Stinder", u"Email:", None))
        self.label_3.setText(QCoreApplication.translate("Stinder", u"Major:", None))
        self.AddBtn.setText(QCoreApplication.translate("Stinder", u"Add", None))
        self.DoneBtn.setText(QCoreApplication.translate("Stinder", u"Done", None))
        self.DeleteBtn.setText(QCoreApplication.translate("Stinder", u"Delete", None))
        self.MatchTitle.setText(QCoreApplication.translate("Stinder", u"Matches", None))
        self.CourseInputEdit.setPlaceholderText(QCoreApplication.translate("Stinder", u"--Enter Course Code--", None))
        self.label.setText(QCoreApplication.translate("Stinder", u"Name:", None))
        self.UserMajor.setText("")
        self.UserEmail.setText("")
        self.LikesTitle.setText(QCoreApplication.translate("Stinder", u"Likes", None))
        self.label_4.setText(QCoreApplication.translate("Stinder", u"Profile", None))
        self.courseinstructLabel.setText(QCoreApplication.translate("Stinder", u"Add courses to connect with people in your classes.", None))
    # retranslateUi

    def next_user(self, users, length):
        counter = self.counter
        counter = counter + 1
        if counter == length:
            counter = counter - 1
        self.counter = counter
        self.Discover_FirstName.setText(users[counter][0])
        self.Discover_LastName.setText(users[counter][1])
        self.Discover_Major.setText(users[counter][2])
        courses = ""
        i = 0
        if len(users[counter][10]) == 0:
            courses = "No courses."
        else:
            for c in users[counter][10]:
                if i == (len(users[counter][10]) - 1):
                    courses = courses + str(c)
                else:
                    courses = courses + str(c) + ", "
                i = i + 1
        self.Discover_Email.setText(courses)
        self.Discover_Year.setText(users[counter][4])

    def prev_user(self, users, length):
        counter = self.counter
        if counter == 0:
            counter = counter + 1
        counter = counter - 1
        self.counter = counter
        self.Discover_FirstName.setText(users[counter][0])
        self.Discover_LastName.setText(users[counter][1])
        self.Discover_Major.setText(users[counter][2])
        courses = ""
        i = 0
        if len(users[counter][10]) == 0:
            courses = "No courses."
        else:
            for c in users[counter][10]:
                if i == (len(users[counter][10]) - 1):
                    courses = courses + str(c)
                else:
                    courses = courses + str(c) + ", "
                i = i + 1
        self.Discover_Email.setText(courses)
        self.Discover_Year.setText(users[counter][4])

    def list(self):
        connection = sqlite3.connect(resource_filename(__name__, "users.db"))
        cursor = connection.cursor()
        with connection:
            cursor.execute("SELECT * FROM contacts")
            users = []
            length = 0
            for row in cursor:
                user_fN = row[0]
                user_lN = row[1]
                user_maj = row[2]
                user_e = row[3]
                user_y = row[4]
                user_met = row[5]
                user_loc = row[6]
                user_job = row[7]
                user_day = row[8]
                user_sH = row[9]
                
                user = [user_fN, user_lN, user_maj, user_e, user_y, user_met, user_loc, user_job, user_day, user_sH]
                users.append(user)
                length = length + 1
            
            cursor.execute("SELECT user_email, code FROM courses") # getting courses separately
            courses = []
            for row in cursor:
                email = row[0]
                code = row[1]
                course = [email, code]
                courses.append(course)

            for student in users: # joining every student's courses
                codes = []
                for course in courses:
                    if course[0] == student[3]:
                        codes.append(course[1])
                student.append(codes)

            return users, length

    def handleFilter(self):
        cat = self.FilterDropdown.currentText()
        line = self.FilterLine.text()

        fltr_users = []
        fltr_length = 0

        if cat == "Major":
            for student in self.students:
                if student[2] == line:
                    fltr_users.append(student)
                    fltr_length = fltr_length + 1
        elif cat == "Year":
            for student in self.students:
                if student[4] == line:
                    fltr_users.append(student)
                    fltr_length = fltr_length + 1
        elif cat == "Course":
            for student in self.students:
                for code in student[10]:
                    if code == line:
                        fltr_users.append(student)
                        fltr_length = fltr_length + 1

        if fltr_length == 0:
            errorBox = QtWidgets.QMessageBox()
            errorBox.setText("No results found matching your search!")
            errorBox.exec()
            self.students, self.s_length = self.list()
        else:
            self.students = fltr_users
            self.s_length = fltr_length
        
        self.handleAlgo()
    
    def likes_counter(self):
        u_email = self.UserEmail.text()
        
        likes_conn = sqlite3.connect(resource_filename(__name__, "users.db"))
        likes_cur = likes_conn.cursor()

        likes_cur.execute("SELECT like_fname, like_lname, like_email FROM likes where user_email = ?", (u_email,))
        likes_conn.commit()
        users_liked = []
        like_counter = 0

        for row in likes_cur:
            like_fN = row[0]
            like_lN = row[1]
            like_e = row[2]
            like = [like_fN, like_lN, like_e]
            users_liked.append(like)
            like_counter = like_counter + 1

        likes_conn.close()
        result = ""
        if like_counter == 1:
            result = "You have received " + str(like_counter) + " like!"
        else:
            result = "You have received " + str(like_counter) + " likes!"
        self.LikesLabel.setText(result)

        self.matches, self.m_length = self.matchList()
        if self.m_length != 0:
            self.MatchName.setText(self.matches[self.m_counter][0])
            self.MatchEmail.setText(self.matches[self.m_counter][1])
        else:
            self.nextMatchButton.setVisible(False)
            self.prevMatchButton.setVisible(False)

    def handleAlgo(self):
        ranking = []
        rank = 0

        for student in self.students:
            rank = 0
            if student[3] == self.c_user[3]: # major
                rank = rank + 18
            if student[4] == self.c_user[4]: # year
                rank = rank + 18
            if student[5] == self.c_user[5]: # method
                rank = rank + 17
            if student[6] == self.c_user[6]: # loc
                rank = rank + 15
            if student[7] == self.c_user[7]: # job
                rank = rank + 12
            if student[8] == self.c_user[8]: # day
                rank = rank + 10
            if student[9] == self.c_user[9]: # study history
                rank = rank + 10
            ranking.append(rank)
        
        numpy_students = numpy.array(self.students, dtype=object)
        numpy_ranking = numpy.array(ranking, dtype=object)
        numpy_sort = numpy_ranking.argsort()[::-1][:self.s_length + 1]
        sortedStudents = numpy_students[numpy_sort]

        self.students = sortedStudents
        self.counter = 0
        self.removeSelf()
        self.prev_user(self.students, self.s_length)
        
    def handleLike(self):
        u_email = self.UserEmail.text()
        l_Fn = self.students[self.counter][0]
        l_Ln = self.students[self.counter][1]
        l_email = self.students[self.counter][3]
        
        likes_conn = sqlite3.connect(resource_filename(__name__, "users.db"))
        likes_cur = likes_conn.cursor()

        # Like already exists
        likes_cur.execute("SELECT COUNT(*) from likes where user_email == ? AND like_email == ?", (u_email, l_email))
        likes_conn.commit()
        isLiked = likes_cur.fetchone()[0]

        # Like yourself, deprecrated
        if u_email == l_email:
            # add error message to GUI also
            likes_conn.close()
            errorBox = QtWidgets.QMessageBox()
            errorBox.setText("You attempted to like yourself!")
            errorBox.exec()
            return
        elif isLiked == 1:
            likes_conn.close()
            errorBox = QtWidgets.QMessageBox()
            errorBox.setText("You already liked this person!")
            errorBox.exec()
            return
        else:
            likes_cur.execute("INSERT OR REPLACE INTO likes (user_email, like_fname, like_lname, like_email) VALUES (?, ?, ?, ?)", (u_email, l_Fn, l_Ln, l_email))
            likes_conn.commit()

            likes_cur.execute("SELECT * from likes WHERE user_email == ?", (l_email, ))
            likes_conn.commit()

            for row in likes_cur:
                if str(row[4]) == u_email:
                    likes_cur.execute("INSERT OR REPLACE INTO matches (user_email, match_fname, match_lname, match_email) VALUES (?, ?, ?, ?)", (u_email, l_Fn, l_Ln, l_email))
                    likes_conn.commit()
                    self.showMatch()
                    break

            likes_conn.close()

    def takeRank(self, i):
        return self.students[i][10]

    def showMatch(self):
        matchUser = "Here's " + self.students[self.counter][0] + "'s email to contact him: " + self.students[self.counter][3]
        self.matchUi.InfoLabel.setText(matchUser)
        self.matchWindow.show()

    def matchList(self):
        u_email = self.UserEmail.text()
        
        match_conn = sqlite3.connect(resource_filename(__name__, "users.db"))
        match_cur = match_conn.cursor()

        match_cur.execute("SELECT * from matches WHERE user_email == ?", (u_email, ))
        match_conn.commit()

        m_list = []
        m_length = 0
        for row in match_cur:
            m_name = str(row[2]) + " " + str(row[3])
            m_email = str(row[4])
            m = [m_name, m_email]
            m_list.append(m)
            m_length = m_length + 1

        return m_list, m_length

    def prevMatch(self):
        if self.m_length != 0:
            counter = self.m_counter

            if counter != 0:
                counter = counter - 1
                self.m_counter = counter

            self.MatchName.setText(self.matches[self.m_counter][0])
            self.MatchEmail.setText(self.matches[self.m_counter][1])

    def nextMatch(self):
        if self.m_length != 0:
        
            counter = self.m_counter

            if counter != self.m_length | self.m_length != 1:
                counter = counter + 1
                self.m_counter = counter

            if self.m_counter == self.m_length:
                counter = counter - 1
                self.m_counter = counter

            self.MatchName.setText(self.matches[self.m_counter][0])
            self.MatchEmail.setText(self.matches[self.m_counter][1])

    def removeSelf(self):
        i = 0
        for student in self.students:
            if student[3] == self.UserEmail.text():
                self.students = numpy.delete(numpy.array(self.students,dtype =object), i, 0)
                self.s_length = self.s_length - 1
                break
            i = i + 1