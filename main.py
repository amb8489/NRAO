import random
import time

import matplotlib
import numpy as np
from PySide6.QtCore import QRect
from PySide6.QtGui import QPalette, QColor, QPainter, QPen, Qt, QBrush

from Server.runGraphs import mkGraphs
from Utills.Functions import microMeters_to_Meters, nanoMeters_to_Meters, toGHz
from python_GUI.plotData import simulate
from python_GUI.utillsGUI import randomColor
from python_GUI.Widgets.FloquetLineDimensionsInputWidget import WidgetFLineDimensionsInputs, Line
from python_GUI.Widgets.FrequencyRangeInputWidget import WidgetFrequencyInputs
from python_GUI.Widgets.GainInputWidget import WidgetGainInputs
from python_GUI.Widgets.MaterialSelectorWidget import TableModel, WidgetMaterialsSelect
from python_GUI.Widgets.PlotWidget import WidgetGraph
from python_GUI.Widgets.SuperConductorInputWidget import WidgetSCInputs

matplotlib.use('Qt5Agg')
from PySide6.QtWidgets import QMainWindow, QApplication, QGridLayout, QScrollArea, QHBoxLayout, QLabel, QFrame
import sys
from PySide6 import QtWidgets, QtGui, QtCore
import pandas as pd
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

        self.ButtonExit = QPushButton('Exit')
        self.ButtonLayout.addWidget(self.ButtonExit, 0, 0)

        self.PlotButton = QPushButton("Plot")
        self.ButtonLayout.addWidget(self.PlotButton, 0, 1)

        # buttons onPress
        self.PlotButton.clicked.connect(self.show_new_window)
        self.ButtonExit.clicked.connect(lambda: exit(0))

        self.ButtonLayoutWidget.setLayout(self.ButtonLayout)
        self.Mainlayout.addWidget(self.ButtonLayoutWidget)

        # ---------------------------------- material selector

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
        self.setWindowTitle("TKIPA SIMULATION")

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
            print(widget.getValues())

    def show_new_window(self, checked):

        if self.plotWindow:
            self.plotWindow.clearPlots()
            self.plotWindow.plot()
        else:
            self.plotWindow = AnotherWindow()

        self.plotWindow.show()


class AnotherWindow(QScrollArea):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PLOTS")
        self.grid = QGridLayout()
        self.vbox = QVBoxLayout()

        holder = QWidget()
        holder.setLayout(self.grid)
        self.setWidgetResizable(True)

        graphData = simulate()

        for i in range(3):
            for j in range(6):
                self.grid.addWidget(WidgetGraph(f"{0}-{0}", graphData["freqs"], graphData["alpha"]), j, i + 1)

        # self.plot()

        self.vbox.addWidget(holder)
        self.setWidget(holder)
        self.setMinimumWidth(900)
        self.setMinimumHeight(700)

        # ----------------

        unit_Cell_Len = microMeters_to_Meters(2300)
        width_unloaded = microMeters_to_Meters(1.49)
        width_loaded = width_unloaded * 1.2

        D0 = .0007666666666666666666
        D1 = 5e-5
        D2 = 5e-5
        D3 = .0001
        loads_Widths = [D1, D2, D3]

        # ---------------------------- SC inputs
        er = 10
        Height = nanoMeters_to_Meters(250)
        line_thickness = nanoMeters_to_Meters(60)
        Tc = 14.28
        T = 0
        pn = 1.008e-6
        tanD = 0
        Jc = 1
        # ------ END remove later in replacement of user input

    def plot(self):

        # time.sleep(10)

        self.ButtonExit = QPushButton('Close window')
        self.grid.addWidget(self.ButtonExit, 0, 0)
        self.ButtonExit.clicked.connect(lambda: self.close())
        graphData = simulate()

        for i in range(3):
            for j in range(6):
                self.grid.addWidget(WidgetGraph(f"{0}-{0}", graphData["freqs"], graphData["alpha"]), j, i + 1)

    def clearPlots(self):
        for i in range(self.grid.count()):
            child = self.grid.itemAt(i).widget()
            if child:
                child.deleteLater()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec()
