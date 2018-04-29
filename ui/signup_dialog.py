from PyQt5.QtWidgets import (QLineEdit, QGridLayout)
from PyQt5.QtSql import QSqlQuery

from ui.dialog import Dialog
from ui.widgets import FilteringComboBox, LineEdit, PrimaryButton


class SignupDialog(Dialog):
    """docstring for [object Object]"""
    def __init__(self, parent, title='Sign up'):
        super(SignupDialog, self).__init__(parent, title)
        self.setWindowTitle('Signup')

    def createButtons(self):
        """Creates dialog buttons

        Returns:
            buttons ({name:QPushbutton}): dictionary containing dialog buttons
        """
        # Define
        buttons = {
            'Signup': PrimaryButton('Sign Up'),
            'Cancel': PrimaryButton('Cancel'),
        }

        # Make connections
        buttons['Signup'].clicked.connect(self.validate)
        buttons['Cancel'].clicked.connect(self.reject)

        return buttons

    def createEditors(self):
        """Creates dialog input widgets.
           Override base class for specific forms"""
        editors = {
            'First Name': LineEdit(
                parent=self, placeholderText='First Name'),
            'Last Name': LineEdit(
                parent=self, placeholderText='Last Name'),
            'User Name': LineEdit(
                parent=self, placeholderText='User Name'),
            'Password': LineEdit(
                parent=self, placeholderText='Password'),
            'Confirm Password': LineEdit(
                parent=self, placeholderText='Repeat Password'),
            'Group': FilteringComboBox(
                parent=self, placeholderText='Group',
                table='department', column='name')
        }
        editors['Password']._editor.setEchoMode(QLineEdit.Password)
        editors['Confirm Password']._editor.setEchoMode(QLineEdit.Password)

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
        layout.addWidget(self.editors['First Name'], 1, 0, 1, 3)
        layout.addWidget(self.editors['Last Name'], 2, 0, 1, 3)
        layout.addWidget(self.editors['User Name'], 3, 0, 1, 3)
        layout.addWidget(self.editors['Password'], 4, 0, 1, 3)
        layout.addWidget(self.editors['Confirm Password'], 5, 0, 1, 3)
        layout.addWidget(self.editors['Group'], 6, 0, 1, 3)
        layout.addWidget(self.buttons['Signup'], 8, 2, 1, 1)
        layout.addWidget(self.buttons['Cancel'], 8, 0, 1, 1)
        layout.setContentsMargins(50, 20, 50, 50)
        layout.setRowMinimumHeight(7, 20)
        return layout

    def validationTest(self, data):
        """Validates user input.
           Resets fields that do not pass validation test

        Args:
            data ({name: value}): dialog user input data

        Returns:
            (str or None): str if error found, None otherwise

        """
        # Validate inputs
        ####################################
        # check for empty inputs
        if any(x == '' or x is None for x in data.values()):
            return 'Missing infomation'

        user_name = data['User Name']
        pwd = data['Password']
        confirm_pwd = data['Confirm Password']

        # Check duplicate user_name in database
        query = QSqlQuery()
        query.prepare("""SELECT id from user
                         WHERE user_name=:user_name""")
        query.bindValue(':user_name', user_name)
        query.exec_()
        query.next()
        if query.isValid():
            self.editors['User Name'].setValue('')
            return 'User name already exists'

        # Check password integrity
        if len(pwd) < 8 or len(pwd) > 32:
            self.editors['Password'].setValue('')
            self.editors['Confirm Password'].setValue('')
            return 'Password must be between 8 and 32 characters long!'

        # Check repeat password matches
        if pwd != confirm_pwd:
            self.editors['Password'].setValue('')
            self.editors['Confirm Password'].setValue('')
            return 'Passowrd do not match!'

        return None
