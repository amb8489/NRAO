import matplotlib
from PySide6.QtGui import QPalette, QColor, Qt, QFont

from python_gui.utills.utills_gui import pump_frequency, signal_amplitude, idler_amplitude, pump_amplitude
from python_gui.widgets.float_input_widget import WidgetDoubleInput

matplotlib.use('Qt5Agg')
from PySide6.QtWidgets import QGridLayout, QLabel
from PySide6 import QtWidgets


class WidgetGainInputs(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(WidgetGainInputs, self).__init__(*args, **kwargs)

        self.setLayout(QGridLayout())

        # title
        self.title = QLabel("Gain")
        self.title.setFont(QFont('Arial', 16))
        self.layout().addWidget(self.title, 0, 0)

        # inputs
        self.inputnames = [signal_amplitude, idler_amplitude, pump_amplitude, pump_frequency]
        self.inputs = []
        for j in range(len(self.inputnames)):
            input_widget = WidgetDoubleInput(self.inputnames[j].get_name(), unit_type=self.inputnames[j].get_unit())
            self.layout().addWidget(input_widget, 1, j, Qt.AlignTop)
            self.inputs.append(input_widget)

        # set widget color
        self.setBackGroundColor("#057878")

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
