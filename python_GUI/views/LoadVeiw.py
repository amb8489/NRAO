import time

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QLabel, QGridLayout, QVBoxLayout, QWidget, QScrollArea
import json


class LoadSettingsWindow(QScrollArea):
    """
    This "window" is alpha_plt QWidget. If it has no parent, it
    will appear as alpha_plt free-floating window as we want.
    """

    def __init__(self, settings_model):
        super().__init__()

        self.settings_model = settings_model

        self.grid = QGridLayout()
        self.vbox = QVBoxLayout()

        holder = QWidget()
        holder.setLayout(self.grid)
        self.setWidgetResizable(True)

        self.setWindowTitle("Load")

        self.grid.addWidget(QLabel(f"saved setting for {settings_model.type}"), 0, 0, Qt.AlignTop)

        settings = []
        settings_type = []
        settings_names = []
        with open("/Users/aaron/PycharmProjects/NRAO/python_GUI/Setting/settings.txt", "r") as settings_file:
            for line in settings_file:
                line = line.split(" ", 2)
                setting_type = line[0]

                if setting_type == settings_model.type:
                    setting_name = f"{setting_type} {line[1]}"
                    setting = json.loads(line[2])

                    settings_names.append(setting_name)
                    settings.append(setting)
                    settings_type.append(setting_type)

        if not settings:
            print("hre")
            self.grid.addWidget(QLabel(f"No setting have been saved for {self.settings_model.type}"), 1, 0, Qt.AlignTop)
        else:
            for i, setting_name in enumerate(settings_names):
                # todo fix idx
                load_button = QPushButton('Load', self, clicked=lambda: self.Load(settings[-1], settings_type[-1]))
                delete_button = QPushButton(f'Delete {i}', self, clicked=lambda: self.Delete(-1))
                name_label = QLabel(setting_name)

                self.grid.addWidget(name_label, i + 1, 0, Qt.AlignTop)
                self.grid.addWidget(load_button, i + 1, 1, Qt.AlignTop)
                self.grid.addWidget(delete_button, i + 1, 2, Qt.AlignTop)

        self.exit_button = QPushButton('Exit', self, clicked=lambda: self.close())
        self.grid.addWidget(self.exit_button, len(settings) + 1 if len(settings) else 2, 0)



        self.vbox.addWidget(holder)
        self.setWidget(holder)


        self.setFixedWidth(400)
        self.setFixedHeight(400)




    def Delete(self, idx):
        # todo delete from file and UI will need the index in file and use that index to delete from file and UI
        print("Deleting ", idx)

    def Load(self, inputs, settings_model):
        # todo pass loaded inout back to main window and have them loaded into the UI

        if settings_model != self.settings_model.type:
            print(f"cant load  {settings_model} when currently on {self.settings_model.type}")
            return

        inputs = inputs

        self.settings_model.set_values(inputs)
        time.sleep(1)
        self.close()
