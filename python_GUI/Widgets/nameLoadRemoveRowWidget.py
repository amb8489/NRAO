from PySide6 import QtWidgets
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QGridLayout, QLabel

from python_GUI.Widgets.ButtonWithIdxWidget import idxButton


# todo set names for each input to the names of the dict
class Row(QtWidgets.QWidget):
    def __init__(self, text, idx, line_number, onClickLoad=None, onClickDelete=None, LoadArgs=None,
                 DeleteArgs=None, widget_name=None, *args, **kwargs):
        super(Row, self).__init__(*args, **kwargs)
        self.setLayout(QGridLayout())

        self.text = text
        self.idx = idx
        self.line_number = line_number
        self.DeleteArgs = DeleteArgs

        if widget_name:
            self.setObjectName(widget_name)

        self.layout().addWidget(QLabel(f"{text}"), 0, 0)

        self.loadButton = idxButton("Load", idx, onClick=onClickLoad, onClickArgs=LoadArgs)
        self.layout().addWidget(self.loadButton, 0, 1)

        self.deleteButton = idxButton("Delete", idx, onClick=onClickDelete, onClickArgs=self.DeleteArgs)
        self.layout().addWidget(self.deleteButton, 0, 2)

        self.setBackGroundColor("#FFFFFF")

    def setBackGroundColor(self, hex_color: str):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(hex_color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def DownShiftIdx(self):
        self.idx -= 1
        self.line_number -= 1

        return self.deleteButton.DownShiftIdx()

    def set_idx(self, new_idx):
        self.idx = new_idx

        # todo set index in the two buttons ?

    def set_line_number(self, new_line_number):
        # todo set index in the two buttons ?

        self.line_number = new_line_number
