from PyQt5.QtCore import QCoreApplication, QFileSystemWatcher
from PyQt5.QtGui import QIcon
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QMessageBox, QVBoxLayout, QWidget)

from config import DB_PATH, DENTON_LOGO_ICO

from ui.login_dialog import LoginDialog
from ui.signup_dialog import SignupDialog
from ui.new_issue_dialog import NewIssueDialog


class MainWindow(QMainWindow):
    """MainWindow class to create GUI inteface for the Application.

    Key Atrributes:
        access (str): user access level. Access level determines visibility of
                 various Application actions(features) to user.
        active_dialogs ([]): list of open tableview edit dialogs
        tableviews ([]): list containing Application tableviews
        user (str): user full name for the Application session
        user_id (int)
        user_name (str): user name for the Application session
        user_settings ({setting_type (str): setting})
    """

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.mainWindow = self
        # self.tableviews = []
        self.active_dialogs = []
        self.user_name = None
        self.user_id = None
        self.user_settings = None
        self.user = None
        self.access = 'login'

        self.addDatabase()
        self.initUi()
        self.showMaximized()

    def addDatabase(self, database=DB_PATH):
        """Adds database connection"""
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(database)
        if not self.db.open():
            QMessageBox.critical(
                None, "Cannot open database",
                "Unable to establish a database connection.\n"
                "This example needs SQLite support. Please read the Qt SQL "
                "driver documentation for information how to build it.\n\n"
                "Click Cancel to exit.",
                QMessageBox.Cancel)
            self.close()
            QCoreApplication.instance().quit()
        self.db_watcher = QFileSystemWatcher(self)
        self.db_watcher.addPath(database)
        self.db_watcher.fileChanged.connect(self.handleDBChanged)

    def center(self):
        """Centers main window on the active screen"""
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(
                              QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def closeEvent(self, event):
        self.close()
        QCoreApplication.instance().quit()

    def forgotPassword(self):
        print('Forgot password accesed')

    def handleDBChanged(self):
        """Handles changes in the database file.
           Refreshes models for all active dialogs
           TableViews are refreshed automatically through ProxyModels
        """
        for dialog in self.active_dialogs:
            dialog.updateEditorModels()

    def initUi(self):
        """Initializes application main window"""

        self.setWindowTitle('Denton Service Request Management System')
        self.setWindowIcon(QIcon(DENTON_LOGO_ICO))
        self.statusBar()
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.setMinimumSize(700, 500)
        self.default_font = self.font()

    def promptLogin(self):
        """Displays Login dialog asking for user name and password
           Upon successful login:
                fetches user_id, access, full name, settings
                Loads full UI
                Logs login
        """
        dialog = LoginDialog(parent=self)
        dialog.accepted.connect(
            lambda: self.login(user_name=dialog.data()['User Name']))
        dialog.show()
        dialog.center(parent=self)

    def login(self, user_name):
        self.user_name, self.user_id, self.access, self.user = \
            self.userInfo(user_name=user_name)
        print('successful login')
        dialog = NewIssueDialog(parent=self)
        dialog.show()
        dialog.center(parent=self)

    def promptSignUp(self):
        dialog = SignupDialog(parent=self)
        dialog.accepted.connect(lambda: self.signUp(data=dialog.data()))
        dialog.show()
        dialog.center(parent=self)

    def signUp(self, data):
        pass

    def userInfo(self, user_name=None):
        """Returns user settings stored as dictionary

        Returns:
            (user_name (str, None),
             user id (int, None),
             user access (str, None),
             user full name (str, None))
        """
        if user_name is None:
            return (None, None, None, None)

        query = QSqlQuery()
        query.prepare("""SELECT user.id, user_access.name, user.name
                         FROM user JOIN user_access ON
                         user.user_access_id=user_access.id
                         WHERE user_name=:user_name""")
        query.bindValue(':user_name', user_name)
        query.exec_()
        query.next()
        user_name = user_name
        user_id = query.value(0)
        access = query.value(1)
        user = query.value(2)
        return (user_name, user_id, access, user)
