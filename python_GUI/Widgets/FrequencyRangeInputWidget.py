import matplotlib
from PySide6.QtGui import QPalette, QColor
from python_GUI.Widgets.FloatNLabelInputWidget import WidgetDoubleInput
matplotlib.use('Qt5Agg')
from PySide6.QtWidgets import QGridLayout, QLabel
from PySide6 import QtWidgets


class WidgetFrequencyInputs(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):

        super(WidgetFrequencyInputs, self).__init__(*args, **kwargs)

        self.setLayout(QGridLayout())



        # widget title
        self.Title = "Frequency"
        self.layout().addWidget(QLabel(self.Title), 0, 0)

        self.inputs = []

        # inputs for freq range and res
        self.inputnames = ["Start Freq [GHZ]", "End Freq [GHZ]", "resolution"]
        for j in range(len(self.inputnames)):
            input_widget = WidgetDoubleInput(self.inputnames[j])
            self.layout().addWidget(input_widget, 1, j)
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

        return res
