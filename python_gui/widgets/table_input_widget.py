import matplotlib
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QVBoxLayout, QTableView

from python_gui.widgets.float_input_widget import WidgetDoubleInput

matplotlib.use('Qt5Agg')
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt, QItemSelection, QItemSelectionModel


class TableModel1(QtCore.QAbstractTableModel):

    def __init__(self, data, colNames, onChange=None, row_name=""):
        super(TableModel1, self).__init__()
        self._data = data

        self._row_name = row_name

        self.colNames = colNames

        self.onChange = onChange

    def rowCnt(self):
        return len(self._data)

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def insertRows(self, position, rows, QModelIndex, parent):

        self.beginInsertRows(QModelIndex, position, position + rows - 1)
        default_row = ['1'] * len(self._data[0])  # or _headers if you have that defined.
        for i in range(rows):
            self._data.insert(position, default_row)
        self.endInsertRows()
        self.layoutChanged.emit()
        return True

    def get_lengths(self):
        try:
            return [float(row[0]) for row in self._data]
        except:
            pass

    def get_widths(self):
        try:
            return [float(row[1]) for row in self._data]
        except:
            pass

    def headerData(self, section, orientation, role):

        if role == Qt.DisplayRole:
            if orientation == Qt.Vertical:

                if section % 2 == 1:
                    return  str(f"{section + 1}") + " [Load]"


                return str(f"{section + 1}")+" [CL]"

            if orientation == Qt.Horizontal:

                return self.colNames[section]

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

    def NewTableData(self, data):
        self._data = data
        if self.onChange:
            self.onChange()

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def getData(self):
        return self._data

    def setOnChange(self, function):
        self.onChange = function


class TableInputWidget(QtWidgets.QWidget):

    def __init__(self, colName, onChange=None, row_name="",height = 100,title = "Number of Lines in Unit Cell",isarttanle = False):
        super().__init__()
        self.setLayout(QVBoxLayout())

        self.onChange = onChange

        # input for load number selection
        self.NloadsInput = WidgetDoubleInput(title, MaxVal=100, MinVal=3, DefaultVal=3,
                                             onchange=self.setNLoads,inc_amt = 2)
        self.layout().addWidget(self.NloadsInput)

        # inputs materials_table
        self.table = QtWidgets.QTableView()

        # materials_table selection behavior for setting_rows
        self.table.setSelectionBehavior(QTableView.SelectRows)

        # defualt materials_table data and materials_table model
        defualt_n_lines = 3
        data = [[1] * len(colName) for i in range(defualt_n_lines)]

        self.model = TableModel1(data, colName, self.onChange, row_name)
        self.table.setModel(self.model)

        self.layout().addWidget(self.table)

        # size policy
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.setMaximumHeight(height)
        # set widget color
        self.setBackGroundColor("#FFFFFF")
        # self.setFixedWidth(300)

    def setBackGroundColor(self, hex_color: str):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(hex_color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def setOnChange(self, function):
        self.onChange = function
        self.model.setOnChange(function)

    def get_widths(self):
        return self.model.get_widths()

    def get_lengths(self):
        return self.model.get_lengths()

    def setNLoads(self):
        numOfWantedLoads = self.NloadsInput.getTitleAndValue()[1]
        numOfCurrLoads = self.model.rowCnt()
        function = self.insert_row if numOfWantedLoads > numOfCurrLoads else self.delete_row

        for i in range(int(abs(numOfCurrLoads - numOfWantedLoads))):
            function()
        if self.onChange:
            self.onChange()

    def insert_row(self):
        self.model.insertRows(self.model.rowCnt(), 1, self.table.currentIndex(), None)

    def delete_row(self):
        if self.model.rowCnt() > 1:
            self.model.removeRows(self.model.rowCnt() - 1, 1, self.table.currentIndex())

    def getData(self):
        return self.model.getData()

    def SelectRow(self, idx):

        model = self.table.model()  # get data model for indexes.
        selection = QItemSelection()
        model_index = model.index(idx, 0)
        selection.select(model_index, model_index)  # top left, bottom right identical
        mode = QItemSelectionModel.Select | QtCore.QItemSelectionModel.Rows
        self.table.selectionModel().select(selection, mode)

    def setData(self, data):
        self.NloadsInput.setValue(len(data))

        self.model.NewTableData(data)
        pass
