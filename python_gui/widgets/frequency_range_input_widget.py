import matplotlib
from PySide6.QtGui import QPalette, QColor, QFont

from python_gui.utills.utills_gui import start_frequency, end_frequency, resolution, FREQ_WIDGET_COLOR, n_repeated_cells
from python_gui.widgets.float_input_widget import WidgetDoubleInput

matplotlib.use('Qt5Agg')
from PySide6.QtWidgets import QGridLayout, QLabel
from PySide6 import QtWidgets


class WidgetFrequencyInputs(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(WidgetFrequencyInputs, self).__init__(*args, **kwargs)

        self.setLayout(QGridLayout())

        # widget title
        self.title = QLabel("Frequency Range")
        self.title.setFont(QFont('Arial', 16))
        self.layout().addWidget(self.title, 0, 0)

        # inputs for frequency range and res
        [start_frequency, end_frequency, resolution, n_repeated_cells]

        self.start_f = WidgetDoubleInput(start_frequency.get_name(), unit_type=start_frequency.get_unit(),
                                         color=FREQ_WIDGET_COLOR, MinVal=1, DefaultVal=1)
        self.layout().addWidget(self.start_f, 1, 0)

        self.end_f = WidgetDoubleInput(end_frequency.get_name(), unit_type=end_frequency.get_unit(),
                                       color=FREQ_WIDGET_COLOR, MinVal=1, DefaultVal=40)
        self.layout().addWidget(self.end_f, 1, 1)

        self.step_f = WidgetDoubleInput(resolution.get_name(), unit_type="GHz", color=FREQ_WIDGET_COLOR, MinVal=.000001,
                                        DefaultVal=.1)
        self.layout().addWidget(self.step_f, 2, 0)

        self.n_repeated_cells = WidgetDoubleInput(n_repeated_cells.get_name(), unit_type=n_repeated_cells.get_unit(),
                                                  color=FREQ_WIDGET_COLOR, Decimals=0, MinVal=1, DefaultVal=150)
        self.layout().addWidget(self.n_repeated_cells, 2, 1)

        self.inputs = [self.start_f, self.end_f, self.step_f, self.n_repeated_cells]

        # set widget color
        self.setBackGroundColor(FREQ_WIDGET_COLOR)

    def setBackGroundColor(self, hex_color: str):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(hex_color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def getValues(self):
        return {input.getTitleAndValue()[0]: input.getTitleAndValue()[1] for input in self.inputs}

    def setValues(self, values):
        for i, input in enumerate(self.inputs):
            input.setValue(values.get(input.objectName(), "0"))
