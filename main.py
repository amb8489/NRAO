import sys

from PySide6.QtWidgets import QApplication

from python_GUI.Widgets.Main_Window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec()
