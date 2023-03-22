import numpy as np
from PySide6 import QtWidgets
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QGridLayout, QPushButton, QLabel, QFileDialog, QRadioButton

from python_gui.utills.setting_gui import GUI_setting
from python_gui.utills.utills_gui import randomColorBright
from python_gui.widgets.CPW_artifical_dimensions_input_widget import WidgetCPWARTDimensionsInputs
from python_gui.widgets.float_input_widget import WidgetDoubleInput
from python_gui.widgets.frequency_range_input_widget import WidgetFrequencyInputs
from python_gui.widgets.gain_input_widget import WidgetGainInputs


class sim_file(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(sim_file, self).__init__(*args, **kwargs)

        self.type = "SIM_FILE"

        self.setLayout(QGridLayout())

        # ---------------------------------- model_inputs MS
        self.file_name_display = QLabel("")
        self.layout().addWidget(self.file_name_display,0,0)

        self.file_choose_button = QPushButton('Choose a File')
        self.file_choose_button.clicked.connect(self.selectFile)
        self.layout().addWidget(self.file_choose_button, 1, 0)

        self.use_art_line_inputs = QRadioButton("SIMULATE ART CPW LINE")
        self.use_art_line_inputs.setChecked(True)
        self.use_art_line_inputs.toggled.connect(lambda: self.setArtLineInputs())
        self.layout().addWidget(self.use_art_line_inputs, 0, 1)


        self.Lu_length = WidgetDoubleInput("Lu length [microns]", MinVal=0,Decimals=2)
        self.layout().addWidget(self.Lu_length, 1, 1)


        self.dimensionsInputWidget = WidgetCPWARTDimensionsInputs(
            #["Line length [microns]"]
            ["N Lu repeated"],
            [], row_name="Line",line_input_title="Numer of lines in unit cell")
        self.layout().addWidget(self.dimensionsInputWidget,2, 1,1,1)


        #todo add to set and get values
        self.Wu_length = WidgetDoubleInput("Wu [microns]", DefaultVal= 0, MinVal=0, MaxVal=0)
        self.layout().addWidget(self.Wu_length, 0, 2)
        self.Wl_length = WidgetDoubleInput("Wl [microns]", DefaultVal =0, MinVal=0, MaxVal=0)
        self.layout().addWidget(self.Wl_length, 1, 2)









        self.WidgetGainInputs = WidgetGainInputs()
        self.layout().addWidget(self.WidgetGainInputs, 2, 0)


        self.freqRangeWidget = WidgetFrequencyInputs()
        self.layout().addWidget(self.freqRangeWidget, 3,0)



        # set widget color
        self.setBackGroundColor(randomColorBright())

        self.setMinimumHeight(800)
        self.setMinimumWidth(1275)


        self.file_path = ''
        self.setArtLineInputs()

    def selectFile(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        self.file_path = dialog.getOpenFileName(self, 'Find file')[0]
        self.file_name_display.setText(f"File selected: {self.file_path}")



        # load in csv

        csv_data = np.loadtxt(self.file_path,delimiter="	", dtype=float)

        # get how many widths there are

        width_range = (csv_data[0][0],csv_data[-1][0])


        self.Wu_length.setMinMaxRange(width_range[0],width_range[-1])
        self.Wl_length.setMinMaxRange(width_range[0],width_range[-1])

        self.Wu_length.setValue(width_range[0])
        self.Wl_length.setValue(width_range[-1])


        print(width_range)






    def get_inputs(self):
        return {
            "sim_file_path": self.file_path,
            "unit_cell_length": self.Lu_length.get_value(),
            "gain_models": self.WidgetGainInputs.getValues(),
            "Frequency Range": self.freqRangeWidget.getValues(),
        }

    def set_setting(self, setting: GUI_setting):
        self.title.setText(f"Current setting: {setting.name}")

    def set_values(self, input: dict):
        self.file_path = input["hfss_touchstone_file_path"]
        file_path = input["hfss_touchstone_file_path"]
        self.file_name_display.setText(f"File selected: {file_path}")
        self.Lu_length.setValue(float(input.get("unit_cell_length", 0)))
        self.WidgetGainInputs.setValues(input.get("gain_models", []))
        self.freqRangeWidget.setValues(input["Frequency Range"])


    def setBackGroundColor(self, hex_color: str):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(hex_color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def setArtLineInputs(self):
        if self.use_art_line_inputs.isChecked():
            self.Lu_length.show()
            self.dimensionsInputWidget.tableInput.model.colNames = ["N Lu Cells [microns]"]

            return
        self.Lu_length.hide()
        self.dimensionsInputWidget.tableInput.model.colNames = ["line length [microns]"]












