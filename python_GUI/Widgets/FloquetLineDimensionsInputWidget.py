import matplotlib
import numpy as np
from PySide6.QtGui import QPalette, QColor, Qt, QPixmap
from python_GUI.utillsGUI import randomColor, randomColorBright
from python_GUI.Widgets.FloatNLabelInputWidget import WidgetDoubleInput
from python_GUI.Widgets.TableInputWidget import TableInputWidget

matplotlib.use('Qt5Agg')
from PySide6.QtWidgets import QGridLayout, QLabel, QVBoxLayout, QWidget, QScrollArea, QPushButton
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

        self.layO = QGridLayout()
        self.scroll = QScrollArea()  # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()  # Widget that contains the collection of Vertical Box
        self.grid = QGridLayout()  # The Vertical Box that contains the Horizontal Boxes of  labels and buttons

        self.widget.setLayout(self.grid)
        self.layO.addWidget(QLabel("Line Visualizer"), 0, 0)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.layO.addWidget(self.scroll)
        self.grid.setHorizontalSpacing(0)
        self.setLayout(self.layO)
        self.setFixedHeight(200)
        self.setFixedWidth(800)

        # color background
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#ff9d00"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        palette.setColor(QPalette.Window, QColor("#FFFFFF"))
        self.scroll.setPalette(palette)
        self.scroll.setAutoFillBackground(True)

    def Draw(self):

        loadIdx = 0
        for i in range(len(self.Widths) * 2 + 1):
            if i % 2 == 0:

                r = rectangleWidget(False, i, self.centralLineW, self.centralLineW)
                r.setMaximumHeight(self.centralLineW)
                self.grid.addWidget(r, 1, i)

            else:

                w = self.Widths[loadIdx]
                h = self.Heights[loadIdx]
                loadIdx += 1

                r = rectangleWidget(True, loadIdx, w, h, onClick=self.table.SelectRow)
                r.setMaximumHeight(h)
                r.setMaximumWidth(w)

                self.grid.addWidget(QLabel(f"L{loadIdx}"), 0, i, Qt.AlignHCenter)
                self.grid.addWidget(r, 1, i, Qt.AlignHCenter)

    def ToggleShowHide(self):
        self.HideLine = not self.HideLine
        self.show() if self.HideLine else self.hide()

    def clearBars(self):
        for i in range(self.grid.count()):
            child = self.grid.itemAt(i).widget()
            if child:
                child.deleteLater()

    def updateLine(self):
        self.clearBars()
        self.setHeights(self.table.getHeights())
        self.setWidths(self.table.getWidths())
        self.Draw()

    def setWidths(self, widths):
        loadWidths = np.array(widths)
        # todo max(loadWidths) should be the central line widths really
        self.Widths = (loadWidths / max(loadWidths)) * self.maxsize

    def setHeights(self, heights):
        loadHeights = np.array(heights)

        # todo max(loadWidths) should be the central line widths really
        self.Heights = (loadHeights / max(loadHeights)) * self.maxsize


# widget for rectangleWidget
class rectangleWidget(QtWidgets.QWidget):

    def __init__(self, isLoad, tableIdx, w, h, onClick=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.w, self.h = w, h
        self.onClick = onClick
        self.idxInTable = tableIdx

        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )

        color = "#000000"
        if isLoad:
            color = randomColorBright()

        # set widget color
        self.setBackGroundColor(color)

    def setBackGroundColor(self, hex_color: str):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(hex_color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def mousePressEvent(self, event):
        if self.onClick:
            print("clicked")

    def sizeHint(self):
        return QtCore.QSize(self.w, self.h)


class WidgetFLineDimensionsInputs(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(WidgetFLineDimensionsInputs, self).__init__(*args, **kwargs)

        self.HideLine = False

        # main layout
        self.setLayout(QGridLayout())

        # component title
        self.Title = "Dimensions"
        self.layout().addWidget(QLabel(self.Title), 0, 0)

        # input widgets for UC length and Line Width
        self.container = QVBoxLayout()
        self.inputnames = ["Unit Cell Length []", "Central Line Width []"]

        for col in range(len(self.inputnames)):
            self.container.addWidget(WidgetDoubleInput(self.inputnames[col]))

        self.InputWidget = QWidget()
        self.InputWidget.setLayout(self.container)
        self.layout().addWidget(self.InputWidget, 1, 1, Qt.AlignVCenter)

        # table for load widths and lengths inputs
        self.tableInput = TableInputWidget()
        self.layout().addWidget(self.tableInput, 1, 0, Qt.AlignTop)

        # set widget color
        self.setBackGroundColor("#057878")

    def setBackGroundColor(self, hex_color: str):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(hex_color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def getTableValues(self):
        return self.tableInput.getData()

    def getHeights(self):
        return self.tableInput.getHeights()

    def getWidths(self):
        return self.tableInput.getWidths()
