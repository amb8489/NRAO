import matplotlib
from PySide6.QtGui import QPalette, QColor, Qt, QFont

from python_gui.line_models.artificial_cpw_input_widget import ArtificialCPIInputsWidget
from python_gui.line_models.cpw_input_widget import CPWInputsWidget
from python_gui.line_models.micro_strip_input_widget import MicroStripInputsWidget
from python_gui.line_models.s_matrix_input_widget import SMatrixInputsWidget
from python_gui.utills.simulation_plotter import simulate
from python_gui.utills.utills_gui import BASE_COLOR
from python_gui.views.load_veiw import LoadSettingsWindow
from python_gui.views.plot_window import Plot_Window
from python_gui.views.save_veiw import SaveWindow

matplotlib.use('Qt5Agg')
from PySide6.QtWidgets import QMainWindow, QGridLayout, QScrollArea, QLabel, QComboBox, QSizePolicy
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


def gen(n):
    for i in range(n):
        yield i


n = 10


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.iter = gen(10)

        self.widnow_width = 600
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

        self.button_exit = QPushButton(text='EXIT', objectName='EXIT_BUTTON', clicked=lambda: exit(0))
        self.ButtonLayout.addWidget(self.button_exit, 0, 0)

        self.button_plot = QPushButton(text='PLOT', objectName='PLOT_BUTTON', clicked=self.show_plot_window)
        self.ButtonLayout.addWidget(self.button_plot, 0, 1)

        self.modelSelector = QComboBox()
        self.modelSelector.addItems(['Micro Strip', 'CPW', 'Artificial CPW', 'HFSS FILE UPLOAD'])
        self.modelSelector.currentTextChanged.connect(self.model_changed)

        self.ButtonLayout.addWidget(self.modelSelector, 0, 2)

        self.button_save_settings = QPushButton(text='SAVE NEW SETTING', objectName='SAVE_BUTTON',
                                                clicked=self.showSaveWindow)
        self.ButtonLayout.addWidget(self.button_save_settings, 1, 0)

        self.button_load_settings = QPushButton(text='LOAD SETTINGS', objectName='SAVE_BUTTON',
                                                clicked=self.showLoadWindow)
        self.ButtonLayout.addWidget(self.button_load_settings, 1, 1)

        self.testButton = QPushButton(text='test', objectName='TEST_BUTTON', clicked=self.print_inputs)
        self.ButtonLayout.addWidget(self.testButton, 1, 2)

        self.ButtonLayoutWidget.setLayout(self.ButtonLayout)

        palette = self.ButtonLayoutWidget.palette()
        palette.setColor(QPalette.Window, QColor(BASE_COLOR))
        self.ButtonLayoutWidget.setPalette(palette)
        self.ButtonLayoutWidget.setAutoFillBackground(True)


        self.Mainlayout.addWidget(self.ButtonLayoutWidget)

        # title
        self.title = QLabel(self.modelSelector.currentText())
        self.title.setMaximumHeight(40)
        palette = self.title.palette()
        palette.setColor(QPalette.Window, QColor("#FFFFFF"))
        self.title.setPalette(palette)
        self.title.setAutoFillBackground(True)
        self.title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont('Arial', 28))
        self.Mainlayout.addWidget(self.title)

        # ---------------------------------- input models
        self.Micro_strip_inputs_widget = MicroStripInputsWidget()
        self.CPW_inputs_widget = CPWInputsWidget()
        self.Atrifical_CPW_inputs_widget = ArtificialCPIInputsWidget()
        self.S_matrix_inputs_widget = SMatrixInputsWidget()

        self.Micro_strip_inputs_widget.setFixedWidth(1250)
        self.Mainlayout.addWidget(self.Micro_strip_inputs_widget)
        self.Mainlayout.addWidget(self.CPW_inputs_widget)
        self.Mainlayout.addWidget(self.Atrifical_CPW_inputs_widget)

        self.Mainlayout.addWidget(self.S_matrix_inputs_widget)

        self.line_model = self.Micro_strip_inputs_widget
        self.line_models = {'Micro Strip': self.Micro_strip_inputs_widget,
                            'CPW': self.CPW_inputs_widget,
                            'Artificial CPW': self.Atrifical_CPW_inputs_widget,
                            'HFSS FILE UPLOAD': self.S_matrix_inputs_widget}
        self.init()

    def showModel(self, line_model):

        for model_name in self.line_models:
            self.line_models[model_name].hide()

        self.line_model = line_model
        self.line_model.show()

        # resetting the plot window
        self.plotWindow = None


    def model_changed(self, modelName):

        self.title.setText(self.modelSelector.currentText())
        self.showModel(self.line_models[modelName])

    def init(self):
        self.Mainlayout.insertStretch(-1, 1)

        # start off with micro strip model showing
        self.showModel(self.Micro_strip_inputs_widget)

        self.setWindowTitle("TKIPA DESIGN TOOL")
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(BASE_COLOR))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        self.ROOT.setLayout(self.Mainlayout)
        self.scroll.setWidget(self.ROOT)

        self.setCentralWidget(self.scroll)

        self.setMinimumHeight(800)
        self.setMinimumWidth(1275)

        self.show()

    def print_inputs(self):
        print(self.line_model.get_inputs())

    def show_plot_window(self):

        plots = simulate(self.line_model)

        if self.plotWindow:
            self.plotWindow.update_plots(plots)
        else:
            # open a new plotting window
            self.plotWindow = Plot_Window(plots)

        self.plotWindow.show()

    def showSaveWindow(self):

        self.SaveWindow = SaveWindow(self.line_model)
        self.SaveWindow.show()

    def showLoadWindow(self):

        self.SaveWindow = LoadSettingsWindow(self.line_model)
        self.SaveWindow.show()
