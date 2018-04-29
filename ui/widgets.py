from PyQt5.QtWidgets import (QComboBox, QCompleter, QDateEdit, QLabel,
                             QVBoxLayout, QWidget, QLineEdit, QPlainTextEdit,
                             QPushButton, QHBoxLayout, QGridLayout, QSpacerItem)
from PyQt5.QtCore import Qt, QSortFilterProxyModel, pyqtSlot, QDate, QPoint
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtGui import QPalette, QColor, QPixmap
from config import DROPDOWN_PNG


class DialogTitleBar(QWidget):
    """docstring for TitleBar"""
    def __init__(self, parent=None, title='', color='rgb(0,145,234)'):
        super().__init__(parent)
        self.title = title
        self.color = color
        self.parent = parent

        # Setup titlebar layout
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # title bar
        title = QLabel(self.title.upper())
        style = """
            QLabel {{
                color: white;
                min-height: 3em;
                background-color: {color};
                font: bold 20pt;
            }}""".format(color=self.color)
        title.setStyleSheet(style)
        title.setAlignment(Qt.AlignHCenter | Qt. AlignVCenter)
        layout.addWidget(title)

    # def mousePressEvent(self, event):
    #     self.oldPos = event.globalPos()
    #
    # def mouseMoveEvent(self, event):
    #     delta = QPoint(event.globalPos() - self.oldPos)
    #     pos = self.parent.pos()
    #     self.parent.move(pos.x() + delta.x(), pos.y() + delta.y())
    #     self.oldPos = event.globalPos()


class Widget(QWidget):
    """docstring for [object Object]"""
    def __init__(self, parent=None, placeholderText='', image='',
                 color='rgb(0,145,234)', toggle=False):
        self.placeholderText = placeholderText
        self.image = image
        self.color = color
        self.toggle = toggle
        super().__init__(parent)
        self.parent = parent

        if self.parent is not None:
            self.mainWindow = self.parent.mainWindow

        # default appearances
        self._editor_font_size = 14
        self._label_font_size = 11
        self._hyperlink_font_size = 12

        self._primary_color = self.color.replace('b(', 'ba(').\
            replace(')', ',1)')

        # setup editor
        self._editor = self.createEditor()

        # setup label
        self._label = self.createLabel()
        self._label.showLabel(True)

        # setup helper text label
        self._helper = self.createHelper()

        # setup loayout
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self._label)
        self.layout.addSpacing(10)
        self.layout.addWidget(self._editor)
        self.layout.addWidget(self._helper)
        self.setLayout(self.layout)

    def createEditor(self):
        """Returns editor widget"""
        editor = QWidget()
        return editor

    def createLabel(self):
        try:
            self._editor
        except NameError:
            self.createEditor()

        label = ImageTextLabel(text=self.placeholderText, image=self.image,
                               buddy=self._editor)
        style = """
            QLabel {{
                color: rgba(0,0,0,0.48);
                font: {label_font_size}pt;}}
            """.format(label_font_size=self._label_font_size)
        label.setStyleSheet(style)
        return label

    def createHelper(self):
        """Returns label displaying helper text.
           Base class returns empty QLabel
        """
        label = QLabel()
        return label

    def style(self):
        """Returns stylesheet for editor. Baseclass returns empty string

        Returns:
            style (str)
        """
        return ''

    @pyqtSlot(str)
    def onActivated(self, text):
        if not text and self.toggle:
            # placeholder text displayed and label is not visible
            self._label.showLabel(False)
        else:  # selected text is displayed and label is visible
            self._label.showLabel(True)


class ImageTextLabel(QWidget):
    """docstring for Label"""
    def __init__(self, parent=None, text='', image='', buddy=None):
        self.image = image
        self.text = text
        self.buddy = buddy
        super().__init__(parent)

        # Setup visible layout
        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().setParent(None)
                elif child.layout() is not None:
                    self.clearLayout(child.layout())

    def showLabel(self, visible):
        if visible:
            # clear layout
            self.clearLayout(self.layout)
            # create icon and title
            self.title = QLabel(self.text)
            if self.buddy is not None:
                self.title.setBuddy(self.buddy)
            if self.image:
                self.icon = QLabel()
                self.pixmap = QPixmap(self.image)
                self.icon.setPixmap(self.pixmap)
                self.icon.setAlignment(Qt.AlignLeft)
                self.title.setMinimumHeight(self.pixmap.height())
            self.title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.title.setStyleSheet("""margin-right: 10px;""")
            # add item and title to layout
            if self.image:
                self.layout.addWidget(self.icon)
            self.layout.addWidget(self.title)
            self.layout.addStretch()
        else:
            self.clearLayout(self.layout)


