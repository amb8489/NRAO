from PySide6 import QtWidgets
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QGridLayout, QPushButton, QLabel, QFileDialog

from python_gui.utills.utills_gui import randomColorBright
from python_gui.widgets.float_input_widget import WidgetDoubleInput


class SMatrixInputsWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(SMatrixInputsWidget, self).__init__(*args, **kwargs)

        self.type = "SMAT"

        self.setLayout(QGridLayout())

        # ---------------------------------- model_inputs MS

        self.layout().addWidget(QLabel("input a file"))

        self.file_choose_button = QPushButton('Choose a File')
        self.file_choose_button.clicked.connect(self.selectFile)
        self.layout().addWidget(self.file_choose_button, 0, 1)

        self.n_interp_points = WidgetDoubleInput("Number of interpolation points", MinVal=0, DefaultVal=1000)
        self.layout().addWidget(self.n_interp_points, 0, 2)

        self.file_name_display = QLabel("")
        self.layout().addWidget(self.file_name_display, 2, 0,2,1)

        # set widget color
        self.setBackGroundColor(randomColorBright())
        self.setMaximumHeight(100)

        self.file_path = ''

    def selectFile(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        self.file_path = dialog.getOpenFileName(self, 'Select a file')[0]

        self.file_name_display.setText(f"File selected: {self.file_path}")

    def setBackGroundColor(self, hex_color: str):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(hex_color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
