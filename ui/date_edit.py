from PyQt5.QtWidgets import QDateEdit


class DateEdit(QDateEdit):
    """docstring for [object Object]"""
    def __init__(self, minimumDate, placeholderText, parent=None):
        super(DateEdit, self).__init__(parent)
        self.parent = parent
        self.setMinimumDate(minimumDate)
        self.setSpecialValueText(placeholderText)
