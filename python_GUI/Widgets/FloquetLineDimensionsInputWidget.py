import math

import matplotlib
import numpy as np
from PySide6.QtGui import QPalette, QColor, Qt
from python_GUI.utillsGUI import randomColor
from python_GUI.Widgets.FloatNLabelInputWidget import WidgetDoubleInput
from python_GUI.Widgets.TableInputWidget import TableInputWidget

matplotlib.use('Qt5Agg')
from PySide6.QtWidgets import QGridLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PySide6 import QtWidgets, QtCore


class Line(QtWidgets.QWidget):

    def __init__(self, table, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Widths = []
        self.Heights = []
        self.table = table

        self.table.setOnChange(self.updateLine)

        self.maxsize = 50
        # todo add in for central line
        self.centralLineW = 5

        self.HideLine = True
        self.setLayout(QGridLayout())
        self.layout().setHorizontalSpacing(0)

        # self.ButtonLineVeiwer = QPushButton('Hide/Show Line')
        # self.layout().addWidget(self.ButtonLineVeiwer, 0, 0, Qt.AlignTop)
        # self.ButtonLineVeiwer.clicked.connect(self.ToggleShowHide)

    def Draw(self):

        loadIdx = 0
        for i in range(len(self.Widths) * 2 + 1):
            if i % 2 == 0:

                r = bar(i, self.centralLineW, self.centralLineW)
                r.setMaximumHeight(self.centralLineW)
                self.layout().addWidget(r, 1, i)

            else:

                w = self.Widths[loadIdx]
                h = self.Heights[loadIdx]
                loadIdx += 1

                r = bar(i, w, h)
                r.setMaximumHeight(h)
                r.setMaximumWidth(w)
                self.layout().addWidget(QLabel(f"L{loadIdx}"), 0, i, Qt.AlignHCenter)
                self.layout().addWidget(r, 1, i, Qt.AlignHCenter)

    def ToggleShowHide(self):
        self.HideLine = not self.HideLine
        self.show() if self.HideLine else self.hide()

    def clearBars(self):
        for i in range(self.layout().count()):
            child = self.layout().itemAt(i).widget()
            if child:
                child.deleteLater()

    def updateLine(self):
        self.clearBars()
        self.setHeights(self.table.getHeights())
        self.setWidths(self.table.getWidths())
        self.Draw()

    def setWidths(self, widths):
        loadWidths = np.array(widths)

        self.Widths = (loadWidths / max(loadWidths)) * self.maxsize

    def setHeights(self, heights):
        loadHeights = np.array(heights)
        self.Heights = (loadHeights / max(loadHeights)) * self.maxsize


class bar(QtWidgets.QWidget):

    def __init__(self, idx, w, h, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.w, self.h = w, h
        layout = QtWidgets.QHBoxLayout()

        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )

        color = "#FFFFFF"
        while color == "#FFFFFF": color = randomColor()

        if idx % 2 == 0:
            color = "#FFFFFF"

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        self.setLayout(layout)

    def sizeHint(self):
        return QtCore.QSize(self.w, self.h)


class WidgetFLineDimensionsInputs(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(WidgetFLineDimensionsInputs, self).__init__(*args, **kwargs)

        self.Title = "Dimensions"
        self.HideLine = False
        self.inputnames = ["Unit Cell Length []", "Central Line Width []"]

        self.setLayout(QGridLayout())
        self.layout().addWidget(QLabel(self.Title), 0, 0)

        self.InputWidget = QWidget()
        self.container = QVBoxLayout()
        for col in range(len(self.inputnames)):
            self.container.addWidget(WidgetDoubleInput(self.inputnames[col]))
        self.InputWidget.setLayout(self.container)
        self.layout().addWidget(self.InputWidget, 1, 1, Qt.AlignVCenter)

        self.tableInput = TableInputWidget()

        self.layout().addWidget(self.tableInput, 1, 0, Qt.AlignTop)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#057878"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)


    def getValue(self):
        return self.tableInput.getData()

    def getHeights(self):
        return self.tableInput.getHeights()

    def getWidths(self):
        return self.tableInput.getWidths()
