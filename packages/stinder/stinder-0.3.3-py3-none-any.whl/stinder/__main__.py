import sqlite3
import os
import re
import sys

from pkg_resources import resource_filename

from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QSizePolicy, QTableWidgetItem
from PySide6.QtSql import QSqlDatabase, QSqlQuery
from PySide6.QtGui import QIcon
from sqlite3 import Error

from stinder.home import Ui_Stinder
from stinder.login import Ui_Stinder_Login
from stinder.resources.images import *
from stinder.resources.fonts import *

from stinder.stinder_images_rc import *

class LogInWindow(QDialog):
    def __init__(self):
        super(LogInWindow, self).__init__()
        self.setFixedSize(646, 476)
        self.setIcon()
        self.loginUi = Ui_Stinder_Login()
        self.loginUi.setupUi(self)
        self.user = None

        # PAGE 1
        self.loginUi.LogInBtn.clicked.connect(self.handleSignIn)
        self.loginUi.SignUpBtn.clicked.connect(lambda: self.loginUi.loginPages.setCurrentWidget(self.loginUi.BasicPage))
        # PAGE 2
        self.loginUi.ContinueBtn.clicked.connect(self.handleBasicPage)
        # PAGE 3
        self.loginUi.ContinueBtnP2.clicked.connect(self.handleCreateAcct)
        self.loginUi.SignInBtn.clicked.connect(lambda: self.loginUi.loginPages.setCurrentWidget(self.loginUi.WelcomePage))

    # Override close event to close whole app when dialog is closed
    def closeEvent(self, event):
        sys.exit()

    def setIcon(self):
        appIcon = QIcon(resource_filename(__name__, "resources/images/stinder_book_logo.png"))
        self.setWindowIcon(appIcon)

    def setEmail(self, email):
        self.user = email

    def getEmail(self):
        return self.user

    def checkEmail(self, email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.match(regex, email)):
            return True
        else:
            return False

    def handleSignIn(self):
        email = self.loginUi.LoginInput.text()
        exists_conn = sqlite3.connect(resource_filename(__name__, "users.db"))
        curs = exists_conn.cursor()

        if len(email) == 0:
            self.loginUi.errorLabelP1.setText("Please input an email address.")
        elif not self.checkEmail(email):
            self.loginUi.errorLabelP1.setText("Invalid Email.")
        elif curs.execute("SELECT * FROM contacts WHERE email = ?", (email,)).fetchone():
            exists_conn.close()
            self.setEmail(email)
            self.accept()
        else:
            self.loginUi.errorLabelP1.setText("Email address not found.")

    def handleBasicPage(self):
        fName = self.loginUi.FirstNameInput.text()
        lName = self.loginUi.LastNameTb.text()
        email = self.loginUi.EmailInput.text()
        major = self.loginUi.MajorInput.currentText()

        if len(fName) == 0 or len(lName) == 0 or len(email) == 0 or major == "---Please Select Major---":
            self.loginUi.errorLabel.setText("Please input all fields.")
        elif not self.checkEmail(email):
            self.loginUi.errorLabel.setText("Invalid Email.")
        else:
            self.setEmail(email)
            self.loginUi.loginPages.setCurrentWidget(self.loginUi.DetailPage)

    def handleCreateAcct(self):
        # check if login is valid
        fName = self.loginUi.FirstNameInput.text()
        lName = self.loginUi.LastNameTb.text()
        email = self.loginUi.EmailInput.text()
        major = self.loginUi.MajorInput.currentText()
        year = self.loginUi.YearInput.currentText()
        method = self.loginUi.MethodInput.currentText()
        loc = self.loginUi.LocInput.currentText()
        job = self.loginUi.JobInput.currentText()
        day = self.loginUi.TimeInput.currentText()
        sHistory = self.loginUi.StudyHistInput.currentText()
        placeholder = "---Please Select---"

        if year == placeholder or method == placeholder or loc == placeholder or job == placeholder or \
                day == placeholder or sHistory == placeholder:
            self.loginUi.errorLabelP2.setText("Please input all fields.")
        else:
            login_conn = sqlite3.connect(resource_filename(__name__, "users.db"))
            login_cur = login_conn.cursor()
            login_cur.execute(
                "INSERT OR REPLACE INTO contacts(Fname, Lname, major, email, year, method, loc, job, day, sHistory) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (fName, lName, major, email, year, method, loc, job, day, sHistory)
            )
            login_conn.commit()
            login_conn.close()

            self.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(855, 538)
        self.setIcon()
        self.ui = Ui_Stinder()
        self.ui.setupUi(self)
        self.email = None

        # PAGE 1
        self.ui.AboutButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.AboutPage))
        # PAGE 2
        self.ui.BrowseButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.BrowsePage))
        # PAGE 3
        self.ui.ProfileButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.ProfilePage))

        # If add courses button is pushed, display box and list
        self.ui.AddCoursesBtn.clicked.connect(self.AddCoursesClicked)
        self.ui.AddBtn.clicked.connect(self.AddCourses)
        self.ui.DeleteBtn.clicked.connect(self.DeleteCourses)
        self.ui.DoneBtn.clicked.connect(self.DoneEditing)

        self.ui.LogoutBtn.clicked.connect(self.Logout)

    def Logout(self):
        self.close()
        new_window = MainWindow()
        new_dialog = LogInWindow()

        if new_dialog.exec() == QDialog.Accepted:
            new_window.show()
            new_window.setUser(new_dialog.getEmail())
            new_window.displayCourses(new_dialog.getEmail())

    def DoneEditing(self):
        if self.ui.lCourseListWidget.count() == 0:
            self.ui.courseinstructLabel.setVisible(True)
            self.ui.lCourseListWidget.setVisible(False)

        self.ui.AddBtn.setVisible(False)
        self.ui.DeleteBtn.setVisible(False)
        self.ui.CourseInputEdit.setVisible(False)
        self.ui.DoneBtn.setVisible(False)
        self.ui.AddCoursesBtn.setVisible(True)

    def DeleteCourses(self):
        row = self.ui.lCourseListWidget.currentRow()
        if not self.ui.lCourseListWidget.count() == 0:
            course = self.ui.lCourseListWidget.item(row).text()
            self.ui.lCourseListWidget.takeItem(row)
            profileconn = sqlite3.connect(resource_filename(__name__, "users.db"))
            profilecurs = profileconn.cursor()
            profilecurs.execute("DELETE FROM courses WHERE user_email=? AND code=?", (self.email, course))
            profileconn.commit()
            profileconn.close()

    def AddCourses(self):
        profileconn = sqlite3.connect(resource_filename(__name__, "users.db"))
        profilecurs = profileconn.cursor()
        if self.ui.CourseInputEdit.text() == "":
            # Do nothing
            print("")
        else:
            self.ui.lCourseListWidget.addItem(self.ui.CourseInputEdit.text())
            profilecurs.execute("INSERT INTO courses(user_email, code) VALUES (?, ?)",
                                (self.email, self.ui.CourseInputEdit.text()))
            profileconn.commit()
            profileconn.close()
            self.ui.CourseInputEdit.setText("")

    def AddCoursesClicked(self):
        self.ui.AddCoursesBtn.setVisible(False)
        self.ui.courseinstructLabel.setVisible(False)
        self.ui.AddBtn.setVisible(True)
        self.ui.CourseInputEdit.setVisible(True)
        self.ui.lCourseListWidget.setVisible(True)
        self.ui.DeleteBtn.setVisible(True)
        self.ui.DoneBtn.setVisible(True)

    def displayCourses(self, email):
        self.email = email
        resize = self.ui.lCourseListWidget.sizePolicy()
        resize.setRetainSizeWhenHidden(True)
        self.ui.lCourseListWidget.setSizePolicy(resize)

        self.ui.AddBtn.setVisible(False)
        self.ui.DeleteBtn.setVisible(False)
        self.ui.CourseInputEdit.setVisible(False)
        self.ui.DoneBtn.setVisible(False)

        profileconn = sqlite3.connect(resource_filename(__name__, "users.db"))
        profilecurs = profileconn.cursor()
        user = profilecurs.execute("SELECT * FROM courses WHERE user_email = ?", (email,)).fetchone()
        # If user has no courses, display prompt information and hide everything else
        if not user:
            profilecurs.close()
            self.ui.lCourseListWidget.setVisible(False)
        # If user has courses display courses but not prompt information
        else:
            self.ui.courseinstructLabel.setVisible(False)
            self.ui.lCourseListWidget.setVisible(True)
            courses = profilecurs.execute("SELECT code FROM courses WHERE user_email = ?", (email,)).fetchall()
            for course in courses:
                course_str = str(course)
                self.ui.lCourseListWidget.addItem(course_str.split("\'")[1])
            profilecurs.close()

    def setUser(self, email):
        self.email = email
        profileconn = sqlite3.connect(resource_filename(__name__, "users.db"))
        profilecurs = profileconn.cursor()
        user = profilecurs.execute("SELECT * FROM contacts WHERE email = ? ", (email,)).fetchone()
        name = user[0] + " " + user[1]
        major = user[2]
        profile_email = user[3]
        self.ui.c_user = [ user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7], user[8], user[9] ]
        self.ui.UserName.setText(name)
        self.ui.UserEmail.setText(profile_email)
        self.ui.UserMajor.setText(major)
        

    def setIcon(self):
        appIcon = QIcon(resource_filename(__name__, "resources/images/stinder_book_logo.png"))
        self.setWindowIcon(appIcon)


def main():
    app = QApplication([])
    login = LogInWindow()
    window = MainWindow()

    if login.exec() == QDialog.Accepted:
        window.show()
        window.setUser(login.getEmail())
        window.displayCourses(login.getEmail())

    sys.exit(app.exec())


if __name__ == "__main__":
    main()