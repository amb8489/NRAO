import matplotlib
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QVBoxLayout, QTableView
from python_GUI.Widgets.FloatNLabelInputWidget import WidgetDoubleInput

matplotlib.use('Qt5Agg')
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data, onChange=None):
        super(TableModel, self).__init__()
        self._data = data

        self.onChange = onChange

    def rowCnt(self):
        return len(self._data)

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def insertRows(self, position, rows, QModelIndex, parent):

        self.beginInsertRows(QModelIndex, position, position + rows - 1)
        default_row = ['10'] * len(self._data[0])  # or _headers if you have that defined.
        for i in range(rows):
            self._data.insert(position, default_row)
        self.endInsertRows()
        self.layoutChanged.emit()
        return True

    def getHeights(self):
        return [float(row[0]) for row in self._data]

    def getWidths(self):
        return [float(row[1]) for row in self._data]

    def headerData(self, section, orientation, role):

        if role == Qt.DisplayRole:
            if orientation == Qt.Vertical:
                return str(f"Load {section + 1}")

            if orientation == Qt.Horizontal:
                if section == 0:
                    return str(f"Hight [unit]")
                return str(f"Width [unit]")

    def removeRows(self, position, rows, QModelIndex):
        self.beginRemoveRows(QModelIndex, position, position + rows - 1)
        for i in range(rows):
            del (self._data[position])
        self.endRemoveRows()
        self.layoutChanged.emit()
        return True

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole or role == Qt.EditRole:
                value = self._data[index.row()][index.column()]
                return str(value)

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self._data[index.row()][index.column()] = value

            if self.onChange:
                self.onChange()
            return True
        return False

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def getData(self):
        return self._data

    def setOnChange(self, function):
        self.onChange = function


class TableInputWidget(QtWidgets.QWidget):

    def __init__(self, onChange=None):
        super().__init__()
        self.setLayout(QVBoxLayout())

        self.onChange = onChange

        self.NloadsInput = WidgetDoubleInput("Number of loads", MinVal=1, DefaultVal=2, onchange=self.setNLoads)

        self.layout().addWidget(self.NloadsInput)
        self.table = QtWidgets.QTableView()
        self.table.setSelectionBehavior(QTableView.SelectRows)

        defualt_n_loads = 2
        data = [['10', '10'] for i in range(defualt_n_loads)]
        self.model = TableModel(data, self.onChange)
        self.table.setModel(self.model)

        self.layout().addWidget(self.table)

        # size policy
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)


        # background color
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#FFFFFF"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def setOnChange(self, function):
        self.onChange = function
        self.model.setOnChange(function)

    def getWidths(self):
        return self.model.getWidths()

    def getHeights(self):
        return self.model.getHeights()

    def setNLoads(self):
        numOfWantedLoads = self.NloadsInput.getTitleAndValue()[1]
        numOfCurrLoads = self.model.rowCnt()
        function = self.insert_row if numOfWantedLoads > numOfCurrLoads else self.delete_row

        for i in range(int(abs(numOfCurrLoads - numOfWantedLoads))):
            function()
        if self.onChange():
            self.onChange()

    def insert_row(self):
        self.model.insertRows(self.model.rowCnt(), 1, self.table.currentIndex(), None)

    def delete_row(self):
        if self.model.rowCnt() > 1:
            self.model.removeRows(self.model.rowCnt() - 1, 1, self.table.currentIndex())

    def getData(self):
        return self.model.getData()