class PrimaryButton(QPushButton):
    """docstring for [object Object]"""
    def __init__(self, parent, font_size=16, color='rgb(0,145,234)'):
        super().__init__(parent)
        self.font_size = font_size
        self.color = color
        style = """
        QPushButton {{
            background-color: rgba(0,0,0,01);
            border: 0px;
            border-radius: 2px;
            color: {color};
            padding: 8px;
            margin-top: 24px;
            min-height: 1.2em;
            font: {font_size}pt;}}

        QPushButton:hover, QPushButton:hover:focus {{
            background-color: rgba(0,0,0,0.05);
        }}

        QPushButton:pressed,
        QPushButton:pressed:focus {{
            background-color: rgba(153,153,153,0.4);
        }}

        QPushButton:disabled {{
            color: lightGray;
            background-color: gray;
            border: none
        }}
        """.format(color=self.color, font_size=self.font_size)
        self.setStyleSheet(style)


class HyperlinkButton(QPushButton):
    """docstring for [object Object]"""
    def __init__(self, parent=None, font_size=12):
        super().__init__(parent)
        self.font_size = font_size
        self.setFlat(True)
        style = """
            QPushButton {{
                color: rgba(0,0,0,0.65);
                margin: 2px;
                border: 0px;
                padding: 0px;
                text-align: right;
                font: {font_size}pt;}}

            QPushButton:hover {{
                text-decoration: underline;
                color: rgba(0,0,0,0.65)}}

            QPushButton:pressed {{
                color: rgba(0,0,0,1);
                background-color: rgba(153,153,153,0.4)}}
        """.format(font_size=self.font_size)
        self.setStyleSheet(style)


