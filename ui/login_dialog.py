import bcrypt

from PyQt5.QtWidgets import QLineEdit, QGridLayout
from PyQt5.QtSql import QSqlQuery

from ui.dialog import Dialog
from ui.widgets import LineEdit, HyperlinkButton, PrimaryButton
from config import PWD_ICO, UNAME_ICO


class LoginDialog(Dialog):
    """docstring for LoginDialog."""
    def __init__(self, parent, title='Sign in'):
        super(LoginDialog, self).__init__(parent, title)
        self.setWindowTitle('Login')

    def createButtons(self):
        """Creates dialog buttons

        Returns:
            buttons ({name:QPushbutton}): dictionary containing dialog buttons
        """
        # Define
        buttons = {
            'Login': PrimaryButton('LOGIN'),
            'Forgot Password': HyperlinkButton('Forgot Password?'),
            'Sign Up': HyperlinkButton('First time login? Sign Up')
        }

        # Make connections
        buttons['Login'].clicked.connect(self.validate)
        buttons['Forgot Password'].clicked.\
            connect(self.mainWindow.forgotPassword)
        buttons['Sign Up'].clicked.\
            connect(self.mainWindow.promptSignUp)
        buttons['Sign Up'].clicked.\
            connect(self.reject)

        return buttons

    def createEditors(self):
        """Creates dialog input widgets.
           Override base class for specific forms"""
        editors = {
            'User Name': LineEdit(parent=self, placeholderText='User Name',
                                  image=UNAME_ICO),
            'Password': LineEdit(parent=self, placeholderText='Password',
                                 image=PWD_ICO)
        }
        editors['Password']._editor.setEchoMode(QLineEdit.Password)
        return editors

    def createContentsLayout(self):
        """Returns dialog layout containing all dialog widgetsself.
           Base class returns empty QGridLayout

        Returns:
            layout (QLayout)
        """
        # Setup layout
        layout = QGridLayout()
        layout.setSpacing(15)
        layout.addWidget(self.editors['User Name'], 0, 0, 1, 4)
        layout.addWidget(self.editors['Password'], 1, 0, 1, 4)
        layout.addWidget(self.buttons['Login'], 4, 0, 1, -1)
        layout.addWidget(self.buttons['Forgot Password'], 2, 3, 1, -1)
        layout.addWidget(self.buttons['Sign Up'], 5, 0, 1, -1)
        return layout

    def validationTest(self, data):
        """Validates user input.
           Resets fields that do not pass validation test

        Args:
            data ({name: value}): dialog user input data

        Returns:
            (str or None): str if error found, None otherwise
        """
        user_name = data['User Name'].lower()
        pwd = data['Password']

        # Check missing inputs
        if user_name == '' or pwd == '':
            return 'Missing inputs'

        # Query db for user information
        query = QSqlQuery()
        query.prepare(
            """SELECT id, password FROM user
               WHERE user_name=:uname""")
        query.bindValue(':uname', user_name)
        query.exec_()
        query.next()

        # Check if user is found
        if not query.isValid():
            self.reset()
            return 'User not found!'

        # check password
        db_pwd = query.value(1)
        db_pwd = db_pwd.data()  # converts QByteArray to b'...'
        if not bcrypt.checkpw(pwd.encode(), db_pwd):
            self.editors['Password'].setValue('')
            return 'Incorrect password!'

        return None
