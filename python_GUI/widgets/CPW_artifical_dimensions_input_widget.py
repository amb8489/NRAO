import matplotlib
from PySide6.QtGui import QPalette, QColor, Qt, QFont

from python_gui.utills.unit import nameUnit
from python_gui.utills.utills_gui import DIMS_WIDGET_COLOR
from python_gui.widgets.float_input_widget import WidgetDoubleInput
from python_gui.widgets.table_input_widget import TableInputWidget

matplotlib.use('Qt5Agg')
from PySide6.QtWidgets import QGridLayout, QLabel, QVBoxLayout
from PySide6 import QtWidgets


class WidgetCPWARTDimensionsInputs(QtWidgets.QWidget):

    def __init__(self, column_names, input_names, row_name="Load", line_input_title="Number of Lines in Unit Cell",
                 *args, **kwargs):
        super(WidgetCPWARTDimensionsInputs, self).__init__(*args, **kwargs)

        self.HideLine = False

        # main layout
        self.setLayout(QGridLayout())

        # component title

        self.title = QLabel("Line Dimensions")
        self.title.setFont(QFont('Arial', 16))
        self.layout().addWidget(self.title, 0, 0)

        # todo isarttanle = True refacote out ? whats the difff now ?
        self.tableInput = TableInputWidget(column_names, row_name=row_name, height=200, title=line_input_title,
                                           isarttanle=True)

        self.layout().addWidget(self.tableInput, 0, 0, 3, 2, Qt.AlignTop)

        # input widgets for UC length and Line Width
        self.container = QVBoxLayout()
        self.inputs = []
        self.displays = []

        # set widget color
        self.setBackGroundColor(DIMS_WIDGET_COLOR)

    def setBackGroundColor(self, hex_color: str):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(hex_color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def getValues(self):
        values = {f"lengths_widths": self.tableInput.getData()}
        for input in self.inputs:
            values[input.getTitleAndValue()[0]] = input.getTitleAndValue()[1]

        return values

    def update_line_data(self):
        pass

    def get_central_line_width(self):
        return self.inputs[1].get_value()

    def setValues(self, inputs):
        lens_widths = inputs['lengths_widths']
        self.tableInput.setData(lens_widths)

        for i, input in enumerate(self.inputs):
            input.setValue(inputs[input.objectName()])
