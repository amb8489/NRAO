import csv
import random

import matplotlib
import numpy as np
from PySide6.QtGui import QPalette, QColor

from python_gui.utills.utills_gui import randomColorBright

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PySide6 import QtWidgets
from PySide6.QtWidgets import QVBoxLayout, QFileDialog, QPushButton, QWidget, QFormLayout, QLineEdit, QInputDialog, \
    QDialog


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, Xdata, Ydata, title, width=4, height=4, dpi=100):
        self.plt.x_data = Xdata
        self.plt.y_data = Ydata
        self.plt.title = title
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        fig.suptitle(title)
        self.axes.plot(Xdata, Ydata)

        super(MplCanvas, self).__init__(fig)


class MplCanvas_fig(FigureCanvasQTAgg):

    def __init__(self, fig):
        super(MplCanvas_fig, self).__init__(fig)


class WidgetGraph_fig(QtWidgets.QWidget):

    def __init__(self, fig, *args, **kwargs):
        super(WidgetGraph_fig, self).__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.fig = fig
        # matpltlib plot
        plt = MplCanvas_fig(fig)

        # navbar for plot
        self.layout().addWidget(NavigationToolbar(plt, self))
        self.layout().addWidget(plt)


        self.save_to_csv_button = QPushButton(text='save to csv', clicked=self.save_to_csv)
        self.layout().addWidget(self.save_to_csv_button)

        # size policy
        self.setMinimumWidth(580)
        self.setMinimumHeight(570)

        self.setMaximumHeight(580)
        self.setMaximumWidth(580)
        # set widget color
        self.setBackGroundColor(randomColorBright())

    def setBackGroundColor(self, hex_color: str):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(hex_color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def save_to_csv(self):


        fields = []
        data = []


        for axs_idx,ax in enumerate(self.fig.axes):
            for subplot_idx ,sub_plot in enumerate(ax.lines):
                data.extend(sub_plot.get_data())


                x = ax.get_xlabel().replace(" ","_")
                y = ax.get_ylabel().replace(" ","_")

                if not x:
                    x = "Frequency"
                if not y:
                    y = "Y_DATA"

                fields.extend([f"{x}", f"{y}"])
        rows = np.column_stack(data)


        popup_for_name = inputdialogdemo(fields,rows)
        popup_for_name.close()






class inputdialogdemo(QDialog):
    def __init__(self,fields,rows,parent = None):
        super(inputdialogdemo, self).__init__(parent)
        self.fields = fields
        self.rows = rows
        self.setWindowTitle("File Name Input")
        self.get_save_file_name()

    def get_save_file_name(self):
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Enter file name:')
        if ok:
            dialog = QFileDialog()
            dialog.setFileMode(QFileDialog.Directory)
            save_location_path = dialog.getExistingDirectory(self, 'Select Directory')


            # check to add .csv at the end and for empty string name
            text = (str(text).replace(".csv",""))+'.csv'
            if text == '.csv':
                text = randomColorBright()+'.csv'


            print(f'saving data to {save_location_path}/{str(text)}')
            with open(f'{save_location_path}/{str(text)}', 'w') as f:
                # using csv.writer method from CSV package
                write = csv.writer(f)
                write.writerow(self.fields)
                write.writerows(self.rows)

        self.close()