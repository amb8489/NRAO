import random
import time

from PySide6.QtWidgets import QScrollArea, QGridLayout, QLabel, QLineEdit, QPushButton

from python_gui import utills_gui
from python_gui.utills_gui import randomColor, SETTINGS_FILE_PATH, random_setting


class SaveWindow(QScrollArea):
    """
    This "window" is alpha_plt QWidget. If it has no parent, it
    will appear as alpha_plt free-floating window as we want.
    """

    #todo make not relitive to my computer
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

        self.random_settings_button = QPushButton(text='Random SETTINGS', objectName='rand_BUTTON',
                                                  clicked=self.mk_Random_settings)
        self.layout().addWidget(self.random_settings_button, 2, 0)

        self.setFixedWidth(400)
        self.setFixedHeight(200)

    def mk_Random_settings(self):
        with open(SETTINGS_FILE_PATH, "a") as settings_file:
            for i in range(10):
                type = random.choice(["cpw", "MS"])

                if type == "cpw":
                    nrow = 3
                else:
                    nrow = 2
                self.settings = random_setting(nrow)

                settings_file.write(

                    f"{type} {randomColor()}_{i} " + str(self.settings).replace("'", "\"") + "\n")

        time.sleep(1)
        self.close()

    def Save(self):
        setting_name = self.name_input.text() if self.name_input.text() else randomColor()
        setting_name = setting_name.replace(" ", "_")

        with open(SETTINGS_FILE_PATH, "a") as settings_file:
            print(self.settings)
            settings_file.write(f"{self.line_type} {setting_name} " + str(self.settings).replace("'", "\"") + "\n")

        print(f"saving {setting_name}")
        # todo save setting values somewere
        time.sleep(1)
        self.close()
