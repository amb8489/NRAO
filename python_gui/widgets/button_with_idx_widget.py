from PySide6 import QtWidgets
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QVBoxLayout, QPushButton


# todo set names for each input to the names of the dict
class idxButton(QtWidgets.QWidget):
    def __init__(self, text, idx, onClick=None, onClickArgs=None, widget_name=None, *args, **kwargs):
        super(idxButton, self).__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())

        if widget_name:
            self.setObjectName(widget_name)

        self.load_button = QPushButton(text, self)
        self.idx = idx

        self.onClickArgs = onClickArgs

        if onClick:
            self.load_button.clicked.connect(lambda: onClick(self.onClickArgs) if self.onClickArgs else onClick())

        self.layout().addWidget(self.load_button)

        self.setBackGroundColor("#a89b74")

    def setBackGroundColor(self, hex_color: str):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(hex_color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def DownShiftIdx(self):

        self.onClickArgs[2] -= 1
        self.onClickArgs[1] -= 1
        return [self.onClickArgs[2], self.onClickArgs[1]]
