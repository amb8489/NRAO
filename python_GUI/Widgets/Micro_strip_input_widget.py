from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QGridLayout, QWidget, QPushButton, QLabel

from python_GUI.Widgets.FloquetLineDimensionsInputWidget import Line, WidgetFLineDimensionsInputs
from python_GUI.Widgets.FrequencyRangeInputWidget import WidgetFrequencyInputs
from python_GUI.Widgets.GainInputWidget import WidgetGainInputs
from python_GUI.Widgets.MaterialSelectorWidget import WidgetMaterialsSelect
from python_GUI.Widgets.SuperConductorInputWidget import WidgetSCInputs
from python_GUI.utillsGUI import randomColorBright


class MicroStripInputsWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(MicroStripInputsWidget, self).__init__(*args, **kwargs)
        self.type = "MS"


        self.setLayout(QGridLayout())

        # self.table = WidgetMaterialsSelect(onchange=self.SCW.setValues)
        self.table = WidgetMaterialsSelect()

        self.layout().addWidget(self.table, 0, 0, 2, 2)
        # ---------------------------------- Inputs MS

        self.SCW = WidgetSCInputs()
        self.layout().addWidget(self.SCW, 2, 0, 1, 2)
        self.dimensionsInputWidget = WidgetFLineDimensionsInputs(["Lengths []","Widths []"])

        # todo make not absoulte path
        imgPath = "/Users/aaron/PycharmProjects/NRAO/python_GUI/images/MS_Diagram.png"

        actualImage = QtGui.QImage(imgPath)
        pixmap = QtGui.QPixmap(imgPath)
        pixmap = pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)

        lbl.setScaledContents(True)

        self.layout().addWidget(lbl, 5, 1, 1, 1)

        self.layout().addWidget(self.dimensionsInputWidget, 3, 1, 2, 1)
        self.freqRangeWidget = WidgetFrequencyInputs()
        self.layout().addWidget(self.freqRangeWidget, 3, 0)
        self.WidgetGainInputs = WidgetGainInputs()
        self.layout().addWidget(self.WidgetGainInputs, 4, 0)

        line = Line(self.dimensionsInputWidget.tableInput)
        self.layout().addWidget(line, 5, 0)

        self.table.onchange = self.SCW.setValues

        # set widget color
        self.setBackGroundColor(randomColorBright())

    def setBackGroundColor(self, hex_color: str):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(hex_color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def get_inputs(self):
        return {"SC": self.SCW.getValues(),
                "Dimensions": self.dimensionsInputWidget.getValues(),
                "Frequency Range": self.freqRangeWidget.getValues(),
                "Gain": self.WidgetGainInputs.getValues()
                }

    def set_values(self, input):

        self.SCW.setValues(input["SC"])
        self.dimensionsInputWidget.setValues(input["Dimensions"])
        self.freqRangeWidget.setValues(input["Frequency Range"])
        self.WidgetGainInputs.setValues(input["Gain"])
