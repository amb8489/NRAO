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



        # inputs for freq range and res
        self.inputnames = ["Start Freq [GHZ]", "End Freq [GHZ]", "resolution"]
        for j in range(len(self.inputnames)):
            self.layout().addWidget(WidgetDoubleInput(self.inputnames[j]), 1, j)



        # set widget color
        self.setBackGroundColor("#057878")

    def setBackGroundColor(self, hex_color: str):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(hex_color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def getValues(self):
        res = []
        for child in self.children():
            try:
                res.append(child.getTitleAndValue())
            except:
                pass

        return res