class FilteringComboBox(Widget):
    """Combination of QCombobox and QLineEdit with autocompletionself.
    Line edit and completer model is taken from QSqlTable mod

    Parameters:
        table (str): db table name containing data for combobox
        column (str): column name containing data for combobox
        color (str): 'rgb(r, g, b)' used for primary color
        font_size (int): default text font size in pt
        _model (QSqlTableModel): data model
        _col (int): display data model source coulumn
        _proxy (QSortFilterProxyModel): completer data model.
                                        _proxy.sourceModel() == _model
        _le (QLineEdit): QCombobox LineEdit


    Methods:
        createEditor(): (Widget): returns user input widgets
        value(): (str): returns user input text value
        setValue(value(str)): sets editor widget display value
        style(): (str): Returns CSS stylesheet string for input widget
        updateModel(): updates input widget model

    Args:
        table (str): db table name containing data for combobox
        column (str): column name containing data for combobox
    """
    def __init__(self, parent, placeholderText, table, column,
                 color='rgb(0,145,234)', image=''):
        self.table = table
        self.column = column
        self.color = color
        super().__init__(parent, placeholderText, image)
        self.updateModel()

    def createEditor(self):
        # setup data model
        self._model = QSqlTableModel()
        self._model.setTable(self.table)
        self._col = self._model.fieldIndex(self.column)

        # setup filter model for sorting and filtering
        self._proxy = QSortFilterProxyModel()
        self._proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self._proxy.setSourceModel(self._model)
        self._proxy.setFilterKeyColumn(self._col)

        # setup completer
        self._completer = QCompleter()
        self._completer.setModel(self._proxy)
        self._completer.setCompletionColumn(self._col)
        self._completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)

        # setup combobox
        editor = QComboBox()
        editor.setModel(self._proxy)
        editor.setModelColumn(self._col)
        editor.setEditable(True)
        editor.setFocusPolicy(Qt.StrongFocus)
        editor.setInsertPolicy(QComboBox.NoInsert)
        editor.setCompleter(self._completer)

        # setup connections
        editor.currentTextChanged[str].connect(self.onActivated)

        # setup editor appearence
        style = self.style()
        editor.setStyleSheet(style)
        editor.lineEdit().setStyleSheet(style)
        font = editor.font()
        self._completer.popup().setFont(font)

        return editor

    @pyqtSlot(str)
    def onActivated(self, text):
        print('combo_box filter text', text)
        if not text:  # placeholder text displayed and label is not visible
            self._editor.setCurrentIndex(-1)
            if self.toggle:
                self._label.showLabel(False)
        else:  # selected text is displayed and label is visible
            # self._editor.showPopup()
            # self._editor.lineEdit().setFocus()
            print('current copmpletion string',
                  self._completer.currentCompletion())
            self._proxy.setFilterFixedString(text)
            if self.toggle:
                self._label.showLabel(True)

    def style(self):
        """Returns stylesheet for editors

        Returns:
            style (str)
        """
        style = """
            QLineEdit {{
                border: none;
                padding-bottom: 2px;
                border-bottom: 1px solid rgba(0,0,0,0.42);
                background-color: white;
                color: rgba(0,0,0,0.42);
                font-size: {font_size}pt;}}

            QLineEdit:editable {{
                padding-bottom: 2px;
                border-bottom: 1px rgba(0,0,0,0.42);
                color: rgba(0,0,0,0.42);}}

            QLineEdit:disabled {{
                border: none;
                padding-bottom: 2px;
                border-bottom: 1px rgba(0,0,0,0.42);
                color: rgba(0,0,0,0.38);}}

            QLineEdit:hover {{
                padding-bottom: 2px;
                border-bottom: 2px solid rgba(0,0,0,0.6);
                color: rgba(0,0,0,0.54);
                }}

            QLineEdit:focus {{
                padding-bottom: 2px;
                border-bottom: 2px solid {color};
                color: rgba(0,0,0,0.87);}}

            QLineEdit:pressed {{
                border-bottom: 2px {color};
                font: bold;
                color: rgba(0,0,0,0.87)}}

            QComboBox {{
                border: none;
                padding-bottom: 2px;
                font-size: {font_size}pt;
                }}

            QComboBox::down-arrow {{
                image: url('dropdown.png');
                background-color: white;
                border: 0px white;
                padding: 0px;
                margin: 0px;
                height:14px;
                width:14px;}}

            QComboBox::drop-down{{
                subcontrol-position: center right;
                border: 0px;
                margin: 0px;
            }}

            QComboBox QAbstractItemView {{
                font: {font_size};}}

        """.format(color=self.color, font_size=self._editor_font_size,
                   dropdown=DROPDOWN_PNG)
        return style

    def updateModel(self):
        model = self._editor.model().sourceModel()
        col = self._editor.modelColumn()
        model.select()
        model.sort(col, Qt.AscendingOrder)

    def value(self):
        return self._editor.currentText()

    def setValue(self, value):
        self._editor.setCurrentText(value)


class DateEdit(Widget):
    """docstring for [object Object]"""
    def __init__(self, parent, placeholderText, minimumDate, image=''):
        self.minimumDate = minimumDate
        super().__init__(parent, placeholderText, image)

    def createEditor(self):
        editor = QDateEdit()
        editor.setMinimumDate(self.minimumDate)
        # editor.setSpecialValueText(self.placeholderText)
        editor.setCalendarPopup(True)
        style = self.style()
        editor.setStyleSheet(style)
        # setup connections
        editor.dateChanged[QDate].connect(self.onActivated)

        return editor

    def value(self):
        return self._editor.date().toString(format=Qt.ISODate)

    def setValue(self, value):
        if value is None or value == '':
            self._editor.setMinimumDate(self._editor.minimumDate())
        else:
            self._editor.setDate(QDate.fromString(value, 'yyyy-MM-dd'))

    @pyqtSlot(QDate)
    def onActivated(self, date):
        if date.isNull() and self.toggle:
            # placeholder text displayed and label is invisible
            self._label.showLabel(False)
        else:  # selected text is displayed and label is visible
            self._label.showLabel(True)

    def style(self):
        """Returns stylesheet for editors

        Returns:
            style (str)
        """
        style = """
            QLineEdit {{
                border: none;
                padding-bottom: 2px;
                border-bottom: 1px solid rgba(0,0,0,0.42);
                background-color: white;
                color: rgba(0,0,0,0.42);
                font-size: {font_size}pt;}}

            QLineEdit:editable {{
                padding-bottom: 2px;
                border-bottom: 1px rgba(0,0,0,0.42);
                color: rgba(0,0,0,0.42);}}

            QLineEdit:disabled {{
                border: none;
                padding-bottom: 2px;
                border-bottom: 1px rgba(0,0,0,0.42);
                color: rgba(0,0,0,0.38);}}

            QLineEdit:hover {{
                padding-bottom: 2px;
                border-bottom: 2px solid rgba(0,0,0,0.6);
                color: rgba(0,0,0,0.54);
                }}

            QLineEdit:focus {{
                padding-bottom: 2px;
                border-bottom: 2px solid {color};
                color: rgba(0,0,0,0.87);}}

            QLineEdit:pressed {{
                border-bottom: 2px {color};
                font: bold;
                color: rgba(0,0,0,0.87)}}

            QDateEdit {{
                border: none;
                padding-bottom: 2px;
                font-size: {font_size}pt;
                }}

            QComboBox::down-arrow {{
                image: url('dropdown.png');
                background-color: white;
                border: 0px white;
                padding: 0px;
                margin: 0px;
                height:14px;
                width:14px;}}

            QComboBox::drop-down{{
                subcontrol-position: center right;
                border: 0px;
                margin: 0px;
            }}

            QComboBox QAbstractItemView {{
                font: {font_size};}}

        """.format(color=self.color, font_size=self._editor_font_size - 2,
                   dropdown=DROPDOWN_PNG)
        return style


