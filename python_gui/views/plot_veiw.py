from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QWidget, QVBoxLayout, QScrollArea

from python_gui.plot_data import simulate
from python_gui.widgets.plot_widget import WidgetGraph_fig


class PlotWindow(QScrollArea):
    """
    This "window" is alpha_plt QWidget. If it has no parent, it
    will appear as alpha_plt free-floating window as we want.
    """

    def __init__(self, line_model):
        super().__init__()

        self.setWindowTitle(f"{line_model.type} PLOTS")
        self.grid = QGridLayout()
        self.vbox = QVBoxLayout()
        self.line_model = line_model

        holder = QWidget()
        holder.setLayout(self.grid)
        self.setWidgetResizable(True)

        plots = simulate(line_model)

        for i in range(len(plots)):
            x, y = i % 2, i // 2
            self.grid.addWidget(WidgetGraph_fig(plots[i]), y + 1, x, Qt.AlignTop)

        self.vbox.addWidget(holder)
        self.setWidget(holder)

        self.setMinimumWidth(1200)
        self.setMinimumHeight(600)
        self.setMaximumWidth(1200)
        self.setMaximumHeight(600)

    def plot(self):


        # todo destory all open plots

        plots = simulate(self.line_model)

        for i in range(len(plots)):
            x, y = i % 2, i // 2
            self.grid.addWidget(WidgetGraph_fig(plots[i]), y + 1, x, Qt.AlignTop)

    def clearPlots(self):
        for i in range(self.grid.count()):
            child = self.grid.itemAt(i).widget()
            if child:
                child.deleteLater()
