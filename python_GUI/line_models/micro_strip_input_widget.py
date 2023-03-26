from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtGui import QPalette, QColor, QFont
from PySide6.QtWidgets import QGridLayout, QLabel

from python_gui.utills.setting_gui import GUI_setting
from python_gui.utills.utills_gui import unit_cell_length, central_line_width, D0, BASE_COLOR
from python_gui.widgets.floquet_line_dimensions_input_widget import WidgetFLineDimensionsInputs
from python_gui.widgets.frequency_range_input_widget import WidgetFrequencyInputs
from python_gui.widgets.gain_input_widget import WidgetGainInputs
from python_gui.widgets.super_conductor_input_widget import WidgetSCInputs
from simulation.utills.constants import MICRO_STRIP_TYPE


class MicroStripInputsWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(MicroStripInputsWidget, self).__init__(*args, **kwargs)
        self.type = MICRO_STRIP_TYPE

        self.setLayout(QGridLayout())

        self.title = QLabel("")
        self.title.setMaximumHeight(40)
        self.title.setFont(QFont('Arial', 28))
        self.layout().addWidget(self.title)

        # ---------------------------------- inputs_containters MS

        self.super_conductor_inputs = WidgetSCInputs()
        self.layout().addWidget(self.super_conductor_inputs, 2, 0, 1, 2)
        self.dimensions_inputs = WidgetFLineDimensionsInputs(["Line Length [μm]", "Line Width [μm]"],[])
        imgPath = "images/micro_strip_diagram_img.png"

        pixmap = QtGui.QPixmap(imgPath)
        pixmap = pixmap.scaled(800, 400, QtCore.Qt.KeepAspectRatio)
        picture = QLabel(self)
        picture.setPixmap(pixmap)
        picture.setScaledContents(True)

        self.layout().addWidget(picture, 5, 0, 1, 1)

        self.layout().addWidget(self.dimensions_inputs, 3, 1, 2, 1)
        self.freq_range_inputs = WidgetFrequencyInputs()
        self.layout().addWidget(self.freq_range_inputs, 4, 0)
        self.gain_inputs = WidgetGainInputs()
        self.layout().addWidget(self.gain_inputs, 3, 0)

        # set widget color
        self.setBackGroundColor(BASE_COLOR)
        self.layout().setSpacing(5)

    def setBackGroundColor(self, hex_color: str):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(hex_color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def set_setting(self, setting: GUI_setting):
        self.title.setText(f"Current setting: {setting.name}")

    def get_inputs(self):
        return {
            "super_conductor_properties": self.super_conductor_inputs.getValues(),
            "line_dimensions": self.dimensions_inputs.getValues(),
            "frequency_range": self.freq_range_inputs.getValues(),
            "gain_properties": self.gain_inputs.getValues()
        }

    def set_values(self, inputs: dict):
        self.super_conductor_inputs.setValues(inputs.get("super_conductor_properties"))
        self.dimensions_inputs.setValues(inputs.get("line_dimensions"))
        self.freq_range_inputs.setValues(inputs.get("frequency_range"))
        self.gain_inputs.setValues(inputs.get("gain_properties"))
