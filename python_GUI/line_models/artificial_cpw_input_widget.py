from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtGui import QPalette, QColor, QFont
from PySide6.QtWidgets import QGridLayout, QLabel

from python_gui.utills.setting_gui import GUI_setting
from python_gui.utills.utills_gui import ground_spacing, central_line_width, D0, unit_cell_length, BASE_COLOR
from python_gui.widgets.CPW_artifical_dimensions_input_widget import WidgetCPWARTDimensionsInputs
from python_gui.widgets.float_input_widget import WidgetDoubleInput
from python_gui.widgets.frequency_range_input_widget import WidgetFrequencyInputs
from python_gui.widgets.gain_input_widget import WidgetGainInputs
from python_gui.widgets.super_conductor_input_widget import WidgetSCInputs
from simulation.utills.constants import ARTIFICIAL_CPW_TYPE


class ArtificialCPIInputsWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(ArtificialCPIInputsWidget, self).__init__(*args, **kwargs)
        self.type = ARTIFICIAL_CPW_TYPE

        self.setLayout(QGridLayout())

        # settings title
        self.title = QLabel("")
        self.title.setMaximumHeight(40)
        self.title.setFont(QFont('Arial', 28))
        self.layout().addWidget(self.title)
        self.layout().setSpacing(5)

        # ---------------------------------- inputs_containters MS

        self.super_conductor_inputs = WidgetSCInputs()
        self.layout().addWidget(self.super_conductor_inputs, 2, 0, 1, 4)

        # #todo refacir all to use the same type of table

        self.lu_S = WidgetDoubleInput("lu_S", unit_type="μm", MinVal=1, DefaultVal=1)
        self.lu_WH = WidgetDoubleInput("lu_WH", unit_type="μm", MinVal=1, DefaultVal=1)
        self.lu_LH = WidgetDoubleInput("lu_LH", unit_type="μm", MinVal=1, DefaultVal=1)
        self.lu_LL = WidgetDoubleInput("lu_LL", unit_type="μm", MinVal=1, DefaultVal=1)

        self.layout().addWidget(self.lu_S, 3, 0)
        self.layout().addWidget(self.lu_LH, 3, 1)
        self.layout().addWidget(self.lu_WH, 4, 0)
        self.layout().addWidget(self.lu_LL, 4, 1)

        self.lu_inputs = {inpt.getTitleAndValue()[0]: inpt.get_value() for inpt in
                          [self.lu_S, self.lu_LH, self.lu_WH, self.lu_LL]}

        self.line_dimensions_inputs = WidgetCPWARTDimensionsInputs(
            ["N repeated Lu segments", "Line width"],
            [], row_name="Line")
        self.layout().addWidget(self.line_dimensions_inputs, 5, 0, 2, 2)

        self.freq_range_inputs = WidgetFrequencyInputs()
        self.layout().addWidget(self.freq_range_inputs, 3, 2, 1, 2)
        self.gain_inputs = WidgetGainInputs()
        self.layout().addWidget(self.gain_inputs, 4, 2, 1, 2)

        imgPath = "images/Lu_diagram.png"
        pixmap = QtGui.QPixmap(imgPath)
        pixmap = pixmap.scaled(500, 500, QtCore.Qt.KeepAspectRatio)
        picture = QLabel(self)
        picture.setPixmap(pixmap)
        picture.setScaledContents(True)
        self.layout().addWidget(picture, 5, 2, 2, 2)

        # set widget color
        self.setBackGroundColor(BASE_COLOR)

    def setBackGroundColor(self, hex_color: str):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(hex_color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def set_values(self, inputs: dict):
        self.super_conductor_inputs.setValues(inputs.get("super_conductor_properties"))
        self.line_dimensions_inputs.setValues(inputs.get("line_dimensions"))
        self.freq_range_inputs.setValues(inputs.get("frequency_range"))
        self.gain_inputs.setValues(inputs.get("gain_properties"))

        for key, val in inputs.get("lu_dimensions", {}).items():
            self.lu_inputs[key].setValue(val)

    def get_inputs(self):
        return {"super_conductor_properties": self.super_conductor_inputs.getValues(),
                "line_dimensions": self.line_dimensions_inputs.getValues(),
                "lu_dimensions": {inpt.getTitleAndValue()[0]: inpt.get_value() for inpt in
                                  [self.lu_S, self.lu_LH, self.lu_WH, self.lu_LL]},
                "frequency_range": self.freq_range_inputs.getValues(),
                "gain_properties": self.gain_inputs.getValues(),
                }

    def set_setting(self, setting: GUI_setting):
        self.title.setText(f"Current setting: {setting.name}")
