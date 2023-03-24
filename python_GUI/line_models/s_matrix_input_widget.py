from PySide6 import QtWidgets
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QGridLayout, QPushButton, QLabel, QFileDialog

from python_gui.utills.setting_gui import GUI_setting
from python_gui.utills.utills_gui import randomColorBright
from python_gui.widgets.float_input_widget import WidgetDoubleInput
from python_gui.widgets.gain_input_widget import WidgetGainInputs


class SMatrixInputsWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(SMatrixInputsWidget, self).__init__(*args, **kwargs)

        self.type = "HFSS_TOUCHSTONE_FILE"

        self.setLayout(QGridLayout())

        # ---------------------------------- inputs_containters MS

        self.layout().addWidget(QLabel("input a file"))

        self.file_choose_button = QPushButton('Choose a File')
        self.file_choose_button.clicked.connect(self.selectFile)
        self.layout().addWidget(self.file_choose_button, 0, 1)

        self.n_interp_points = WidgetDoubleInput("Number of interpolation points", MinVal=0, DefaultVal=1000)
        self.layout().addWidget(self.n_interp_points, 0, 2)

        self.file_name_display = QLabel("")
        self.layout().addWidget(self.file_name_display, 2, 0, 2, 1)

        self.unit_cell_length = WidgetDoubleInput("unit cell length [meters]", MinVal=0)
        self.layout().addWidget(self.unit_cell_length, 1, 3)

        self.n_repeated_cells = WidgetDoubleInput("N cells [Gain | Transmission]", MinVal=1)
        self.layout().addWidget(self.n_repeated_cells, 0, 3)

        self.WidgetGainInputs = WidgetGainInputs()
        self.layout().addWidget(self.WidgetGainInputs, 4, 0)

        self.title = QLabel("")
        self.layout().addWidget(self.WidgetGainInputs, 5, 0)

        # set widget color
        self.setBackGroundColor(randomColorBright())
        # self.setMaximumHeight(100)

        self.file_path = ''

    def selectFile(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        self.file_path = dialog.getOpenFileName(self, 'Find file')[0]

        self.file_name_display.setText(f"File selected: {self.file_path}")

    def get_inputs(self):
        return {
            "hfss_touchstone_file_path": self.file_path,
            "unit_cell_length": self.unit_cell_length.get_value(),
            "n_interpt_points": self.n_interp_points.get_value(),
            "n_repeated_cells": self.n_repeated_cells.get_value(),
            "gain_models": self.WidgetGainInputs.getValues()
        }

    def set_setting(self, setting: GUI_setting):
        self.title.setText(f"Current setting: {setting.name}")

    def set_values(self, input: dict):
        self.file_path = input["hfss_touchstone_file_path"]
        file_path = input["hfss_touchstone_file_path"]
        self.file_name_display.setText(f"File selected: {file_path}")
        self.n_interp_points.setValue(int(input.get("n_interpt_points", 1000)))
        self.unit_cell_length.setValue(float(input.get("unit_cell_length", 0)))
        self.n_repeated_cells.setValue(int(input.get("n_repeated_cells", 1)))
        self.WidgetGainInputs.setValues(input.get("gain_models", []))

    def setBackGroundColor(self, hex_color: str):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(hex_color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
