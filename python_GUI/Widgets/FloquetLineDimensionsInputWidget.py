import matplotlib
import numpy as np
from PySide6.QtGui import QPalette, QColor, Qt, QFont

from python_GUI.Widgets.FloatNLabelInputWidget import WidgetDoubleInput
from python_GUI.Widgets.TableInputWidget import TableInputWidget
from python_GUI.utillsGUI import randomColorBright

matplotlib.use('Qt5Agg')
from PySide6.QtWidgets import QGridLayout, QLabel, QVBoxLayout, QWidget, QScrollArea
from PySide6 import QtWidgets, QtCore


class Line(QtWidgets.QWidget):

    def __init__(self, table, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.lengths = []
        self.widths = []
        self.table = table

        self.table.setOnChange(self.updateLine)
        # todo add input connection in for central line
        self.centralLineW = 5
        self.maxsize = self.centralLineW

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
        for i in range(len(self.lengths) * 2 + 1):
            if i % 2 == 0:

                r = rectangleWidget(False, i, self.centralLineW, self.centralLineW)
                r.setMaximumHeight(self.centralLineW)
                self.grid.addWidget(r, 1, i)

            else:

                load_length = self.lengths[loadIdx]
                load_width = self.widths[loadIdx]
                loadIdx += 1

                r = rectangleWidget(True, loadIdx, load_length, load_width, onClick=self.table.SelectRow)
                r.setMaximumHeight(load_width)
                r.setMaximumWidth(load_length)

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
        self.setLengths(self.table.get_lengths())
        self.setWidths(self.table.get_widths())
        self.Draw()

    def setLengths(self, lengths):

        load_lengths = np.array(lengths)
        w = (load_lengths / self.centralLineW)
        # self.centralLineW = 10
        self.lengths = w * self.centralLineW

    def setWidths(self, widths):

        load_widths = np.array(widths)
        h = (load_widths / self.centralLineW)
        # self.centralLineW = 10
        self.widths = h * self.centralLineW


# widget for rectangleWidget
class rectangleWidget(QtWidgets.QWidget):

    def __init__(self, isLoad, tableIdx, length, width, onClick=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.l, self.w = length, width
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
        return QtCore.QSize(self.l, self.w)


class WidgetFLineDimensionsInputs(QtWidgets.QWidget):

    def __init__(self, colNames, *args, **kwargs):
        super(WidgetFLineDimensionsInputs, self).__init__(*args, **kwargs)

        self.HideLine = False

        # main layout
        self.setLayout(QGridLayout())

        # component title

        self.title = QLabel("Dimensions")
        self.title.setFont(QFont('Arial', 16))
        self.layout().addWidget(self.title, 0, 0)

        # input widgets for UC length and Line Width
        self.container = QVBoxLayout()
        self.inputnames = ["Unit Cell Length []", "Central Line Width []"]
        self.inputs = []
        for col in range(len(self.inputnames)):
            input_widget = WidgetDoubleInput(self.inputnames[col])
            self.container.addWidget(input_widget)
            self.inputs.append(input_widget)

        self.InputWidget = QWidget()
        self.InputWidget.setLayout(self.container)
        self.layout().addWidget(self.InputWidget, 1, 1, Qt.AlignVCenter)

        # table for load widths and lengths inputs
        self.tableInput = TableInputWidget(colNames)
        self.layout().addWidget(self.tableInput, 1, 0, Qt.AlignTop)

        # set widget color
        self.setBackGroundColor("#057878")

    def setBackGroundColor(self, hex_color: str):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(hex_color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def getLengths(self):
        return self.tableInput.getLengths()

    def getWidths(self):
        return self.tableInput.getWidths()

    def getValues(self):
        values = {f"loads": self.tableInput.getData()}
        for input in self.inputs:
            values[input.getTitleAndValue()[0]] = input.getTitleAndValue()[1]

        return values

    def setValues(self, inputs):
        loads = inputs['loads']

        self.tableInput.setData(loads)

        for i, input in enumerate(self.inputs):
            input.setValue(inputs[input.objectName()])
