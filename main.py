import time

import matplotlib
from PySide6.QtGui import QPalette, QColor, Qt
from Inputs.MicroStripInputs import MicroStripInputs
from python_GUI.Widgets.CPW_input_widget import CPWInputsWidget
from python_GUI.Widgets.Micro_strip_input_widget import MicroStripInputsWidget
from python_GUI.Widgets.PlotWidget import WidgetGraph_fig
from python_GUI.Widgets.S_Matrix_input_widget import SMatrixInputsWidget
from python_GUI.plotData import simulate
from python_GUI.utillsGUI import randomColorBright, randomColor

matplotlib.use('Qt5Agg')
from PySide6.QtWidgets import QMainWindow, QApplication, QGridLayout, QScrollArea, QLabel, QComboBox, QLineEdit
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

        self.button_exit = QPushButton('Exit')
        self.ButtonLayout.addWidget(self.button_exit, 0, 0)

        self.button_plot = QPushButton("Plot")
        self.ButtonLayout.addWidget(self.button_plot, 0, 1)

        self.modelSelector = QComboBox()
        self.modelSelector.addItems(['Micro Strip', 'CPW', 'S Matrix'])

        self.modelSelector.currentTextChanged.connect(self.model_changed)

        self.ButtonLayout.addWidget(self.modelSelector, 0, 2)

        self.button_save_settings = QPushButton('Save Settings')
        self.ButtonLayout.addWidget(self.button_save_settings, 1, 1)

        self.button_load_settings = QPushButton('Load Settings')
        self.ButtonLayout.addWidget(self.button_load_settings, 1, 2)

        # buttons onPress
        self.button_plot.clicked.connect(self.show_new_window)
        self.button_exit.clicked.connect(lambda: exit(0))
        self.button_save_settings.clicked.connect(self.showSaveWindow)
        self.button_load_settings.clicked.connect(self.showLoadWindow)

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

        # todo will error on model woth no SCW or table temp fix for testing
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
        # todo put this in line model widget class MicroStripInputsWidget() and CPWInputsWidget()
        # what to do with classes that dont have these subwidgets

        widgets = [self.WidgetGainInputs, self.freqRangeWidget, self.SCW, self.dimensionsInputWidget]

        for widget in widgets:
            print(widget.getTableValues())

    def show_new_window(self, checked):

        # if we already have a window open redisplay the plots
        if self.plotWindow:
            self.plotWindow.clearPlots()
            self.plotWindow.plot()
        else:
            # open a new plotting window
            self.plotWindow = AnotherWindow(self.model_type, self.inputs)

        self.plotWindow.show()

    def showSaveWindow(self):

        # if we already have a window open redisplay the plots
        # todo add in map of the input name to input val
        self.SaveWindow = SaveWindow([1, 2, 3, 4, 5, 6, 7, 8, 9])

        self.SaveWindow.show()

    def showLoadWindow(self):

        self.SaveWindow = LoadSettingsWindow()
        self.SaveWindow.show()


class AnotherWindow(QScrollArea):
    """
    This "window" is alpha_plt QWidget. If it has no parent, it
    will appear as alpha_plt free-floating window as we want.
    """

    def __init__(self, model_type, inputs):
        super().__init__()

        self.setWindowTitle("PLOTS")
        self.grid = QGridLayout()
        self.vbox = QVBoxLayout()
        self.inputs = inputs
        self.model_type = model_type
        holder = QWidget()
        holder.setLayout(self.grid)
        self.setWidgetResizable(True)

        plots = simulate(self.model_type, self.inputs)

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

        plots = simulate(self.model_type, self.inputs)

        for i in range(2):
            for j in range(3):
                self.grid.addWidget(WidgetGraph_fig(plots[j][i]), j, i + 1)

    def clearPlots(self):
        for i in range(self.grid.count()):
            child = self.grid.itemAt(i).widget()
            if child:
                child.deleteLater()


class SaveWindow(QScrollArea):
    """
    This "window" is alpha_plt QWidget. If it has no parent, it
    will appear as alpha_plt free-floating window as we want.
    """

    def __init__(self, settings):
        super().__init__()

        self.settings = settings

        self.setLayout(QGridLayout())
        self.setWindowTitle("save")

        self.name_label = QLabel("Setting Name:")
        self.name_input = QLineEdit(self)

        self.save_button = QPushButton('Save', self)
        self.save_button.clicked.connect(self.Save)

        self.layout().addWidget(self.name_label, 0, 0)
        self.layout().addWidget(self.name_input, 0, 1)
        self.layout().addWidget(self.save_button, 1, 0)

        self.setFixedWidth(400)
        self.setFixedHeight(200)

    def Save(self):
        setting_name = self.name_input.text()
        setting_name = setting_name if setting_name else randomColor()

        with open("/Users/aaron/PycharmProjects/NRAO/python_GUI/Setting/settings.txt", "a") as settings_file:
            print(self.settings)
            settings_file.write(f"{setting_name} " + str(self.settings) + "\n")

        print(f"saving {setting_name}")
        # todo save setting values somewere
        time.sleep(1)
        self.close()


class LoadSettingsWindow(QScrollArea):
    """
    This "window" is alpha_plt QWidget. If it has no parent, it
    will appear as alpha_plt free-floating window as we want.
    """

    def __init__(self):
        super().__init__()

        self.grid = QGridLayout()
        self.vbox = QVBoxLayout()

        holder = QWidget()
        holder.setLayout(self.grid)
        self.setWidgetResizable(True)

        self.setWindowTitle("Load")

        settings = []
        with open("/Users/aaron/PycharmProjects/NRAO/python_GUI/Setting/settings.txt", "r") as settings_file:
            for line in settings_file:
                settings.append(line)

        if not settings:
            self.layout().addWidget(QLabel("no setting have been saved"), 0, 0)

        for i, setting in enumerate(settings):
            name_label = QLabel(setting)
            load_button = QPushButton('Load', self)
            load_button.clicked.connect(self.Load)

            delete_button = QPushButton(f'Delete {i}', self)
            delete_button.clicked.connect(lambda: self.Delete(-1))

            self.grid.addWidget(name_label, i, 0)
            self.grid.addWidget(load_button, i, 1)
            self.grid.addWidget(delete_button, i, 2)

            self.vbox.addWidget(holder)
            self.setWidget(holder)

        self.exit_button = QPushButton('Exit', self)
        self.exit_button.clicked.connect(lambda: self.close())

        self.grid.addWidget(self.exit_button, len(settings) if len(settings) else 1, 0)

        self.setFixedWidth(400)
        self.setFixedHeight(400)

    def Delete(self, idx):
        # todo delete from file and UI will need the index in file and use that index to delete from file and UI
        print("Deleting ", idx)

    def Load(self):
        # todo pass loaded inout back to main window and have them loaded into the UI
        print("loading ")
        time.sleep(1)
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec()
