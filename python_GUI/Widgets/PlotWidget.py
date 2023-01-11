import matplotlib
from PySide6.QtGui import QPalette, QColor
from python_GUI.utillsGUI import randomColor
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PySide6 import QtWidgets
from PySide6.QtWidgets import QVBoxLayout


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, Xdata,Ydata,title="TBD", width=4, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        fig.suptitle(title)
        self.axes.set_xlabel('Frequency')
        self.axes.set_ylabel('Frequency')
        self.axes.plot(Xdata,Ydata)

        super(MplCanvas, self).__init__(fig)


class WidgetGraph(QtWidgets.QWidget):

    def __init__(self, title,Xdata,Ydata, *args, **kwargs):
        super(WidgetGraph, self).__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.plt = MplCanvas(Xdata,Ydata,title=title, width=4, height=4, dpi=100)
        self.layout().addWidget(NavigationToolbar(self.plt, self))
        self.layout().addWidget(self.plt)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(randomColor()))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # self.setFixedWidth(400)
        # self.setFixedHeight(400)

        self.setMinimumWidth(250)
        self.setMinimumHeight(250)
