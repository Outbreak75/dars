"""
dialog.py docstring
"""
from PyQt5.QtWidgets import (QDialog, QGraphicsDropShadowEffect, QPushButton,
                             QGridLayout, QMessageBox, QApplication, QWidget,
                             QVBoxLayout, QHBoxLayout, QDialogButtonBox,
                             QScrollArea)
from PyQt5.QtCore import Qt, QPoint

from ui.widgets import FilteringComboBox, DialogTitleBar


class Dialog(QDialog):
    """docstring for Dialog.

    Args:
        parent (QWidget): parent application widget
        default_data ({name: value}): dicitionary containing default data
                       name (str): editor name
                       value (str): editor display value
    """

    def __init__(self,  parent, title='', color='rgb(0,145,234)'):
        super(Dialog, self).__init__(parent)
        self.parent = parent
        self.title = title
        self.color = color

        self.mainWindow = self.parent.mainWindow
        self.screen_geometry = QApplication.primaryScreen().geometry()

        self.editors = self.createEditors()
        self.buttons = self.createButtons()
        self.default_data = {}
        self.initUi()

        # keep track of the dialog in the main application window
        self.mainWindow.active_dialogs.append(self)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def keyPressEvent(self,  event):

        if event.key == Qt.Key_Enter:
            print('enter pressed pressed')
            self.validate()
        else:
            print('enter not pressed pressed')
            super().keyPressEvent(event)

    def createContentsLayout(self):
        """Returns dialog layout containing all dialog widgetsself.
           Base class returns empty QGridLayout

        Returns:
            layout (QLayout)
        """
        layout = QGridLayout()
        return layout

    def initUi(self):
        """Arranges editors and buttons in the Dialog window"""
        style = """
            QDialog {
                border-top: 0px;
                padding: 2px;
                margin: 0px;
                background-color: white;}
        """
        self.setStyleSheet(style)
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self._titleBar = DialogTitleBar(parent=self, title=self.title)

        # setup contents container and scroll area
        self._contents = QWidget()
        self._contents_layout = self.createContentsLayout()
        self._contents_layout.setContentsMargins(50, 50, 50, 50)
        self._contents.setLayout(self._contents_layout)

        # setup scroll area for contents
        self._scroll = QScrollArea()
        self._scroll.setWidget(self._contents)
        self._scroll.setWidgetResizable(True)
        self._scroll.setFixedHeight(self.height() + 500)
        self._scroll.setObjectName('scroll')
        self._scroll.setStyleSheet(
            """QScrollArea#scroll {background-color: white;}
            """
        )

        # setup button_bar
        self._button_bar = self.createButtonBar()

        # setup layout
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self._titleBar)
        self.layout.addWidget(self._scroll)
        self.setLayout(self.layout)

        shadow = QGraphicsDropShadowEffect()
        shadow.setOffset(0)
        shadow.setBlurRadius(50)
        self.setGraphicsEffect(shadow)
        self.adjustSize()

        self.setData(self.default_data)

    def center(self, parent):
        """Centers dialog on parent widget.

        Args:
            parent (QWidget)
        """
        parent_pos = parent.mapToGlobal(parent.window().rect().center())
        x = parent_pos.x() - self.width() / 2
        y = parent_pos.y() - self.height() / 2
        self.move(x, y)

    def createButtonBar(self):
        button_bar = QDialogButtonBox()
        return button_bar

    def createButtons(self):
        """Creates dialog buttons

        Returns
            buttons ({name:QPushbutton}): dictionary containing dialog buttons
        """
        default_buttons = {
                'Submit': self.validate,
                'Reset': self.reset,
                'Cancel': self.reject
            }
        buttons = {}
        for name, action in default_buttons.items():
            button = QPushButton(name)
            button.clicked.connect(action)
            buttons[name] = button
        return buttons

    def createEditors(self):
        """Creates dialog input widgets.
           Override base class for specific forms"""
        editors = {}
        return editors

    def data(self):
        """Convenience method returning dialog editor display values.

        Returns:
            data ({name: value}): dict containing dialog widgets display values
                                  keys match self.editors
        """
        data = {}
        for name, editor in self.editors.items():
            data[name] = editor.value()

        return data

    def errorMessage(self, error):
        popup = QMessageBox(QMessageBox.Critical, 'Error', error,
                            QMessageBox.Ok, self)
        popup.exec_()

    def isReadOnly(self):
        return False

    def reset(self):
        """Resets dialog widgets display values to default values"""
        self.setData(data=self.default_data)

    def reject(self):
        super().reject()
        self.mainWindow.active_dialogs.remove(self)

    def validate(self):
        data = self.data()
        #############################
        error = self.validationTest(data=data)
        #############################

        if error is None:
            self.accept()
            self.mainWindow.active_dialogs.remove(self)
        else:
            self.errorMessage(error)
            return

    def setData(self, data):
        """Convenience method setting dialog editor display values
           to data values.

        Args:
            data ({name: value}): dict containing dialog widgets display values
        """
        for name, editor in self.editors.items():
            if name in data:
                editor.setValue(data[name])

    def updateEditorModels(self):
        """Updates dialog editor models"""
        try:
            self.editors
        except NameError:
            return

        if self.editors:
            for name, editor in self.editors.items():
                if isinstance(editor, FilteringComboBox):
                    editor.updateModel()