class LineEdit(Widget):
    """docstring for [object Object]"""
    def __init__(self, parent, placeholderText, image=''):
        super().__init__(parent, placeholderText, image)

    def createEditor(self):
        editor = QLineEdit()
        # editor.setPlaceholderText(self.placeholderText)

        # setup connections
        editor.textEdited[str].connect(self.onActivated)

        style = self.style()
        editor.setStyleSheet(style)

        return editor

    def value(self):
        return self._editor.text()

    def setValue(self, value):
        self._editor.setText(value)

    def style(self):
        style = """
            QLineEdit {{
                border: none;
                padding-bottom: 2px;
                border-bottom: 1px solid rgba(0,0,0,0.42);
                background-color: white;
                color: rgba(0,0,0,0.42);
                font-size: {font_size}pt;}}

            QLineEdit:editable {{
                padding-bottom: 2px;
                border-bottom: 1px rgba(0,0,0,0.42);
                color: rgba(0,0,0,0.42);}}

            QLineEdit:disabled {{
                border: none;
                padding-bottom: 2px;
                border-bottom: 1px rgba(0,0,0,0.42);
                color: rgba(0,0,0,0.38);}}

            QLineEdit:hover {{
                padding-bottom: 2px;
                border-bottom: 2px solid rgba(0,0,0,0.6);
                color: rgba(0,0,0,0.54);
                }}

            QLineEdit:focus {{
                padding-bottom: 2px;
                border-bottom: 2px solid {color};
                color: rgba(0,0,0,0.87);}}

            QLineEdit:pressed {{
                border-bottom: 2px {color};
                font: bold;
                color: rgba(0,0,0,0.87)}}
        """.format(font_size=self._editor_font_size,
                   color=self._primary_color)
        return style

    @pyqtSlot(str)
    def onActivated(self, text):
        value = self.value()
        if not value:  # placeholder text displayed and label is not visible
            palette = self._editor.palette()
            palette.setColor(QPalette.Text, QColor(0, 0, 0, 0.5))
            self._editor.setPalette(palette)
            if self.toggle:
                self._label.showLabel(False)
        else:  # selected text is displayed and label is visible
            palette = self._editor.palette()
            palette.setColor(QPalette.Text, QColor(0, 0, 0, 0.87))
            self._editor.setPalette(palette)
            if self.toggle:
                self._label.showLabel(True)


class PlainTextEdit(Widget):
    """docstring for [object Object]"""
    def __init__(self, parent, placeholderText):
        super().__init__(parent, placeholderText)

    def createEditor(self):
        editor = QPlainTextEdit()
        # editor.setPlaceholderText(self.placeholderText)

        # setup connections
        editor.textChanged.connect(self.onActivated)

        return editor

    def value(self):
        return self._editor.toPlainText()

    def setValue(self, value):
        self._editor.document().setPlainText(value)

    @pyqtSlot()
    def onActivated(self):
        if not self._editor.toPlainText() and self.toggle:
            self._label.showLabel(False)
        else:  # selected text is displayed and label is visible
            self._label.showLabel(True)
