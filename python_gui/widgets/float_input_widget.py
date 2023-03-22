import matplotlib
from PySide6.QtGui import QPalette, QColor, QFont

matplotlib.use('Qt5Agg')
from PySide6.QtWidgets import QLabel, QDoubleSpinBox, QVBoxLayout
from PySide6 import QtWidgets


# todo set names for each input to the names of the dict
class WidgetDoubleInput(QtWidgets.QWidget):
    def __init__(self, Title, unit_type="", MaxVal=10 ** 10, MinVal=0, DefaultVal=0, onchange=None, widget_name=None,
                 color=None,Decimals = 5,inc_amt = 1,*args,
                 **kwargs):
        super(WidgetDoubleInput, self).__init__(*args, **kwargs)

        self.setObjectName(widget_name if widget_name else Title)
        self.setLayout(QVBoxLayout())
        self.Title = Title
        self.label = QLabel(Title + (f" [{unit_type}]" if unit_type else ""))
        self.label.setFont(QFont('Arial', 14))

        self.input = QDoubleSpinBox()
        self.input.setSingleStep(inc_amt)
        self.input.setMinimum(MinVal)
        self.input.setMaximum(MaxVal)
        self.input.setDecimals(Decimals)

        self.input.setValue(DefaultVal)

        if onchange:
            self.input.valueChanged.connect(onchange)

        self.layout().addWidget(self.label)
        self.layout().addWidget(self.input)
        self.setFixedHeight(70)
        # self.setFixedWidth(150)

        color = color if color else "#AAAAAA"
        self.setBackGroundColor(color)

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

    def set_title(self,title):
        self.label.setText(title)


    def setMinMaxRange(self,min,max):
        self.input.setMinimum(min)
        self.input.setMaximum(max)

    def get_value(self):
        return float(self.input.value())
