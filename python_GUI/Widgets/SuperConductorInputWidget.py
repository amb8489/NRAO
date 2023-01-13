import matplotlib
from PySide6.QtGui import QPalette, QColor
from python_GUI.Widgets.FloatNLabelInputWidget import WidgetDoubleInput
matplotlib.use('Qt5Agg')
from PySide6.QtWidgets import QGridLayout, QLabel
from PySide6 import QtWidgets


class WidgetSCInputs(QtWidgets.QWidget):

    def __init__(self,  *args, **kwargs):
        super(WidgetSCInputs, self).__init__(*args, **kwargs)


        self.Title = "Super Conductor"
        self.inputnames = ["er", "h", "ts", "tg", "t", "tc", "jc", "normal_resistivity", "tand"]


        self.setLayout(QGridLayout())
        self.layout().addWidget(QLabel(self.Title), 0, 0)


        self.inputs = []
        for j in range(len(self.inputnames)):
            input = WidgetDoubleInput(self.inputnames[j])
            self.layout().addWidget(input, 1, j)
            self.inputs.append(input)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#057878"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def setValues(self,values):
        for i,input in enumerate(self.inputs):
            input.setValue(values[i])

    def getValues(self):
        return [input.getTitleAndValue()[1] for input in self.inputs]

