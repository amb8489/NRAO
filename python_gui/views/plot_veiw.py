from PySide6.QtWidgets import QPushButton, QGridLayout, QWidget, QVBoxLayout, QScrollArea

from model_inputs.cpw_inputs import CPWInputs
from model_inputs.micro_strip_inputs import MicroStripInputs
from python_gui.plot_data import simulate
from python_gui.widgets.plot_widget import WidgetGraph_fig
from utills.constants import MICRO_STRIP_TYPE, CPW_TYPE


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

        self.inputs = self.line_model_to_input_obj(line_model)

        holder = QWidget()
        holder.setLayout(self.grid)
        self.setWidgetResizable(True)

        plots = simulate(line_model.type, self.inputs)

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

        plots = simulate(self.line_model.type, self.inputs)

        for i in range(2):
            for j in range(3):
                self.grid.addWidget(WidgetGraph_fig(plots[j][i]), j, i + 1)

    def clearPlots(self):
        for i in range(self.grid.count()):
            child = self.grid.itemAt(i).widget()
            if child:
                child.deleteLater()

    # todo refactor this into the indiviucal line model to be able to return its own input obj

    """
    what we are doing is getting the inputs from the GUI and simulating them 
    
    curretnly when getting the inputs they are in json form and we neeed to go from json to the inputObj according to the
    line type and pass that to the simulate function
    
    """

    def line_model_to_input_obj(self, line_model):

        inputs = line_model.get_inputs()

        # todo change based on line model

        # make inputs based on the line type
        if line_model.type == MICRO_STRIP_TYPE:
            self.inputs = MicroStripInputs()
        elif line_model.type == CPW_TYPE:
            self.inputs = CPWInputs()
        else:
            pass

        return
