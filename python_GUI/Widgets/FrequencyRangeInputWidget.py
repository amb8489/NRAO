import matplotlib
from PySide6.QtGui import QPalette, QColor
from python_GUI.Utils_GUI import randomColor
from python_GUI.Widgets.FloatNLabelInputWidget import WidgetDoubleInput
matplotlib.use('Qt5Agg')
from PySide6.QtWidgets import QGridLayout, QLabel
from PySide6 import QtWidgets


class WidgetFrequencyInputs(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):

        super(WidgetFrequencyInputs, self).__init__(*args, **kwargs)

        self.Title = "Frequency"
        self.inputnames = ["Start Freq [GHz]", "End Freq [GHz]", "Resolution"]

        self.setLayout(QGridLayout())
        self.layout().addWidget(QLabel(self.Title), 0, 0)

        for j in range(len(self.inputnames)):
            self.layout().addWidget(WidgetDoubleInput(self.inputnames[j]), 1, j)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#057878"))
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
