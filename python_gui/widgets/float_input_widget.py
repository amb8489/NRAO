import matplotlib
from PySide6.QtGui import QPalette, QColor, QFont

matplotlib.use('Qt5Agg')
from PySide6.QtWidgets import QLabel, QDoubleSpinBox, QVBoxLayout
from PySide6 import QtWidgets


# todo set names for each input to the names of the dict
class WidgetDoubleInput(QtWidgets.QWidget):
    def __init__(self, Title, MaxVal=10 ** 5, MinVal=0, DefaultVal=0, onchange=None, widget_name=None, *args, **kwargs):
        super(WidgetDoubleInput, self).__init__(*args, **kwargs)

        self.setObjectName(widget_name if widget_name else Title)
        self.setLayout(QVBoxLayout())
        self.Title = Title
        self.label = QLabel(Title)
        self.label.setFont(QFont('Arial', 14))

        self.input = QDoubleSpinBox()

        self.input.setMinimum(MinVal)
        self.input.setMaximum(MaxVal)
        self.input.setDecimals(6)

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
            print("error setting val in float inputs")