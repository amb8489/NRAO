import matplotlib
from PySide6.QtGui import QPalette, QColor
matplotlib.use('Qt5Agg')
from PySide6.QtWidgets import QLabel,QDoubleSpinBox, QVBoxLayout
from PySide6 import QtWidgets


class WidgetDoubleInput(QtWidgets.QWidget):
    def __init__(self, Title, MinVal=None, DefaultVal=0, onchange=None, *args, **kwargs):
        super(WidgetDoubleInput, self).__init__(*args, **kwargs)


        self.setLayout(QVBoxLayout())
        self.Title = Title
        self.label = QLabel(Title)
        self.input = QDoubleSpinBox()

        if MinVal:
            self.input.setMinimum(MinVal)
        self.input.setValue(DefaultVal)

        if onchange:
            self.input.valueChanged.connect(onchange)

        self.layout().addWidget(self.label)
        self.layout().addWidget(self.input)



        self.setBackGroundColor("#a89b74")

    def setBackGroundColor(self, hex_color: str):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(hex_color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def getTitleAndValue(self):
        return [self.Title, self.input.value()]

    def getInputWidget(self):
        return self.input

    def setValue(self, val):
        try:
            self.input.setValue(float(val))
        except:
            print("errot setting val in float inputs")
            pass
