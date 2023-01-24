import matplotlib
from PySide6.QtGui import QPalette, QColor
from Inputs.MicroStripInputs import MicroStripInputs
from python_GUI.Widgets.CPW_input_widget import CPWInputsWidget
from python_GUI.Widgets.Micro_strip_input_widget import MicroStripInputsWidget
from python_GUI.Widgets.S_Matrix_input_widget import SMatrixInputsWidget
from python_GUI.utillsGUI import randomColorBright
from python_GUI.views.LoadVeiw import LoadSettingsWindow
from python_GUI.views.PlotVeiw import PlotWindow
from python_GUI.views.SaveVeiw import SaveWindow

matplotlib.use('Qt5Agg')
from PySide6.QtWidgets import QMainWindow, QApplication, QGridLayout, QScrollArea, QLabel, QComboBox
import sys
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget


# TODO:
# [] make material selector change values in SC inputs
# [] put real labels and units for different input widgets
# [] for dim input widget make input for how many loads and load widths ect
# [] show hide button for material selector
# [] make window popup that draws the FL
# [] dynamic input for load widths and hights based on the number of loads
# {} connect input data to sim
# {} updates plots on plot button press
# [] other missed things
# {} style


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.showWidget = False
        self.showMS = True
        self.showMaterialsWidget = False
        self.scroll = QScrollArea()
        self.ROOT = QWidget()
        self.Mainlayout = QVBoxLayout()

        self.plotWindow = None  # No external window yet.

        # ----------------------------------EXIT and Plots buttons

        self.ButtonLayout = QGridLayout()
        self.ButtonLayoutWidget = QWidget()

        # text = '', objectName = '', clicked =

        self.button_exit = QPushButton(text='EXIT', objectName='EXIT_BUTTON', clicked=lambda: exit(0))
        self.ButtonLayout.addWidget(self.button_exit, 0, 0)

        self.button_plot = QPushButton(text='PLOT', objectName='PLOT_BUTTON', clicked=self.show_plot_window)
        self.ButtonLayout.addWidget(self.button_plot, 0, 1)

        self.modelSelector = QComboBox()
        self.modelSelector.addItems(['Micro Strip', 'CPW', 'S Matrix'])
        self.modelSelector.currentTextChanged.connect(self.model_changed)

        self.ButtonLayout.addWidget(self.modelSelector, 0, 2)

        self.button_save_settings = QPushButton(text='SAVE SETTINGS', objectName='SAVE_BUTTON',
                                                clicked=self.showSaveWindow)
        self.ButtonLayout.addWidget(self.button_save_settings, 1, 1)

        self.button_load_settings = QPushButton(text='LOAD SETTINGS', objectName='SAVE_BUTTON',
                                                clicked=self.showLoadWindow)
        self.ButtonLayout.addWidget(self.button_load_settings, 1, 2)

        self.testButton = QPushButton(text='TEST', objectName='TEST_BUTTON', clicked=self.get_inputs)
        self.ButtonLayout.addWidget(self.testButton, 1, 0)

        self.ButtonLayoutWidget.setLayout(self.ButtonLayout)
        self.ButtonLayoutWidget.setFixedHeight(100)

        palette = self.ButtonLayoutWidget.palette()
        palette.setColor(QPalette.Window, QColor(randomColorBright()))
        self.ButtonLayoutWidget.setPalette(palette)
        self.ButtonLayoutWidget.setAutoFillBackground(True)

        self.Mainlayout.addWidget(self.ButtonLayoutWidget)

        # title
        self.title = QLabel(self.modelSelector.currentText())
        self.title.setMaximumHeight(20)

        palette = self.title.palette()
        palette.setColor(QPalette.Window, QColor(randomColorBright()))
        self.title.setPalette(palette)
        self.title.setAutoFillBackground(True)

        self.Mainlayout.addWidget(self.title)

        # ---------------------------------- input models
        self.Micro_strip_inputs_widget = MicroStripInputsWidget()
        self.CPW_inputs_widget = CPWInputsWidget()
        self.S_matrix_inputs_widget = SMatrixInputsWidget()

        self.Mainlayout.addWidget(self.Micro_strip_inputs_widget)
        self.Mainlayout.addWidget(self.CPW_inputs_widget)
        self.Mainlayout.addWidget(self.S_matrix_inputs_widget)

        self.line_model = self.Micro_strip_inputs_widget

        self.line_models = {"Micro Strip": self.Micro_strip_inputs_widget,
                            "CPW": self.CPW_inputs_widget,
                            "S Matrix": self.S_matrix_inputs_widget}
        self.init()

    def showModel(self, line_model):

        for model_name in self.line_models:
            self.line_models[model_name].hide()

        self.line_model = line_model
        self.line_model.show()

        # todo will error on model with no SCW or table temp fix for testing
        try:
            line_model.table.onchange = self.line_model.SCW.setValues
        except:
            pass

    def model_changed(self, modelName):

        self.title.setText(self.modelSelector.currentText())
        self.showModel(self.line_models[modelName])

    def init(self):
        self.Mainlayout.insertStretch(-1, 1)

        self.showModel(self.Micro_strip_inputs_widget)

        # todo
        self.model_type = "MS"
        self.inputs = None
        if self.model_type == "MS":
            self.inputs = MicroStripInputs()
        else:
            print(f"model_type {self.model_type} is not supported")
            exit(1)

        self.setWindowTitle("TKIPA DESIGN TOOL")
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#AAAAAA"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        self.ROOT.setLayout(self.Mainlayout)
        self.scroll.setWidget(self.ROOT)

        self.setCentralWidget(self.scroll)

        self.setFixedWidth(1350)
        self.setFixedHeight(800)

        self.show()

    def srow(self):
        # todo get inputs from selected row
        print(self.line_model.table.getFirstSelectedRow())

    def get_inputs(self):
        try:
            print(self.line_model.get_inputs())
        except:
            pass

    def show_plot_window(self, checked):

        # if we already have a window open redisplay the plots
        if self.plotWindow:
            self.plotWindow.clearPlots()
            self.plotWindow.plot()
        else:
            # open a new plotting window
            self.plotWindow = PlotWindow(self.model_type, self.inputs)

        self.plotWindow.show()

    def showSaveWindow(self):

        # if we already have a window open redisplay the plots
        # todo add in map of the input name to input val
        self.SaveWindow = SaveWindow([1, 2, 3, 4, 5, 6, 7, 8, 9])

        self.SaveWindow.show()

    def showLoadWindow(self):

        self.SaveWindow = LoadSettingsWindow(self.line_model)
        self.SaveWindow.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec()
