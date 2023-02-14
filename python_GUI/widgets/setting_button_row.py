from PySide6 import QtWidgets
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QGridLayout, QLabel

from python_gui.utills.setting_gui import GUI_setting
from python_gui.widgets.delete_button import DeleteButton
from python_gui.widgets.load_button import LoadButton
from python_gui.widgets.update_button import UpdateButton


# todo set names for each input to the names of the dict
class Setting_Button_Row(QtWidgets.QWidget):
    def __init__(self, setting: GUI_setting, on_click_load_function, on_click_delete_function, on_click_update_function,
                 *args, **kwargs):
        super(Setting_Button_Row, self).__init__(*args, **kwargs)
        self.setLayout(QGridLayout())
        self.setting = setting

        # tile
        self.layout().addWidget(QLabel(f"{self.setting.name}"), 0, 0)

        # setting buttons
        self.layout().addWidget(LoadButton(setting, on_click_load_function), 0, 1)
        self.layout().addWidget(UpdateButton(setting, on_click_update_function), 0, 2)
        self.layout().addWidget(DeleteButton(setting, on_click_delete_function), 0, 3)

        self.setBackGroundColor("#FFFFFF")

    def setBackGroundColor(self, hex_color: str):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(hex_color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def DownShiftIdx(self):
        self.setting.setting_file_idx -= 1
        self.setting.setting_row_idx -= 1

    def set_idx(self, new_idx):
        self.idx = new_idx

        # todo set index in the two buttons ?

    def set_line_number(self, new_line_number):
        # todo set index in the two buttons ?

        self.line_number = new_line_number
