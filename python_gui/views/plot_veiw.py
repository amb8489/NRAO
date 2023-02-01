from PySide6.QtWidgets import QPushButton, QGridLayout, QWidget, QVBoxLayout, QScrollArea

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

        for i in range(2):
            for j in range(3):
                self.grid.addWidget(WidgetGraph_fig(plots[j][i]), j, i + 1)

        self.vbox.addWidget(holder)
        self.setWidget(holder)
        self.setMinimumWidth(900)
        self.setMinimumHeight(700)

    def plot(self):

        # time.sleep(10)

        self.ButtonExit = QPushButton('Close window')
        self.grid.addWidget(self.ButtonExit, 0, 0)
        self.ButtonExit.clicked.connect(lambda: self.close())

        # todo update inputs

        plots = simulate(self.line_model)

        for i in range(2):
            for j in range(3):
                self.grid.addWidget(WidgetGraph_fig(plots[j][i]), j, i + 1)

    def clearPlots(self):
        for i in range(self.grid.count()):
            child = self.grid.itemAt(i).widget()
            if child:
                child.deleteLater()
