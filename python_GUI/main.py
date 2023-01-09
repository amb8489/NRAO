import random

import matplotlib
import numpy as np
from PySide6.QtCore import QRect
from PySide6.QtGui import QPalette, QColor, QPainter, QPen, Qt, QBrush

from utillsGUI import randomColor
from Widgets.FloquetLineDimensionsInputWidget import WidgetFLineDimensionsInputs
from Widgets.FrequencyRangeInputWidget import WidgetFrequencyInputs
from Widgets.GainInputWidget import WidgetGainInputs
from Widgets.MaterialSelectorWidget import TableModel, WidgetMaterialsSelect
from Widgets.PlotWidget import WidgetGraph
from Widgets.SuperConductorInputWidget import WidgetSCInputs

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

        # top buttons
        self.ButtonLayout = QGridLayout()
        self.ButtonLayoutWidget = QWidget()
        ButtonPlot = QPushButton('Plot')
        self.ButtonLayout.addWidget(ButtonPlot, 0, 0)
        ButtonExit = QPushButton('exit')
        self.ButtonLayout.addWidget(ButtonExit, 0, 1)
        ButtonMaterials = QPushButton('Show/Hide Materials List')
        self.ButtonLayout.addWidget(ButtonMaterials, 0, 3)

        ButtonPlot.clicked.connect(self.get_inputs)
        ButtonExit.clicked.connect(lambda: exit(0))
        ButtonMaterials.clicked.connect(self.hideMaterialsList)

        self.ButtonLayoutWidget.setLayout(self.ButtonLayout)
        self.Mainlayout.addWidget(self.ButtonLayoutWidget)

        # material selector
        self.SCW = WidgetSCInputs()
        self.table = WidgetMaterialsSelect(onchange=self.SCW.setValues)

        self.Mainlayout.addWidget(self.table)

        # inputs
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

        # loadwidths = self.dimensions_input.getWidths()
        # loadheights = self.dimensions_input.getHeights()



        # graphs
        self.GraphLayout = QGridLayout()
        self.GraphLayoutWidget = QWidget()
        for i in range(3):
            for j in range(3):
                Xdata, Ydata = [i for i in range(20)], [random.randint(0, 1) for i in range(20)]

                self.GraphLayout.addWidget(WidgetGraph(f"{i}-{j}",Xdata, Ydata), i, j)
        self.GraphLayoutWidget.setLayout(self.GraphLayout)
        self.Mainlayout.addWidget(self.GraphLayoutWidget)

        self.init()

    def init(self):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#AAAAAA"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        self.ROOT.setLayout(self.Mainlayout)
        self.scroll.setWidget(self.ROOT)

        self.setCentralWidget(self.scroll)

        self.setFixedWidth(1400)
        self.setFixedHeight(800)
        self.show()

    def hideMaterialsList(self):
        self.showMaterialsWidget = not self.showMaterialsWidget
        self.table.show() if self.showMaterialsWidget else self.table.hide()

    def srow(self):
        print(self.table.getFirstSelectedRow())

    def get_inputs(self):

        widgets = [self.WidgetGainInputs,self.freqRangeWidget,self.SCW,self.dimensionsInputWidget]

        for widget in widgets:
            print(widget.getValues())

    def plot(self):

        for y in range(2):
            for x in range(2):


                Xdata, Ydata = [i for i in range(20)], [random.randint(0, 50) for i in range(20)]
                self.ROOT.addWidget(WidgetGraph(f"{x}-{y}",Xdata,Ydata), x, y + 1)
                # Just some button connected to 'plot' method




if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec()
