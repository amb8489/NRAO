import random

import matplotlib
import pandas as pd
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QGridLayout, QLabel, QAbstractItemView, QTableView

from python_GUI.utillsGUI import randomColor

matplotlib.use('Qt5Agg')
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                headers = ["er", "h", "ts", "tg", "t", "tc", "jc", "pn", "tand","other"]
                return headers[section]

            if orientation == Qt.Vertical:
                return str(self._data.index[section])

    def sectionClicked(self, int):
        print("zero")


class WidgetMaterialsSelect(QtWidgets.QWidget):

    def __init__(self,onchange, *args, **kwargs):

        self.onchange = onchange

        super(WidgetMaterialsSelect, self).__init__(*args, **kwargs)

        self.setLayout(QGridLayout())

        self.Title = "Material Properties"
        self.inputnames = ["Start Freq [GHz]", "End Freq [GHz]", "Resolution"]

        self.layout().addWidget(QLabel(self.Title), 0, 0)

        self.table = QtWidgets.QTableView()

        # table
        self.table.setSelectionBehavior(QTableView.SelectRows)



        # table data
        size = 10
        data = pd.DataFrame(
            [[random.randrange(0,99) for i in range(size)] for i in range(size)],
            columns=[f'Col {i}' for i in range(size)],
            index=[f'Row {i}' for i in range(size)], )

        self.model = TableModel(data)
        self.table.setModel(self.model)
        self.table.selectionModel().selectionChanged.connect(self.prow)

        # size policy
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # self.table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.table.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)  # ---

        # background color
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(randomColor()))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.layout().addWidget(self.table, 1, 0)

    def prow(self):
        self.onchange(self.getFirstSelectedRow())

    def getFirstSelectedRow(self):
        index = self.table.selectionModel().selectedRows()

        if not index:
            selectedRowIdx = 0
        else:
            selectedRowIdx = index[0].row()

        nCols = self.table.model()._data.shape[1]
        model = self.table.model()

        return [model.data(model.index(selectedRowIdx, col), 0) for col in range(nCols)]
