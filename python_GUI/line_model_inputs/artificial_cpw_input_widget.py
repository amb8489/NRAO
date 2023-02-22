from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtGui import QPalette, QColor, QFont
from PySide6.QtWidgets import QGridLayout, QLabel

from python_gui.utills.setting_gui import GUI_setting
from python_gui.utills.utills_gui import ground_spacing, central_line_width, D0, unit_cell_length, BASE_COLOR
from python_gui.widgets.CPW_artifical_dimensions_input_widget import WidgetCPWARTDimensionsInputs
from python_gui.widgets.frequency_range_input_widget import WidgetFrequencyInputs
from python_gui.widgets.gain_input_widget import WidgetGainInputs
from python_gui.widgets.super_conductor_input_widget import WidgetSCInputs
from utills.constants import ARTIFICIAL_CPW


class ArtificialCPIInputsWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(ArtificialCPIInputsWidget, self).__init__(*args, **kwargs)
        self.type = ARTIFICIAL_CPW

        self.setLayout(QGridLayout())


        # settings title
        self.title = QLabel("")
        self.title.setMaximumHeight(40)
        self.title.setFont(QFont('Arial', 28))
        self.layout().addWidget(self.title)

        # ---------------------------------- model_inputs MS

        self.SCW = WidgetSCInputs()
        self.layout().addWidget(self.SCW, 2, 0, 1, 4)
        self.dimensionsInputWidget = WidgetCPWARTDimensionsInputs(
            ["N", "S [μm]", "WH [μm]", "LH [μm]", "WL [μm]", "LL [μm]"],
            [unit_cell_length, central_line_width, D0,
             ground_spacing], row_name="Line")
        self.layout().addWidget(self.dimensionsInputWidget, 3, 0, 3, 3)

        imgPath = "images/cpw_diagram_img.png"

        pixmap = QtGui.QPixmap(imgPath)
        pixmap = pixmap.scaled(800, 400, QtCore.Qt.KeepAspectRatio)
        picture = QLabel(self)
        picture.setPixmap(pixmap)
        picture.setScaledContents(True)

        self.layout().addWidget(picture, 6, 0, 3, 3)
        self.freqRangeWidget = WidgetFrequencyInputs()
        self.layout().addWidget(self.freqRangeWidget, 3, 3, 1, 1)
        self.WidgetGainInputs = WidgetGainInputs()
        self.layout().addWidget(self.WidgetGainInputs, 4, 3, 1, 1)
        self.layout().setSpacing(5)

        # set widget color
        self.setBackGroundColor(BASE_COLOR)

    def setBackGroundColor(self, hex_color: str):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(hex_color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def get_inputs(self):
        return {"SC": self.SCW.getValues(),
                "Dimensions": self.dimensionsInputWidget.getValues(),
                "Frequency Range": self.freqRangeWidget.getValues(),
                "gain_models": self.WidgetGainInputs.getValues()
                }

    def set_values(self, input: dict):
        self.SCW.setValues(input["SC"])
        self.dimensionsInputWidget.setValues(input["Dimensions"])
        self.freqRangeWidget.setValues(input["Frequency Range"])
        self.WidgetGainInputs.setValues(input["gain_models"])

    def set_setting(self, setting: GUI_setting):
        self.title.setText(f"Current setting: {setting.name}")

    def toggel_materials_table(self):
        if self.materials_table.isVisible():
            self.materials_table.hide()
            self.toggel_materials_table_button.setText("Show materials table")

        else:
            self.materials_table.show()
            self.toggel_materials_table_button.setText("Hide materials table")
