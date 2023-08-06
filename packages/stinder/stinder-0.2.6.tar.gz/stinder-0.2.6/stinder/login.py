# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Login.ui'
##
## Created by: Qt User Interface Compiler version 6.1.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

from stinder.stinder_images_rc import *

class Ui_Stinder_Login(object):
    def setupUi(self, Stinder_Login):
        if not Stinder_Login.objectName():
            Stinder_Login.setObjectName(u"Stinder_Login")
        Stinder_Login.resize(646, 476)
        QFontDatabase.addApplicationFont(":/fonts/fonts/NexaBold.otf")
        Stinder_Login.setStyleSheet(u"background-color:qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(56, 0, 83, 255), stop:1 rgba(75, 0, 149, 255))")
        self.loginPages = QStackedWidget(Stinder_Login)
        self.loginPages.setObjectName(u"loginPages")
        self.loginPages.setGeometry(QRect(0, 0, 651, 473))
        self.loginPages.setStyleSheet(u"background-color:qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(56, 0, 83, 255), stop:1 rgba(75, 0, 149, 255))")
        self.loginPages.setFrameShape(QFrame.NoFrame)
        self.WelcomePage = QWidget()
        self.WelcomePage.setObjectName(u"WelcomePage")
        self.StinderLogo_3 = QLabel(self.WelcomePage)
        self.StinderLogo_3.setObjectName(u"StinderLogo_3")
        self.StinderLogo_3.setGeometry(QRect(110, -40, 411, 201))
        self.StinderLogo_3.setStyleSheet(u"background-color: transparent;")
        self.StinderLogo_3.setPixmap(QPixmap(u":/logo/images/stinder_logo.png"))
        self.StinderLogo_3.setScaledContents(True)
        self.LoginInput = QLineEdit(self.WelcomePage)
        self.LoginInput.setObjectName(u"LoginInput")
        self.LoginInput.setGeometry(QRect(100, 210, 481, 41))
        self.LoginInput.setStyleSheet(u"background-color: white;\n"
                                      "border-radius: 10px;\n"
                                      "font: 300 13pt Nexa;\n"
                                      "padding: 0 8px;\n"
                                      "padding-top: 4px;\n"
                                      "color:black")
        self.LogInBtn = QPushButton(self.WelcomePage)
        self.LogInBtn.setObjectName(u"LogInBtn")
        self.LogInBtn.setGeometry(QRect(100, 280, 481, 31))
        self.LogInBtn.setStyleSheet(u"background-color: rgb(106,255,121);\n"
                                    "border-radius: 10px;\n"
                                    "font: 700 13pt \"NexaBold\";\n"
                                    "color: white;")
        self.SignInInstruct = QLabel(self.WelcomePage)
        self.SignInInstruct.setObjectName(u"SignInInstruct")
        self.SignInInstruct.setGeometry(QRect(160, 120, 341, 51))
        self.SignInInstruct.setStyleSheet(u"background-color: transparent;\n"
                                          "color: white;\n"
                                          "font:  700 24p5 \"NexaBold\";")
        self.NewLabel = QLabel(self.WelcomePage)
        self.NewLabel.setObjectName(u"NewLabel")
        self.NewLabel.setGeometry(QRect(100, 330, 111, 16))
        self.NewLabel.setStyleSheet(u"background-color: transparent;\n"
                                    "color: white;\n"
                                    "font: 600 11pt \"NexaBold\";")
        self.SignUpBtn = QPushButton(self.WelcomePage)
        self.SignUpBtn.setObjectName(u"SignUpBtn")
        self.SignUpBtn.setGeometry(QRect(215, 327, 61, 24))
        self.SignUpBtn.setStyleSheet(u"background-color: transparent;\n"
                                     "color: rgb(106,255,121);;\n"
                                     "font: 600 11pt \"NexaBold\";")
        self.errorLabelP1 = QLabel(self.WelcomePage)
        self.errorLabelP1.setObjectName(u"errorLabelP1")
        self.errorLabelP1.setGeometry(QRect(110, 259, 491, 16))
        self.errorLabelP1.setStyleSheet(u"background-color: transparent;\n"
                                        "color: red;")
        self.loginPages.addWidget(self.WelcomePage)
        self.BasicPage = QWidget()
        self.BasicPage.setObjectName(u"BasicPage")
        self.StinderLogo = QLabel(self.BasicPage)
        self.StinderLogo.setObjectName(u"StinderLogo")
        self.StinderLogo.setGeometry(QRect(110, -40, 411, 201))
        self.StinderLogo.setStyleSheet(u"background-color: transparent;")
        self.StinderLogo.setPixmap(QPixmap(u":/logo/images/stinder_logo.png"))
        self.StinderLogo.setScaledContents(True)
        self.InstructLabel = QLabel(self.BasicPage)
        self.InstructLabel.setObjectName(u"InstructLabel")
        self.InstructLabel.setGeometry(QRect(150, 100, 361, 41))
        self.InstructLabel.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"font: 700 24pt \"Nexa\";")
        #QFontDatabase.addApplicationFont(":/fonts/fonts/NexaHeavy.otf")
        self.FirstNameInput = QLineEdit(self.BasicPage)
        self.FirstNameInput.setObjectName(u"FirstNameInput")
        self.FirstNameInput.setGeometry(QRect(50, 160, 231, 41))
        self.FirstNameInput.setStyleSheet(u"background-color: white;\n"
"border-radius: 10px;\n"
"font: 300 13pt \"Nexa\";\n"
"padding: 0 8px;\n"
"color: black;\n"
"padding-top: 4px;")
        self.LastNameTb = QLineEdit(self.BasicPage)
        self.LastNameTb.setObjectName(u"LastNameTb")
        self.LastNameTb.setGeometry(QRect(350, 160, 251, 41))
        self.LastNameTb.setStyleSheet(u"background-color: white;\n"
"border-radius: 10px;\n"
"font: 300 13pt \"Nexa\";\n"
"padding: 0 8px;\n"
"color: black;\n"
"padding-top: 4px;")
        self.EmailInput = QLineEdit(self.BasicPage)
        self.EmailInput.setObjectName(u"EmailInput")
        self.EmailInput.setGeometry(QRect(50, 230, 551, 41))
        self.EmailInput.setStyleSheet(u"background-color: white;\n"
"border-radius: 10px;\n"
"font: 300 13pt \"Nexa\";\n"
"padding: 0 8px;\n"
"color: black;\n"
"padding-top: 4px;")
        self.MajorInput = QComboBox(self.BasicPage)
        self.MajorInput.addItem("")
        self.MajorInput.addItem("")
        self.MajorInput.addItem("")
        self.MajorInput.addItem("")
        self.MajorInput.addItem("")
        self.MajorInput.addItem("")
        self.MajorInput.addItem("")
        self.MajorInput.addItem("")
        self.MajorInput.addItem("")
        self.MajorInput.addItem("")
        self.MajorInput.addItem("")
        self.MajorInput.addItem("")
        self.MajorInput.addItem("")
        self.MajorInput.addItem("")
        self.MajorInput.addItem("")
        self.MajorInput.addItem("")
        self.MajorInput.addItem("")
        self.MajorInput.addItem("")
        self.MajorInput.addItem("")
        self.MajorInput.addItem("")
        self.MajorInput.addItem("")
        self.MajorInput.addItem("")
        self.MajorInput.setObjectName(u"MajorInput")
        self.MajorInput.setGeometry(QRect(50, 300, 551, 41))
        self.MajorInput.setStyleSheet(u"background-color: white;\n"
"border-radius: 10px;\n"
"font: 300 13pt \"Nexa\";\n"
"padding: 0 8px;\n"
"padding-top: 4px;"
"color: black;")
        self.MajorInput.setEditable(False)
        self.ContinueBtn = QPushButton(self.BasicPage)
        self.ContinueBtn.setObjectName(u"ContinueBtn")
        self.ContinueBtn.setGeometry(QRect(50, 390, 551, 31))
        self.ContinueBtn.setStyleSheet(u"background-color: rgb(106,255,121);\n"
"border-radius: 10px;\n"
"font: 700 13pt \"Nexa\";\n"
"color: white;")
        # self.ContinueBtn.setFont()
        self.errorLabel = QLabel(self.BasicPage)
        self.errorLabel.setObjectName(u"errorLabel")
        self.errorLabel.setGeometry(QRect(60, 347, 491, 16))
        self.errorLabel.setStyleSheet(u"background-color: transparent;\n"
"color: red;")
        self.label = QLabel(self.BasicPage)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(200, 430, 181, 16))
        self.label.setStyleSheet(u"background-color: transparent;\n"
                                 "color: white;\n"
                                 "font: 600 11pt \"NexaBold\";")
        self.SignInBtn = QPushButton(self.BasicPage)
        self.SignInBtn.setObjectName(u"SignInBtn")
        self.SignInBtn.setGeometry(QRect(376, 426, 73, 24))
        self.SignInBtn.setStyleSheet(u"background-color: transparent;\n"
                                     "color: rgb(106,255,121);;\n"
                                     "font: 600 11pt \"NexaBold\";")
        self.loginPages.addWidget(self.BasicPage)
        self.DetailPage = QWidget()
        self.DetailPage.setObjectName(u"DetailPage")
        self.StinderLogo_2 = QLabel(self.DetailPage)
        self.StinderLogo_2.setObjectName(u"StinderLogo_2")
        self.StinderLogo_2.setGeometry(QRect(110, -40, 411, 201))
        self.StinderLogo_2.setStyleSheet(u"background-color: transparent;")
        self.StinderLogo_2.setPixmap(QPixmap(u":/logo/images/stinder_logo.png"))
        self.StinderLogo_2.setScaledContents(True)
        self.YearInput = QComboBox(self.DetailPage)
        self.YearInput.addItem("")
        self.YearInput.addItem("")
        self.YearInput.addItem("")
        self.YearInput.addItem("")
        self.YearInput.addItem("")
        self.YearInput.setObjectName(u"YearInput")
        self.YearInput.setGeometry(QRect(30, 160, 271, 41))
        self.YearInput.setStyleSheet(u"background-color: white;\n"
"border-radius: 10px;\n"
"font: 300 13pt \"Nexa\";\n"
"padding: 0 8px;\n"
"padding-top: 4px;"
"color:black;\n"
"border: 0px;")
        self.YearInput.setEditable(False)
        self.MethodInput = QComboBox(self.DetailPage)
        self.MethodInput.addItem("")
        self.MethodInput.addItem("")
        self.MethodInput.addItem("")
        self.MethodInput.addItem("")
        self.MethodInput.addItem("")
        self.MethodInput.setObjectName(u"MethodInput")
        self.MethodInput.setGeometry(QRect(30, 250, 271, 41))
        self.MethodInput.setStyleSheet(u"background-color: white;\n"
"border-radius: 10px;\n"
"font: 300 13pt \"Nexa\";\n"
"padding: 0 8px;\n"
"padding-top: 4px;"
"color:black;\n"
"border: 0px;")
        self.MethodInput.setEditable(False)
        self.YearLabel = QLabel(self.DetailPage)
        self.YearLabel.setObjectName(u"YearLabel")
        self.YearLabel.setGeometry(QRect(30, 130, 131, 16))
        self.YearLabel.setStyleSheet(u"background-color:transparent;\n"
"color:white;")
        self.MethodLabel = QLabel(self.DetailPage)
        self.MethodLabel.setObjectName(u"MethodLabel")
        self.MethodLabel.setGeometry(QRect(30, 220, 231, 16))
        self.MethodLabel.setStyleSheet(u"background-color:transparent;\n"
"color:white;")
        self.LocInput = QComboBox(self.DetailPage)
        self.LocInput.addItem("")
        self.LocInput.addItem("")
        self.LocInput.addItem("")
        self.LocInput.addItem("")
        self.LocInput.addItem("")
        self.LocInput.setObjectName(u"LocInput")
        self.LocInput.setGeometry(QRect(30, 340, 271, 41))
        self.LocInput.setStyleSheet(u"background-color: white;\n"
"border-radius: 10px;\n"
"font: 300 13pt \"Nexa\";\n"
"padding: 0 8px;\n"
"padding-top: 4px;"
"color:black;\n"
"border: 0px;")
        self.LocInput.setEditable(False)
        self.LocLabel = QLabel(self.DetailPage)
        self.LocLabel.setObjectName(u"LocLabel")
        self.LocLabel.setGeometry(QRect(30, 310, 231, 16))
        self.LocLabel.setStyleSheet(u"background-color:transparent;\n"
"color:white;")
        self.JobInput = QComboBox(self.DetailPage)
        self.JobInput.addItem("")
        self.JobInput.addItem("")
        self.JobInput.addItem("")
        self.JobInput.setObjectName(u"JobInput")
        self.JobInput.setGeometry(QRect(350, 160, 261, 41))
        self.JobInput.setStyleSheet(u"background-color: white;\n"
"border-radius: 10px;\n"
"font: 300 13pt \"Nexa\";\n"
"padding: 0 8px;\n"
"padding-top: 4px;"
"color:black;\n"
"border: 0px;")
        self.JobInput.setEditable(False)
        self.JobInput.setIconSize(QSize(0, 0))
        self.JobLabel = QLabel(self.DetailPage)
        self.JobLabel.setObjectName(u"JobLabel")
        self.JobLabel.setGeometry(QRect(350, 130, 171, 16))
        self.JobLabel.setStyleSheet(u"background-color:transparent;\n"
"color:white;")
        self.TimeInput = QComboBox(self.DetailPage)
        self.TimeInput.addItem("")
        self.TimeInput.addItem("")
        self.TimeInput.addItem("")
        self.TimeInput.addItem("")
        self.TimeInput.addItem("")
        self.TimeInput.addItem("")
        self.TimeInput.addItem("")
        self.TimeInput.addItem("")
        self.TimeInput.setObjectName(u"TimeInput")
        self.TimeInput.setGeometry(QRect(350, 250, 261, 41))
        self.TimeInput.setStyleSheet(u"background-color: white;\n"
"border-radius: 10px;\n"
"font: 300 13pt \"Nexa\";\n"
"padding: 0 8px;\n"
"padding-top: 4px;"
"color:black;\n"
"border: 0px;")
        self.TimeInput.setEditable(False)
        self.TimeInput.setIconSize(QSize(0, 0))
        self.TimeLabel = QLabel(self.DetailPage)
        self.TimeLabel.setObjectName(u"TimeLabel")
        self.TimeLabel.setGeometry(QRect(350, 220, 251, 16))
        self.TimeLabel.setStyleSheet(u"background-color:transparent;\n"
"color:white;")
        self.StudyHistLabel = QLabel(self.DetailPage)
        self.StudyHistLabel.setObjectName(u"StudyHistLabel")
        self.StudyHistLabel.setGeometry(QRect(350, 310, 261, 16))
        self.StudyHistLabel.setStyleSheet(u"background-color:transparent;\n"
"color:white;")
        self.StudyHistInput = QComboBox(self.DetailPage)
        self.StudyHistInput.addItem("")
        self.StudyHistInput.addItem("")
        self.StudyHistInput.addItem("")
        self.StudyHistInput.setObjectName(u"StudyHistInput")
        self.StudyHistInput.setGeometry(QRect(350, 340, 261, 41))
        self.StudyHistInput.setStyleSheet(u"background-color: white;\n"
"border-radius: 10px;\n"
"font: 300 13pt \"Nexa\";\n"
"padding: 0 8px;\n"
"padding-top: 4px;"
"color:black;\n"
"border: 0px;")
        self.StudyHistInput.setEditable(False)
        self.StudyHistInput.setIconSize(QSize(0, 0))
        self.ContinueBtnP2 = QPushButton(self.DetailPage)
        self.ContinueBtnP2.setObjectName(u"ContinueBtnP2")
        self.ContinueBtnP2.setGeometry(QRect(40, 420, 561, 31))
        self.ContinueBtnP2.setStyleSheet(u"background-color: rgb(106,255,121);\n"
"border-radius: 10px;\n"
"font: 700 13pt \"Nexa\";\n"
"color: white;")
        self.errorLabelP2 = QLabel(self.DetailPage)
        self.errorLabelP2.setObjectName(u"errorLabelP2")
        self.errorLabelP2.setGeometry(QRect(30, 390, 491, 16))
        self.errorLabelP2.setStyleSheet(u"background-color: transparent;\n"
"color: red;")
        self.loginPages.addWidget(self.DetailPage)

        self.retranslateUi(Stinder_Login)

        self.loginPages.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Stinder_Login)
    # setupUi

    def retranslateUi(self, Stinder_Login):
        Stinder_Login.setWindowTitle(QCoreApplication.translate("Stinder_Login", u"Stinder", None))
        self.StinderLogo_3.setText("")
        self.LoginInput.setPlaceholderText(QCoreApplication.translate("Stinder_Login", u"Email Address", None))
        self.LogInBtn.setText(QCoreApplication.translate("Stinder_Login", u"Sign In", None))
        self.SignInInstruct.setText(QCoreApplication.translate("Stinder_Login",
                                                               u"<html><head/><body><p><span style=\" font-size:20pt;\">Enter your email to sign in</span></p></body></html>",
                                                               None))
        self.NewLabel.setText(QCoreApplication.translate("Stinder_Login",
                                                         u"<html><head/><body><p><span style=\" font-size:11pt;\">New to Stinder?</span></p></body></html>",
                                                         None))
        self.SignUpBtn.setText(QCoreApplication.translate("Stinder_Login", u"Sign Up", None))
        self.errorLabelP2.setText("")
        self.StinderLogo.setText("")
        self.InstructLabel.setText(QCoreApplication.translate("Stinder_Login", u"<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">Please fill out form to continue</span></p></body></html>", None))
        self.FirstNameInput.setPlaceholderText(QCoreApplication.translate("Stinder_Login", u"First Name", None))
        self.LastNameTb.setPlaceholderText(QCoreApplication.translate("Stinder_Login", u"Last Name", None))
        self.EmailInput.setPlaceholderText(QCoreApplication.translate("Stinder_Login", u"Email Address", None))
        self.MajorInput.setItemText(0, QCoreApplication.translate("Stinder_Login", u"---Please Select Major---", None))
        self.MajorInput.setItemText(1, QCoreApplication.translate("Stinder_Login", u"Accounting", None))
        self.MajorInput.setItemText(2, QCoreApplication.translate("Stinder_Login", u"Aerospace Engineering", None))
        self.MajorInput.setItemText(3, QCoreApplication.translate("Stinder_Login", u"Anthropology", None))
        self.MajorInput.setItemText(4, QCoreApplication.translate("Stinder_Login", u"Biology", None))
        self.MajorInput.setItemText(5, QCoreApplication.translate("Stinder_Login", u"Botany", None))
        self.MajorInput.setItemText(6, QCoreApplication.translate("Stinder_Login", u"Chemistry", None))
        self.MajorInput.setItemText(7, QCoreApplication.translate("Stinder_Login", u"Computer Science", None))
        self.MajorInput.setItemText(8, QCoreApplication.translate("Stinder_Login", u"Data Science", None))
        self.MajorInput.setItemText(9, QCoreApplication.translate("Stinder_Login", u"Economics", None))
        self.MajorInput.setItemText(10, QCoreApplication.translate("Stinder_Login", u"Education", None))
        self.MajorInput.setItemText(11, QCoreApplication.translate("Stinder_Login", u"Finance", None))
        self.MajorInput.setItemText(12, QCoreApplication.translate("Stinder_Login", u"Geography", None))
        self.MajorInput.setItemText(13, QCoreApplication.translate("Stinder_Login", u"History", None))
        self.MajorInput.setItemText(14, QCoreApplication.translate("Stinder_Login", u"Information Systems", None))
        self.MajorInput.setItemText(15, QCoreApplication.translate("Stinder_Login", u"Journalism", None))
        self.MajorInput.setItemText(16, QCoreApplication.translate("Stinder_Login", u"Marketing", None))
        self.MajorInput.setItemText(17, QCoreApplication.translate("Stinder_Login", u"Nuclear Engineering", None))
        self.MajorInput.setItemText(18, QCoreApplication.translate("Stinder_Login", u"Physics", None))
        self.MajorInput.setItemText(19, QCoreApplication.translate("Stinder_Login", u"Religion", None))
        self.MajorInput.setItemText(20, QCoreApplication.translate("Stinder_Login", u"Sociology", None))
        self.MajorInput.setItemText(21, QCoreApplication.translate("Stinder_Login", u"Theatre", None))

        self.MajorInput.setPlaceholderText(QCoreApplication.translate("Stinder_Login", u"Major", None))
        self.ContinueBtn.setText(QCoreApplication.translate("Stinder_Login", u"Continue", None))
        self.errorLabel.setText("")
        self.label.setText(QCoreApplication.translate("Stinder_Login", u"Already have an account?", None))
        self.SignInBtn.setText(QCoreApplication.translate("Stinder_Login", u"Sign In", None))
        self.StinderLogo_2.setText("")
        self.YearInput.setItemText(0, QCoreApplication.translate("Stinder_Login", u"---Please Select---"))
        self.YearInput.setItemText(1, QCoreApplication.translate("Stinder_Login", u"Freshman", None))
        self.YearInput.setItemText(2, QCoreApplication.translate("Stinder_Login", u"Sophomore", None))
        self.YearInput.setItemText(3, QCoreApplication.translate("Stinder_Login", u"Junior", None))
        self.YearInput.setItemText(4, QCoreApplication.translate("Stinder_Login", u"Senior", None))

        self.YearInput.setPlaceholderText(QCoreApplication.translate("Stinder_Login", u"Year", None))
        self.MethodInput.setItemText(0, QCoreApplication.translate("Stinder_Login", u"---Please Select---", None))
        self.MethodInput.setItemText(1, QCoreApplication.translate("Stinder_Login", u"Flashcards", None))
        self.MethodInput.setItemText(2, QCoreApplication.translate("Stinder_Login", u"Reading through your textbook", None))
        self.MethodInput.setItemText(3, QCoreApplication.translate("Stinder_Login", u"Doing practice problems", None))
        self.MethodInput.setItemText(4, QCoreApplication.translate("Stinder_Login", u"Reviewing your own notes", None))

        self.MethodInput.setPlaceholderText(QCoreApplication.translate("Stinder_Login", u"Study Method", None))
        self.YearLabel.setText(QCoreApplication.translate("Stinder_Login", u"Student Classification", None))
        self.MethodLabel.setText(QCoreApplication.translate("Stinder_Login", u"What's your preferred study method?", None))
        self.LocInput.setItemText(0, QCoreApplication.translate("Stinder_Login", u"---Please Select---", None))
        self.LocInput.setItemText(1, QCoreApplication.translate("Stinder_Login", u"Library", None))
        self.LocInput.setItemText(2, QCoreApplication.translate("Stinder_Login", u"Place of residence", None))
        self.LocInput.setItemText(3, QCoreApplication.translate("Stinder_Login", u"Outdoor park", None))
        self.LocInput.setItemText(4, QCoreApplication.translate("Stinder_Login", u"Coffee shop", None))

        self.LocInput.setPlaceholderText(QCoreApplication.translate("Stinder_Login", u"Study Location", None))
        self.LocLabel.setText(QCoreApplication.translate("Stinder_Login", u"Where do you like to study?", None))
        self.JobInput.setItemText(0, QCoreApplication.translate("Stinder_Login", u"---Please Select---", None))
        self.JobInput.setItemText(1, QCoreApplication.translate("Stinder_Login", u"Yes", None))
        self.JobInput.setItemText(2, QCoreApplication.translate("Stinder_Login", u"No", None))

        self.JobInput.setPlaceholderText(QCoreApplication.translate("Stinder_Login", u"Choose", None))
        self.JobLabel.setText(QCoreApplication.translate("Stinder_Login", u"Are you currently employed?", None))
        self.TimeInput.setItemText(0, QCoreApplication.translate("Stinder_Login", u"---Please Select---", None))
        self.TimeInput.setItemText(1, QCoreApplication.translate("Stinder_Login", u"Monday", None))
        self.TimeInput.setItemText(2, QCoreApplication.translate("Stinder_Login", u"Tuesday", None))
        self.TimeInput.setItemText(3, QCoreApplication.translate("Stinder_Login", u"Wednesday", None))
        self.TimeInput.setItemText(4, QCoreApplication.translate("Stinder_Login", u"Thursday", None))
        self.TimeInput.setItemText(5, QCoreApplication.translate("Stinder_Login", u"Friday", None))
        self.TimeInput.setItemText(6, QCoreApplication.translate("Stinder_Login", u"Saturday", None))
        self.TimeInput.setItemText(7, QCoreApplication.translate("Stinder_Login", u"Sunday", None))

        self.TimeInput.setPlaceholderText(QCoreApplication.translate("Stinder_Login", u"Choose", None))
        self.TimeLabel.setText(QCoreApplication.translate("Stinder_Login", u"What day do you prefer to study?", None))
        self.StudyHistLabel.setText(QCoreApplication.translate("Stinder_Login", u"Have you studied with other people before?", None))
        self.StudyHistInput.setItemText(0, QCoreApplication.translate("Stinder_Login", u"---Please Select---", None))
        self.StudyHistInput.setItemText(1, QCoreApplication.translate("Stinder_Login", u"Yes", None))
        self.StudyHistInput.setItemText(2, QCoreApplication.translate("Stinder_Login", u"No", None))

        self.StudyHistInput.setPlaceholderText(QCoreApplication.translate("Stinder_Login", u"Choose", None))
        self.ContinueBtnP2.setText(QCoreApplication.translate("Stinder_Login", u"Continue", None))
        self.errorLabelP2.setText("")
    # retranslateUi