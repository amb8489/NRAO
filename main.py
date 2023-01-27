import sys

from PySide6.QtWidgets import QApplication

from python_gui.widgets.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec()
