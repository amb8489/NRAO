import time

from PySide6.QtWidgets import QScrollArea, QGridLayout, QLabel, QLineEdit, QPushButton

from python_GUI.utillsGUI import randomColor


class SaveWindow(QScrollArea):
    """
    This "window" is alpha_plt QWidget. If it has no parent, it
    will appear as alpha_plt free-floating window as we want.
    """

    def __init__(self, line_model):
        super().__init__()

        self.line_type = line_model.type
        self.settings = line_model.get_inputs()

        self.setLayout(QGridLayout())
        self.setWindowTitle(f"saved setting for {self.line_type}")

        self.name_label = QLabel("Setting Name:")
        self.name_input = QLineEdit(self)

        self.save_button = QPushButton('Save', self,clicked = self.Save)
        self.cancel_button = QPushButton('Cancel', self, clicked = lambda :self.close())

        self.layout().addWidget(self.name_label, 0, 0)
        self.layout().addWidget(self.name_input, 0, 1)
        self.layout().addWidget(self.save_button, 1, 0)
        self.layout().addWidget(self.cancel_button, 1, 1)


        self.setFixedWidth(400)
        self.setFixedHeight(200)

    def Save(self):
        setting_name = self.name_input.text()
        setting_name = setting_name if setting_name else randomColor()

        with open("/Users/aaron/PycharmProjects/NRAO/python_GUI/Setting/settings.txt", "a") as settings_file:
            print(self.settings)
            settings_file.write(f"{self.line_type} {setting_name} " + str(self.settings).replace("'","\"") + "\n")

        print(f"saving {setting_name}")
        # todo save setting values somewere
        time.sleep(1)
        self.close()
