import matplotlib
from PySide6.QtGui import QPalette, QColor, QFont, Qt

from python_gui.utills.utills_gui import Er, SC_thickness, SC_height, SC_ground_thickness, SC_critical_current, \
    SC_critical_temperature, SC_operation_temperature, SC_normal_resistivity, SC_tangent_delta, \
    SUPER_CONDUCTOR_WIDGET_COLOR
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
        self.input_unit_names = [Er, SC_height, SC_thickness, SC_ground_thickness, SC_operation_temperature,
                                 SC_critical_temperature, SC_critical_current, SC_normal_resistivity, SC_tangent_delta]
        self.inputs = []
        for j in range(len(self.input_unit_names)):
            input = WidgetDoubleInput(self.input_unit_names[j].get_name(),
                                      unit_type=self.input_unit_names[j].get_unit(),
                                      widget_name=self.input_unit_names[j].get_name(),color=SUPER_CONDUCTOR_WIDGET_COLOR)

            x = j % 3
            y = j // 3
            self.layout().addWidget(input, y + 1, x, Qt.AlignLeft)
            self.inputs.append(input)

        # set widget color
        self.setBackGroundColor(SUPER_CONDUCTOR_WIDGET_COLOR)
        self.layout().setSpacing(5)

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
