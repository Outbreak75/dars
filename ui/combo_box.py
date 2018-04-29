from PyQt5.QtWidgets import QComboBox, QCompleter
from PyQt5.QtCore import Qt, QSortFilterProxyModel, pyqtSlot
from PyQt5.QtSql import QSqlTableModel


class FilteringComboBox(QComboBox):
    """Combination of QCombobox and QLineEdit with autocompletionself.
    Line edit and completer model is taken from QSqlTable mod

    Args:
        table (str): db table name containing data for combobox
        column (str): column name containing data for combobox
    """
    def __init__(self, table, column, placeholderText, parent=None):
        super(FilteringComboBox, self).__init__(parent)
        self.parent = parent
        self.setEditable(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setInsertPolicy(QComboBox.NoInsert)
        self.lineEdit().setPlaceholderText(placeholderText)

        # setup data model
        self._model = QSqlTableModel(self)
        self._model.setTable(table)
        self._model.select()
        col_num = self._model.fieldIndex(column)
        self._model.sort(col_num, Qt.AscendingOrder)
        self.setModel(self._model)
        self.setModelColumn(col_num)

        # setup completer
        self._proxy = QSortFilterProxyModel(self)
        self._proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self._proxy.setSourceModel(self._model)
        self._proxy.setFilterKeyColumn(col_num)

        self._completer = QCompleter(self)
        self._completer.setModel(self._proxy)
        self._completer.setCompletionColumn(col_num)
        self._completer.activated.connect(self.onCompleterActivated)
        self._completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self._completer)
        self.lineEdit().textEdited.connect(self._proxy.setFilterFixedString)

    @pyqtSlot(str)
    def onCompleterActivated(self, text):
        if not text:
            return

        self.setCurrentIndex(self.findText(text))
        self.activated[str].emit(self.currentText())

    def updateModel(self):
        self._model.select()
