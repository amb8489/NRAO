import matplotlib
import numpy as np
from PySide6.QtGui import QPalette, QColor, Qt, QFont

from python_gui.utills.utills_gui import randomColorBright, GAIN_WIDGET_COLOR, DIMS_WIDGET_COLOR
from python_gui.widgets.float_input_widget import WidgetDoubleInput
from python_gui.widgets.table_input_widget import TableInputWidget

matplotlib.use('Qt5Agg')
from PySide6.QtWidgets import QGridLayout, QLabel, QVBoxLayout, QWidget, QScrollArea
from PySide6 import QtWidgets, QtCore


class WidgetFLineDimensionsInputs(QtWidgets.QWidget):

    def __init__(self, column_names, input_names,row_name = "Load", *args, **kwargs):
        super(WidgetFLineDimensionsInputs, self).__init__(*args, **kwargs)

        self.HideLine = False

        # main layout
        self.setLayout(QGridLayout())

        # component title

        self.title = QLabel("Unit Cell Dimensions")
        self.title.setFont(QFont('Arial', 16))
        self.layout().addWidget(self.title, 0, 0)

        # materials_table for load widths and lengths inputs
        self.tableInput = TableInputWidget(column_names,row_name=row_name)


        self.layout().addWidget(self.tableInput, 0, 0,2,2, Qt.AlignTop)


        # input widgets for UC length and Line Width
        self.container = QVBoxLayout()
        self.inputnames = input_names
        self.inputs = []

        for i in range(len(self.inputnames)):
            input_widget = WidgetDoubleInput(self.inputnames[i].get_name(), unit_type=self.inputnames[i].get_unit(),color=DIMS_WIDGET_COLOR)
            x = i % 2
            y = i // 2
            self.layout().addWidget(input_widget, 1+y,x)
            self.inputs.append(input_widget)



        # set widget color
        self.setBackGroundColor(DIMS_WIDGET_COLOR)

    def setBackGroundColor(self, hex_color: str):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(hex_color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def getLengths(self):
        return self.tableInput.getLengths()

    def getWidths(self):
        return self.tableInput.getWidths()

    def getValues(self):
        values = {f"lengths_widths": self.tableInput.getData()}
        for input in self.inputs:
            values[input.getTitleAndValue()[0]] = input.getTitleAndValue()[1]

        return values

    def get_central_line_width(self):
        return self.inputs[1].get_value()

    def setValues(self, inputs):
        loads = inputs['lengths_widths']

        self.tableInput.setData(loads)

        for i, input in enumerate(self.inputs):
            input.setValue(inputs[input.objectName()])
