from PyQt5.QtWidgets import (QLineEdit, QPushButton, QGridLayout, QLabel,
                             QVBoxLayout, QGroupBox,
                             QDialogButtonBox, QMessageBox, QHBoxLayout)
from PyQt5.QtCore import QDate

from ui.dialog import Dialog
from ui.widgets import (FilteringComboBox, DateEdit, LineEdit, PrimaryButton)
from config import (CATEGORY_ICO, ROOT_CAUSE_ICO, DESCRIPTION_ICO,
                    REQUESTED_CD_ICO, DATE_OBSERVED_ICO)


class NewIssueDialog(Dialog):
    """docstring for [object Object]"""
    def __init__(self, parent, title='New Issue'):
        super(NewIssueDialog, self).__init__(parent, title)
        height = self.screen_geometry.height()
        width = self.screen_geometry.width()
        self.setFixedSize(width * 0.35, height * 0.6)

    def createButtons(self):
        """Creates dialog buttons

        Returns:
            buttons ({name:QPushbutton}): dictionary containing dialog buttons
        """
        # Define
        buttons = {
            'Submit': PrimaryButton('SUBMIT'),
            'Cancel': PrimaryButton('CANCEL'),
            'New Task': QPushButton('New Task')
        }

        # Make connections
        buttons['Submit'].clicked.connect(self.validate)
        buttons['Cancel'].clicked.connect(self.reject)
        buttons['New Task'].clicked.connect(self.add_task)

        return buttons

    def createEditors(self):
        """Creates dialog input widgets.
           Override base class for specific forms"""
        today = QDate().currentDate()
        min_OD = today.addDays(-7)
        editors = {
            'OD': DateEdit(
                parent=self, placeholderText='Date Observed',
                minimumDate=min_OD, image=DATE_OBSERVED_ICO),
            'Tool': FilteringComboBox(
                parent=self, placeholderText='Tool',
                table='tool', column='name'),
            'Category': FilteringComboBox(
                parent=self, placeholderText='Category',
                table='category', column='name', image=CATEGORY_ICO),
            'Description': LineEdit(
                parent=self, placeholderText='Short Description',
                image=DESCRIPTION_ICO),
            'Root Cause': LineEdit(
                parent=self,
                placeholderText='Possible root cause of the issue, if known',
                image=ROOT_CAUSE_ICO),
            'RCD': DateEdit(
                parent=self, placeholderText='Requested Completion Date',
                minimumDate=today, image=REQUESTED_CD_ICO),
            # 'Tasks': PlainTextEdit(
            #     parent=self,
            #     placeholderText='Add tasks required for issue resoltion')
        }
        return editors

    def add_task(self):
        task_limit = 5
        # find new task number:
        number = 1
        for name, _ in self.editors.items():
            if 'Task' in name:
                number += 1

        # check number of tasks limit
        if number > task_limit:
            msg = QMessageBox()
            msg.setWindowTitle('New Task Warning!')
            msg.setText('Number of taks exceeds limit {}'.format(task_limit))
            msg.exec_()
            return

        # add new editor for this Tasks
        name = 'Task' + str(number)
        self.editors[name] = QLineEdit()

        # add new editor to self.task_layout
        h_layout = QHBoxLayout()
        h_layout.addWidget(QLabel(str(number) + '.'))
        h_layout.addWidget(self.editors[name])
        self.tasks_layout.addLayout(h_layout)

    def createContentsLayout(self):
        """Returns dialog layout containing all dialog widgetsself.
           Base class returns empty QGridLayout

        Returns:
            layout (QLayout)
        """
        # Tasks layout
        self.tasks_layout = QVBoxLayout()
        self.button_bar = QDialogButtonBox()
        self.button_bar.addButton(self.buttons['Submit'],
                                  QDialogButtonBox.AcceptRole)
        self.button_bar.addButton(self.buttons['Cancel'],
                                  QDialogButtonBox.RejectRole)

        tasks = QGroupBox('TASKS')
        tasks.setStyleSheet(
            """QGroupBox {
                font: bold 16pt;}""")
        tasks_layout = QVBoxLayout()
        tasks.setLayout(tasks_layout)

        # Setup layout
        layout = QGridLayout()
        layout.setSpacing(15)
        layout.addWidget(self.editors['Tool'], 0, 0, 1, 2)
        layout.addWidget(self.editors['OD'], 0, 3, 1, 2)
        layout.addWidget(self.editors['Category'], 1, 0, 1, 2)
        layout.addWidget(self.editors['RCD'], 1, 3, 1, 2)
        layout.addWidget(self.editors['Description'], 2, 0, 1, 5)
        layout.addWidget(self.editors['Root Cause'], 3, 0, 1, 5)
        layout.setRowMinimumHeight(4, 20)
        layout.addWidget(tasks, 5, 0, 1, 4)
        layout.addWidget(self.buttons['New Task'], 5, 4, 1, 1)
        layout.setRowMinimumHeight(6, 20)
        layout.addWidget(self.buttons['Submit'], 7, 0, 1, 1)
        layout.addWidget(self.buttons['Cancel'], 7, 1, 1, 1)
        layout.setColumnMinimumWidth(2, 40)
        layout.setRowStretch(6, 1)
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

        return None
