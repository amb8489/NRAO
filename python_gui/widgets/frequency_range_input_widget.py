import matplotlib
from PySide6.QtGui import QPalette, QColor, QFont

from python_gui.utills.utills_gui import start_frequency, end_frequency, resolution, FREQ_WIDGET_COLOR
from python_gui.widgets.float_input_widget import WidgetDoubleInput

matplotlib.use('Qt5Agg')
from PySide6.QtWidgets import QGridLayout, QLabel
from PySide6 import QtWidgets


class WidgetFrequencyInputs(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(WidgetFrequencyInputs, self).__init__(*args, **kwargs)

        self.setLayout(QGridLayout())

        # widget title
        self.title = QLabel("Frequency Range")
        self.title.setFont(QFont('Arial', 16))
        self.layout().addWidget(self.title, 0, 0)

        self.inputs = []

        # inputs for frequency range and res
        self.inputnames = [start_frequency,end_frequency,resolution]
        for j in range(len(self.inputnames)):
            input_widget = WidgetDoubleInput(self.inputnames[j].get_name(),unit_type=self.inputnames[j].get_unit(),color=FREQ_WIDGET_COLOR)
            self.layout().addWidget(input_widget, 1+(j//2), j%2)
            self.inputs.append(input_widget)

        # set widget color
        self.setBackGroundColor(FREQ_WIDGET_COLOR)

    def setBackGroundColor(self, hex_color: str):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(hex_color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def getValues(self):
        return {input.getTitleAndValue()[0]: input.getTitleAndValue()[1] for input in self.inputs}

    def setValues(self, values):
        for i, input in enumerate(self.inputs):
            input.setValue(values[input.objectName()])
