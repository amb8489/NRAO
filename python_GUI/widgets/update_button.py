from PySide6 import QtWidgets
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QVBoxLayout, QPushButton


# todo set names for each input to the names of the dict
class UpdateButton(QtWidgets.QWidget):
    def __init__(self, setting, on_update_function, *args, **kwargs):
        super(UpdateButton, self).__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())

        self.load_button = QPushButton("UPDATE", self)

        self.setting = setting
        self.load_button.clicked.connect(lambda: on_update_function(setting.setting_row_idx))

        self.layout().addWidget(self.load_button)

        self.setBackGroundColor("#a89b74")

    def setBackGroundColor(self, hex_color: str):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(hex_color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

