from PySide6 import QtWidgets
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QGridLayout, QWidget, QPushButton, QLabel, QFileDialog

from python_GUI.Widgets.FloquetLineDimensionsInputWidget import Line, WidgetFLineDimensionsInputs
from python_GUI.Widgets.FrequencyRangeInputWidget import WidgetFrequencyInputs
from python_GUI.Widgets.GainInputWidget import WidgetGainInputs
from python_GUI.Widgets.SuperConductorInputWidget import WidgetSCInputs
from python_GUI.utillsGUI import randomColorBright


class SMatrixInputsWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(SMatrixInputsWidget, self).__init__(*args, **kwargs)

        # todo refeactor this into there own class widget

        self.setLayout(QGridLayout())

        # ---------------------------------- Inputs MS

        self.layout().addWidget(QLabel("input a file"))

        self.file_choose_button = QPushButton('Choose a File')
        self.file_choose_button.clicked.connect(self.selectFile)
        self.layout().addWidget(self.file_choose_button, 0, 1)

        #
        # set widget color
        self.setBackGroundColor(randomColorBright())
        self.setMaximumHeight(100)

    def selectFile(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        file_name = dialog.getOpenFileName(self, 'Select a file')[0]
        try:
            with open(file_name, "r") as sfile:
                for line in sfile:
                    print(line)

        except:
            print("File error")

    def setBackGroundColor(self, hex_color: str):

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(hex_color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
