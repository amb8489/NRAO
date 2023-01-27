import matplotlib
from PySide6.QtGui import QPalette, QColor, QFont

from python_gui.widgets.float_input_widget import WidgetDoubleInput

matplotlib.use('Qt5Agg')
from PySide6.QtWidgets import QGridLayout, QLabel
from PySide6 import QtWidgets


class WidgetSCInputs(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(WidgetSCInputs, self).__init__(*args, **kwargs)

        self.setLayout(QGridLayout())

        # title
        self.title = QLabel("Super Conductor")
        self.title.setFont(QFont('Arial', 16))
        self.layout().addWidget(self.title, 0, 0)

        # inputs
        self.inputnames = ["Er", "H", "Ts", "Tg", "T", "Tc", "Jc", "Normal Resistivity", "Tan D"]
        self.inputs = []
        for j in range(len(self.inputnames)):
            input = WidgetDoubleInput(self.inputnames[j], widget_name=self.inputnames[j])

            x = j % 3
            y = j // 3

            self.layout().addWidget(input, y + 1, x)
            self.inputs.append(input)

        # set widget color
        self.setBackGroundColor("#057878")

    def setBackGroundColor(self, hex_color: str):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(hex_color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def setValues(self, values):
        for i, input in enumerate(self.inputs):
            input.setValue(values[input.objectName()])

    def getValues(self):

        return {input.getTitleAndValue()[0]: input.getTitleAndValue()[1] for input in self.inputs}
