import matplotlib
import numpy as np
from PySide6.QtGui import QPalette, QColor, Qt
from Utils_GUI import randomColor
from Widgets.FloatNLabelInputWidget import WidgetDoubleInput
from Widgets.TableInputWidget import TableInputWidget

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
        maxSize = 50
        centralLineW = 10
        load_widths = np.array(load_widths)
        load_heights = np.array(load_heights)

        # normalise to largest value
        load_heights = ((load_heights / max(load_heights)) * maxSize) + centralLineW
        load_widths = ((load_widths / max(load_widths)) * maxSize) + centralLineW

        # load_widths = (load_widths/max(load_widths)) * maxSize

        load_idx = 0
        for i in range(nloads * 2 + 1):
            if i % 2 == 0:
                r = bar(centralLineW, centralLineW)
                r.setMaximumHeight(centralLineW)
                self.layout().addWidget(r, 0, i)

            else:

                w = load_widths[load_idx]
                h = load_heights[load_idx]
                load_idx += 1

                r = bar(w, h)
                r.setMaximumHeight(h)
                r.setMaximumWidth(w)

                self.layout().addWidget(r, 0, i, Qt.AlignHCenter)


class bar(QtWidgets.QWidget):

    def __init__(self, w, h, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.w, self.h = w, h
        layout = QtWidgets.QHBoxLayout()

        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )

        color = "#FFFFFF"
        while color == "#FFFFFF":
            color = randomColor()
        if w == 10:
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
        self.inputnames = ["Unit Cell Length []", "Central Line Width []"]

        self.setLayout(QGridLayout())
        self.layout().addWidget(QLabel(self.Title), 0, 0)
        self.ButtonLineVeiwer = QPushButton('Veiw Constructed line')
        self.layout().addWidget(self.ButtonLineVeiwer, 1, 1, Qt.AlignTop)
        self.ButtonLineVeiwer.clicked.connect(self.ShowLineWindow)

        self.InputWidget = QWidget()
        self.container = QVBoxLayout()
        for col in range(len(self.inputnames)):
            self.container.addWidget(WidgetDoubleInput(self.inputnames[col]))
        self.InputWidget.setLayout(self.container)
        self.layout().addWidget(self.InputWidget, 1, 1, Qt.AlignVCenter)

        self.tableInput = TableInputWidget(onChange = self.ShowLineWindow)
        self.layout().addWidget(self.tableInput, 1, 0, Qt.AlignTop)

        self.line = QWidget()
        self.layout().addWidget(self.line)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(randomColor()))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def getValues(self):
        res = []
        for child in self.children():
            try:
                res.append(child.getTitleAndValue())
            except:
                pass
        return res

    def ShowLineWindow(self):

        try:

            b = self.layout().takeAt(4)
            b.widget().deleteLater()

            self.layout().addWidget(Line(self.getWidths(), self.getHeights()),2,0,2,0)

        except:
            print("bad value")

        print(self.getWidths(), "\n", self.getHeights())

    def getHeights(self):
        return self.tableInput.getHeights()

    def getWidths(self):
        return self.tableInput.getWidths()
