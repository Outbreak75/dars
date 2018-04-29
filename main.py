import sys
from PyQt5.QtWidgets import QApplication

from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.promptLogin()
    result = app.exec_()
    sys.exit(result)


if __name__ == '__main__':
    main()
