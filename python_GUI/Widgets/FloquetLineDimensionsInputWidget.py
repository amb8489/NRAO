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

    def __init__(self, load_widths, load_heights, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLayout(QGridLayout())
        self.layout().setHorizontalSpacing(0)
        self.layout()

        nloads = len(load_widths)
        centralLineW = 5
        load_widths = np.array(load_widths)
        load_heights = np.array(load_heights)

        # normalise to largest value

        # load_heights = (load_heights / max(load_heights)) * maxSize
        # load_widths = (load_widths / max(load_widths)) * maxSize

        load_heights = (load_heights / centralLineW) * centralLineW
        load_widths = (load_widths / centralLineW) * centralLineW

        load_idx = 0
        for i in range(nloads * 2 + 1):
            if i % 2 == 0:
                r = bar(i, centralLineW, centralLineW)
                r.setMaximumHeight(centralLineW)
                self.layout().addWidget(r, 1, i)

            else:

                w = load_widths[load_idx]
                h = load_heights[load_idx]
                load_idx += 1

                r = bar(i, w, h)
                r.setMaximumHeight(h)
                r.setMaximumWidth(w)
                self.layout().addWidget(QLabel(f"L{load_idx}"), 0, i, Qt.AlignHCenter)

                self.layout().addWidget(r, 1, i, Qt.AlignHCenter)


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
        self.ButtonLineVeiwer = QPushButton('Hide/Show Line')
        self.layout().addWidget(self.ButtonLineVeiwer, 1, 1, Qt.AlignTop)
        self.ButtonLineVeiwer.clicked.connect(self.showHideLine)

        self.InputWidget = QWidget()
        self.container = QVBoxLayout()
        for col in range(len(self.inputnames)):
            self.container.addWidget(WidgetDoubleInput(self.inputnames[col]))
        self.InputWidget.setLayout(self.container)
        self.layout().addWidget(self.InputWidget, 1, 1, Qt.AlignVCenter)

        self.tableInput = TableInputWidget(onChange=self.updateLine)
        self.layout().addWidget(self.tableInput, 1, 0, Qt.AlignTop)

        self.line = QWidget()
        self.layout().addWidget(self.line)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#057878"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def getValues(self):

        return self.tableInput.getData()

    def showHideLine(self):

        self.HideLine = not self.HideLine

        self.line.hide() if self.HideLine else self.line.show()

    def updateLine(self):

        try:

            b = self.layout().takeAt(4)
            b.widget().deleteLater()

            self.line = Line(self.getWidths(), self.getHeights())
            self.layout().addWidget(self.line, 2, 0, 2, 0)

            if self.HideLine:
                self.line.hide()

        except:
            print("bad value")

    def getHeights(self):
        return self.tableInput.getHeights()

    def getWidths(self):
        return self.tableInput.getWidths()
