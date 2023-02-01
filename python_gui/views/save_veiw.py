import time

from PySide6.QtWidgets import QScrollArea, QGridLayout, QLabel, QLineEdit, QPushButton

from python_gui.utills.utills_gui import SETTINGS_FILE_PATH, randomColor


class SaveWindow(QScrollArea):
    """
    This "window" is alpha_plt QWidget. If it has no parent, it
    will appear as alpha_plt free-floating window as we want.
    """

    # todo make not relitive to my computer
    def __init__(self, line_model):
        super().__init__()

        self.line_type = line_model.type
        self.settings = line_model.get_inputs()

        self.setLayout(QGridLayout())
        self.setWindowTitle(f"saved setting for {self.line_type}")

        self.name_label = QLabel("setting Name:")
        self.name_input = QLineEdit(self)

        self.save_button = QPushButton('Save', self, clicked=self.Save)
        self.cancel_button = QPushButton('Cancel', self, clicked=lambda: self.close())

        self.layout().addWidget(self.name_label, 0, 0)
        self.layout().addWidget(self.name_input, 0, 1)
        self.layout().addWidget(self.save_button, 1, 0)
        self.layout().addWidget(self.cancel_button, 1, 1)



        self.setFixedWidth(400)
        self.setFixedHeight(200)

        time.sleep(1)
        self.close()

    def Save(self):
        setting_name = self.name_input.text() if self.name_input.text() else randomColor()
        setting_name = setting_name.replace(" ", "_")

        with open(SETTINGS_FILE_PATH, "a") as settings_file:
            print(self.settings)
            settings_file.write(f"{self.line_type} {setting_name} " + str(self.settings).replace("'", "\"") + "\n")

        print(f"saving {setting_name}")
        self.close()
