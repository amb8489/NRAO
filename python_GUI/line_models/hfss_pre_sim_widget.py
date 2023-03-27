import numpy as np
from PySide6 import QtWidgets
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QGridLayout, QPushButton, QLabel, QFileDialog, QRadioButton, QCheckBox

from python_gui.utills.setting_gui import GUI_setting
from python_gui.utills.utills_gui import randomColorBright
from python_gui.widgets.CPW_artifical_dimensions_input_widget import WidgetCPWARTDimensionsInputs
from python_gui.widgets.float_input_widget import WidgetDoubleInput
from python_gui.widgets.frequency_range_input_widget import WidgetFrequencyInputs
from python_gui.widgets.gain_input_widget import WidgetGainInputs


class sim_file(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(sim_file, self).__init__(*args, **kwargs)

        self.csv_data = None

        self.type = "PRE_SIM_FILE"

        self.setLayout(QGridLayout())

        # ---------------------------------- inputs_containters MS
        self.file_name_display = QLabel("")
        self.layout().addWidget(self.file_name_display, 0, 0)

        self.file_choose_button = QPushButton('Choose a File')
        self.file_choose_button.clicked.connect(self.selectFile)
        self.layout().addWidget(self.file_choose_button, 1, 0)

        self.freqRangeWidget = WidgetFrequencyInputs()
        self.layout().addWidget(self.freqRangeWidget, 2, 0)

        self.WidgetGainInputs = WidgetGainInputs()
        self.layout().addWidget(self.WidgetGainInputs, 3, 0)



        self.use_art_line_inputs = QRadioButton("SIMULATE ART CPW LINE")

        self.use_art_line_inputs.setChecked(True)
        self.use_art_line_inputs.toggled.connect(lambda: self.setArtLineInputs())
        self.layout().addWidget(self.use_art_line_inputs, 0, 1)



        self.Lu_length = WidgetDoubleInput("Lu length [microns]", MinVal=0, Decimals=3,DefaultVal=1)
        self.layout().addWidget(self.Lu_length, 1, 1)

        self.dimensionsInputWidget = WidgetCPWARTDimensionsInputs(
            # ["Line length [microns]"]
            ["N Lu segments repeated"],
            [], row_name="Line", line_input_title="Numer of lines in unit cell")
        self.layout().addWidget(self.dimensionsInputWidget, 2, 1, 1, 1)


        self.Wu_length = WidgetDoubleInput("Wu [microns]", DefaultVal=0, MinVal=0, MaxVal=0)
        self.layout().addWidget(self.Wu_length, 0, 2)

        self.Wl_length = WidgetDoubleInput("Wl [microns]", DefaultVal=0, MinVal=0, MaxVal=0)
        self.layout().addWidget(self.Wl_length, 1, 2)






        # set widget color
        self.setBackGroundColor(randomColorBright())

        self.setMinimumHeight(800)
        self.setMinimumWidth(1275)

        self.file_path = ''
        self.setArtLineInputs()

    def selectFile(self, in_file_path=None):

        try:

            if not in_file_path:
                dialog = QFileDialog()
                dialog.setFileMode(QFileDialog.ExistingFile)
                self.file_path = dialog.getOpenFileName(self, 'Find file')[0]
                self.file_name_display.setText(f"File selected: {self.file_path}")

            else:
                self.file_path = in_file_path

            # load in csv

            self.csv_data = np.loadtxt(self.file_path, delimiter="	", dtype=float)

            # get how many widths there are

            self.width_range = (self.csv_data [0][0], self.csv_data [-1][0])

            self.Wu_length.setMinMaxRange(self.width_range[0], self.width_range[-1])
            self.Wl_length.setMinMaxRange(self.width_range[0], self.width_range[-1])

            self.Wu_length.setValue(self.width_range[0])
            self.Wl_length.setValue(self.width_range[-1])

            return True
        except:
            return False

    def get_inputs(self):
        return {
            "Lu_length": self.Lu_length.get_value(),
            "gain_properties": self.WidgetGainInputs.getValues(),
            "Frequency_Range": self.freqRangeWidget.getValues(),
            "Dimensions_inputs": self.dimensionsInputWidget.getValues(),
            "using_art_line": int(self.use_art_line_inputs.isChecked()),
            "file_path": self.file_path,
            "wl_len":self.Wl_length.get_value(),
            "wu_len":self.Wu_length.get_value(),
        }

    def set_setting(self, setting: GUI_setting):
        self.file_name_display.setText(f"{setting.name}")

    def set_values(self, input: dict):
        self.Lu_length.setValue(float(input.get("Lu_length", 0)))
        self.WidgetGainInputs.setValues(input.get("gain_properties", []))
        self.freqRangeWidget.setValues(input["Frequency_Range"])
        self.dimensionsInputWidget.setValues(input["Dimensions_inputs"])
        self.use_art_line_inputs.setChecked(bool(int(input.get("using_art_line", 0))))

        self.file_path = input.get('file_path', '')
        if not self.file_path:
            return

        if self.selectFile(self.file_path):
            self.Wu_length.setMinMaxRange(self.width_range[0], self.width_range[-1])
            self.Wl_length.setMinMaxRange(self.width_range[0], self.width_range[-1])

            self.Wu_length.setValue(input.get("wu_len", 0))
            self.Wl_length.setValue(input.get("wl_len", 0))

    def setBackGroundColor(self, hex_color: str):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(hex_color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def setArtLineInputs(self):
        if self.use_art_line_inputs.isChecked():
            self.Lu_length.show()
            self.dimensionsInputWidget.tableInput.model.colNames = ["N Lu segments repeated"]
        else:
            self.Lu_length.hide()
            self.dimensionsInputWidget.tableInput.model.colNames = ["Line length [microns]"]
        self.dimensionsInputWidget.tableInput.model.layoutChanged.emit()
