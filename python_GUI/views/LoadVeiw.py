import time

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

        settings = []
        settings_names = []
        with open("/Users/aaron/PycharmProjects/NRAO/python_GUI/Setting/settings.txt", "r") as settings_file:
            for line in settings_file:
                line = line.split(" ", 1)
                name = line[0]
                setting = json.loads(line[1])

                print("name", name)
                print("setting", setting)

                settings_names.append(name)
                settings.append(setting)

        if not settings:
            self.layout().addWidget(QLabel("no setting have been saved"), 0, 0)

        for i, setting_name in enumerate(settings_names):

            #todo fix inx
            load_button = QPushButton('Load', self, clicked=lambda :self.Load(settings[-1]))
            delete_button = QPushButton(f'Delete {i}', self, clicked=lambda: self.Delete(-1))
            name_label = QLabel(setting_name)

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

    def Load(self,inputs):
        # todo pass loaded inout back to main window and have them loaded into the UI
        print("loading ")

        inputs = inputs

        self.settings_model.set_values(inputs)
        time.sleep(1)
        self.close()
