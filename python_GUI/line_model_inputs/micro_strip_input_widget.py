from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtGui import QPalette, QColor, QFont
from PySide6.QtWidgets import QGridLayout, QLabel

from python_gui.utills.setting_gui import GUI_setting
from python_gui.utills.utills_gui import unit_cell_length, central_line_width, D0, BASE_COLOR
from python_gui.widgets.floquet_line_dimensions_input_widget import WidgetFLineDimensionsInputs
from python_gui.widgets.frequency_range_input_widget import WidgetFrequencyInputs
from python_gui.widgets.gain_input_widget import WidgetGainInputs
from python_gui.widgets.super_conductor_input_widget import WidgetSCInputs
from utills.constants import MICRO_STRIP_TYPE


class MicroStripInputsWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(MicroStripInputsWidget, self).__init__(*args, **kwargs)
        self.type = MICRO_STRIP_TYPE

        self.setLayout(QGridLayout())

        # self.materials_table = WidgetMaterialsSelect()
        # self.layout().addWidget(self.materials_table, 0, 0, 2, 2)
        #
        # self.toggel_materials_table_button = QPushButton(text='Hide Materials List',
        #                                                  objectName='toggel_materials_table_button',
        #                                                  clicked=self.toggel_materials_table)
        # self.layout().addWidget(self.toggel_materials_table_button, 0, 1)

        self.title = QLabel("")
        self.title.setMaximumHeight(40)
        self.title.setFont(QFont('Arial', 28))
        self.layout().addWidget(self.title)

        # ---------------------------------- model_inputs MS

        self.SCW = WidgetSCInputs()
        self.layout().addWidget(self.SCW, 2, 0, 1, 2)
        self.dimensionsInputWidget = WidgetFLineDimensionsInputs(["D [μm]", "Widths [μm]"],
                                                                 [unit_cell_length, central_line_width, D0])
        imgPath = "images/micro_strip_diagram_img.png"

        pixmap = QtGui.QPixmap(imgPath)
        pixmap = pixmap.scaled(800, 400, QtCore.Qt.KeepAspectRatio)
        picture = QLabel(self)
        picture.setPixmap(pixmap)
        picture.setScaledContents(True)

        self.layout().addWidget(picture, 5, 0, 1, 1)

        self.layout().addWidget(self.dimensionsInputWidget, 3, 1, 2, 1)
        self.freqRangeWidget = WidgetFrequencyInputs()
        self.layout().addWidget(self.freqRangeWidget, 4, 0)
        self.WidgetGainInputs = WidgetGainInputs()
        self.layout().addWidget(self.WidgetGainInputs, 3, 0)

        # self.materials_table.onchange = self.SCW.setValues

        # set widget color
        self.setBackGroundColor(BASE_COLOR)
        self.layout().setSpacing(5)

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

    # def toggel_materials_table(self):
    #     if self.materials_table.isVisible():
    #         self.materials_table.hide()
    #         self.toggel_materials_table_button.setText("Show Materials Table")
    #
    #     else:
    #         self.materials_table.show()
    #         self.toggel_materials_table_button.setText("Hide Materials Table")

    def set_setting(self, setting: GUI_setting):
        self.title.setText(f"Current setting: {setting.name}")

    def set_values(self, input: dict):
        self.SCW.setValues(input["SC"])
        self.dimensionsInputWidget.setValues(input["Dimensions"])
        self.freqRangeWidget.setValues(input["Frequency Range"])
        self.WidgetGainInputs.setValues(input["gain_models"])
