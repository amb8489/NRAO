import matplotlib
from PySide6 import QtGui, QtWidgets
from PySide6.QtGui import QPalette, QColor, QPixmap, QImage, Qt

from Inputs.MicroStripInputs import MicroStripInputs
from Utills.Functions import micro_meters_to_meters, nano_meters_to_meters
from python_GUI.plotData import simulate
from python_GUI.Widgets.FloquetLineDimensionsInputWidget import WidgetFLineDimensionsInputs, Line
from python_GUI.Widgets.FrequencyRangeInputWidget import WidgetFrequencyInputs
from python_GUI.Widgets.GainInputWidget import WidgetGainInputs
from python_GUI.Widgets.MaterialSelectorWidget import WidgetMaterialsSelect
from python_GUI.Widgets.PlotWidget import WidgetGraph
from python_GUI.Widgets.SuperConductorInputWidget import WidgetSCInputs

matplotlib.use('Qt5Agg')
from PySide6.QtWidgets import QMainWindow, QApplication, QGridLayout, QScrollArea, QLabel
import sys
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget


# TODO:
# [] make material selector change values in SC inputs
# [] put real labels and units for different input widgets
# [] for dim input widget make input for how many loads and load widths ect
# [] show hide button for material selector
# [] make window popup that draws the FL
# [] dynamic input for load widths and hights based on the number of loads
# {} connect input data to sim
# {} updates plots on plot button press
# [] other missed things
# {} style


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.showWidget = False
        self.showMaterialsWidget = False
        self.scroll = QScrollArea()
        self.ROOT = QWidget()
        self.Mainlayout = QVBoxLayout()
        self.plotWindow = None  # No external window yet.

        # ----------------------------------EXIT and Plots buttons

        self.ButtonLayout = QGridLayout()
        self.ButtonLayoutWidget = QWidget()

        self.button_exit = QPushButton('Exit')
        self.ButtonLayout.addWidget(self.button_exit, 0, 0)

        self.button_plot = QPushButton("Plot")
        self.ButtonLayout.addWidget(self.button_plot, 0, 1)

        self.button_choose_model = QPushButton('Select New Model')
        self.ButtonLayout.addWidget(self.button_choose_model, 0, 2)

        # buttons onPress
        self.button_plot.clicked.connect(self.show_new_window)
        self.button_exit.clicked.connect(lambda: exit(0))

        self.ButtonLayoutWidget.setLayout(self.ButtonLayout)
        self.Mainlayout.addWidget(self.ButtonLayoutWidget)

        # ---------------------------------- material selector

        self.title = QLabel('Micro Strip model')
        self.Mainlayout.addWidget(self.title)

        self.SCW = WidgetSCInputs()
        self.table = WidgetMaterialsSelect(onchange=self.SCW.setValues)
        self.Mainlayout.addWidget(self.table)

        # ---------------------------------- Inputs
        self.InputGrid = QGridLayout()
        self.InputGridWidget = QWidget()

        self.InputGrid.addWidget(self.SCW, 0, 0, 1, 2)
        self.dimensionsInputWidget = WidgetFLineDimensionsInputs()
        self.InputGrid.addWidget(self.dimensionsInputWidget, 1, 1, 2, 1)
        self.freqRangeWidget = WidgetFrequencyInputs()
        self.InputGrid.addWidget(self.freqRangeWidget, 1, 0)
        self.WidgetGainInputs = WidgetGainInputs()
        self.InputGrid.addWidget(self.WidgetGainInputs, 2, 0)
        self.InputGridWidget.setLayout(self.InputGrid)
        self.Mainlayout.addWidget(self.InputGridWidget)

        line = Line(self.dimensionsInputWidget.tableInput)
        self.Mainlayout.addWidget(line)
        self.init()

    def init(self):

        self.model_type = "MS"
        self.inputs = None
        if self.model_type == "MS":
            self.inputs = MicroStripInputs()
        else:
            print(f"model_type {self.model_type} is not supported")
            exit(1)

        self.setWindowTitle("TKIPA DESIGN TOOL")
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#AAAAAA"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        self.ROOT.setLayout(self.Mainlayout)
        self.scroll.setWidget(self.ROOT)

        self.setCentralWidget(self.scroll)

        self.setFixedWidth(1050)
        self.setFixedHeight(800)
        self.show()

    def hideMaterialsList(self):
        self.showMaterialsWidget = not self.showMaterialsWidget
        self.table.show() if self.showMaterialsWidget else self.table.hide()

    def srow(self):
        print(self.table.getFirstSelectedRow())

    def get_inputs(self):

        widgets = [self.WidgetGainInputs, self.freqRangeWidget, self.SCW, self.dimensionsInputWidget]

        for widget in widgets:
            print(widget.getTableValues())

    def show_new_window(self, checked):

        if self.plotWindow:
            self.plotWindow.clearPlots()
            self.plotWindow.plot()
        else:
            self.plotWindow = AnotherWindow(self.model_type, self.inputs)

        self.plotWindow.show()


class AnotherWindow(QScrollArea):
    """
    This "window" is alpha_plt QWidget. If it has no parent, it
    will appear as alpha_plt free-floating window as we want.
    """

    def __init__(self, model_type, inputs):
        super().__init__()

        self.setWindowTitle("PLOTS")
        self.grid = QGridLayout()
        self.vbox = QVBoxLayout()
        self.inputs = inputs
        self.model_type = model_type
        holder = QWidget()
        holder.setLayout(self.grid)
        self.setWidgetResizable(True)

        graphData = simulate(self.model_type, self.inputs)

        idx = 0
        for i in range(2):
            for j in range(3):
                self.grid.addWidget(WidgetGraph(f"{0}-{0}", graphData[0], graphData[idx]), j, i + 1)
                idx += 1




        self.vbox.addWidget(holder)
        self.setWidget(holder)
        self.setMinimumWidth(900)
        self.setMinimumHeight(700)

    def plot(self):

        # time.sleep(10)

        self.ButtonExit = QPushButton('Close window')
        self.grid.addWidget(self.ButtonExit, 0, 0)
        self.ButtonExit.clicked.connect(lambda: self.close())

        graphData = simulate(self.model_type, self.inputs)
        idx = 0
        for i in range(2):
            for j in range(3):
                self.grid.addWidget(WidgetGraph(f"{0}-{0}", graphData[0], graphData[idx]), j, i + 1)
                idx += 1

    def clearPlots(self):
        for i in range(self.grid.count()):
            child = self.grid.itemAt(i).widget()
            if child:
                child.deleteLater()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec()
