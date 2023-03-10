from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QWidget, QVBoxLayout, QScrollArea

from python_gui.widgets.plot_widget import WidgetGraph_fig

ROWS = 5
COLS = 2


class Plot_Window(QScrollArea):
    """
    This "window" is floquet_alpha QWidget. If it has no parent, it
    will appear as floquet_alpha free-floating window as we want.
    """

    def __init__(self, plots):
        super().__init__()

        self.setWindowTitle("PLOTS")
        self.grid = QGridLayout()
        self.vbox = QVBoxLayout()

        holder = QWidget()
        holder.setLayout(self.grid)
        self.setWidgetResizable(True)

        self.plots = []

        self.update_plots(plots)

        self.plot()

        self.vbox.addWidget(holder)
        self.setWidget(holder)
        self.setMinimumWidth(1200)
        self.setMinimumHeight(800)

    def plot(self):

        # todo destory all open plots

        for child in self.grid.children():
            child.deleteLater()

        for r, row in enumerate(self.plots):
            for c, plot in enumerate(row):
                self.grid.addWidget(WidgetGraph_fig(plot), r + 1, c, Qt.AlignTop)

    def update_plots(self, plots):
        # transform 1D matrix to 2d or size ROWS X COLS
        new_plots = []
        idx = 0
        for r in range(ROWS):

            plt_row = []
            if idx < len(plots):
                plt_row.append(plots[idx:idx + COLS])
                idx += COLS
            if plt_row:
                new_plots.append(*plt_row)

        self.plots = new_plots
        self.plot()
        return new_plots
