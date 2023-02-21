import matplotlib
from PySide6.QtGui import QPalette, QColor, Qt, QFont

from python_gui.utills.utills_gui import DIMS_WIDGET_COLOR
from python_gui.widgets.table_input_widget import TableInputWidget

matplotlib.use('Qt5Agg')
from PySide6.QtWidgets import QGridLayout, QLabel, QVBoxLayout
from PySide6 import QtWidgets


class WidgetCPWARTDimensionsInputs(QtWidgets.QWidget):

    def __init__(self, column_names, input_names, row_name="Load", *args, **kwargs):
        super(WidgetCPWARTDimensionsInputs, self).__init__(*args, **kwargs)

        self.HideLine = False

        # main layout
        self.setLayout(QGridLayout())

        # component title

        self.title = QLabel("Unit Cell Dimensions")
        self.title.setFont(QFont('Arial', 16))
        self.layout().addWidget(self.title, 0, 0)

        # materials_table for load widths and lengths inputs
        self.tableInput = TableInputWidget(column_names, onChange=self.update_line_data, row_name=row_name)

        self.layout().addWidget(self.tableInput, 0, 0, 3, 2, Qt.AlignTop)

        # input widgets for UC length and Line Width
        self.container = QVBoxLayout()
        self.inputnames = input_names
        self.inputs = []

        self.displays = []

        self.tableInput.getData()
        for i, row in enumerate(self.tableInput.getData()):
            Lu = row[1] * 2 + row[3] + row[5]
            line_len = Lu * row[0]
            display_widget = QLabel(f"Line {i + 1} length: {line_len} -- Lu: {Lu}")

            x = i % 2
            y = i // 2
            self.layout().addWidget(display_widget, y + 2, x)
            self.displays.append(display_widget)

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
        values = {f"loads": self.tableInput.getData()}
        for input in self.inputs:
            values[input.getTitleAndValue()[0]] = input.getTitleAndValue()[1]

        return values

    def update_line_data(self):

        for display in self.displays:
            display.deleteLater()
        self.displays = []

        for i, row in enumerate(self.tableInput.getData()):
            Lu = float(row[1]) * 2 + float(row[3]) + float(row[5])
            line_len = Lu * float(row[0])
            display_widget = QLabel(f"Line {i + 1} length: {line_len} -- Lu: {Lu}")

            x = i % 2
            y = i // 2
            self.layout().addWidget(display_widget, 2 + y, x)
            self.displays.append(display_widget)

    def get_central_line_width(self):
        return self.inputs[1].get_value()

    def setValues(self, inputs):
        loads = inputs['loads']

        self.tableInput.setData(loads)

        for i, input in enumerate(self.inputs):
            input.setValue(inputs[input.objectName()])
