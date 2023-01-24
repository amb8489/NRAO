import matplotlib
from PySide6.QtGui import QPalette, QColor, Qt
from python_GUI.Widgets.FloatNLabelInputWidget import WidgetDoubleInput

matplotlib.use('Qt5Agg')
from PySide6.QtWidgets import QGridLayout, QLabel
from PySide6 import QtWidgets


class WidgetGainInputs(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(WidgetGainInputs, self).__init__(*args, **kwargs)

        self.setLayout(QGridLayout())

        # title
        self.Title = "Gain"
        self.layout().addWidget(QLabel(self.Title), 0, 0)

        # inputs
        self.inputnames = ["As0", "Ai0", "Ap0", "Pump Frequency [GHZ]"]
        self.inputs = []
        for j in range(len(self.inputnames)):
            input_widget = WidgetDoubleInput(self.inputnames[j])
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
