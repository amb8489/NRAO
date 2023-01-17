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
        for j in range(len(self.inputnames)):
            self.layout().addWidget(WidgetDoubleInput(self.inputnames[j]), 1, j, Qt.AlignTop)

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
