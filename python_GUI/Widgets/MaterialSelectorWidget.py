import random
import matplotlib
import pandas as pd
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QGridLayout, QLabel, QTableView

matplotlib.use('Qt5Agg')
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

        self.headers = ["er", "h", "ts", "tg", "t", "tc", "jc", "normal_resistivity", "tand", "other"]


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
                return self.headers[section]

            if orientation == Qt.Vertical:
                return str(self._data.index[section])

    def get_headers(self):
        return self.headers


    def sectionClicked(self, int):
        print("zero")


class WidgetMaterialsSelect(QtWidgets.QWidget):

    def __init__(self, onchange = None, *args, **kwargs):

        self.onchange = onchange

        super(WidgetMaterialsSelect, self).__init__(*args, **kwargs)

        self.setLayout(QGridLayout())

        self.Title = "Material Properties"
        self.layout().addWidget(QLabel(self.Title), 0, 0)

        # table
        self.table = QtWidgets.QTableView()
        self.table.setSelectionBehavior(QTableView.SelectRows)

        # table data
        size = 10
        data = pd.DataFrame(
            [[random.randrange(0, 99) for i in range(size)] for i in range(size)],
            columns=[f'Col {i}' for i in range(size)],
            index=[f'Row {i}' for i in range(size)], )

        # table moedel
        self.model = TableModel(data)
        self.table.setModel(self.model)

        # setting row selections
        self.table.selectionModel().selectionChanged.connect(self.setRowsInSuperConductorInputsOnChange)

        # table size policy
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)

        # table
        self.layout().addWidget(self.table, 1, 0)

        # set widget color
        self.setBackGroundColor("#5b80bd")

    def setBackGroundColor(self, hex_color: str):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(hex_color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)


    def get_values(self):
        row = self.getFirstSelectedRow()
        row_names =  self.model.get_headers()
        return {row_names[i]: row[i] for i in range(len(row))}

    def setRowsInSuperConductorInputsOnChange(self):
        if self.onchange:
            self.onchange(self.get_values())

    def getFirstSelectedRow(self):
        index = self.table.selectionModel().selectedRows()

        if not index:
            selectedRowIdx = 0
        else:
            selectedRowIdx = index[0].row()

        nCols = self.table.model()._data.shape[1]
        model = self.table.model()

        return [model.data(model.index(selectedRowIdx, col), 0) for col in range(nCols)]
