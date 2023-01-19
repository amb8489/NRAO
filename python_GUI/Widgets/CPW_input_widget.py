from PySide6 import QtWidgets
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QGridLayout, QWidget, QPushButton

from python_GUI.Widgets.FloquetLineDimensionsInputWidget import Line, WidgetFLineDimensionsInputs
from python_GUI.Widgets.FrequencyRangeInputWidget import WidgetFrequencyInputs
from python_GUI.Widgets.GainInputWidget import WidgetGainInputs
from python_GUI.Widgets.MaterialSelectorWidget import WidgetMaterialsSelect
from python_GUI.Widgets.SuperConductorInputWidget import WidgetSCInputs
from python_GUI.utillsGUI import randomColorBright


class CPWInputsWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(CPWInputsWidget, self).__init__(*args, **kwargs)

        self.setLayout(QGridLayout())

        # self.table = WidgetMaterialsSelect(onchange=self.SCW.setValues)
        self.table = WidgetMaterialsSelect()

        self.layout().addWidget(self.table, 0, 0, 2, 2)
        # ---------------------------------- Inputs MS

        self.SCW = WidgetSCInputs()
        self.layout().addWidget(self.SCW, 2, 0, 1, 2)
        self.dimensionsInputWidget = WidgetFLineDimensionsInputs()
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
