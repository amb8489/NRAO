import time

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QLabel, QGridLayout, QVBoxLayout, QWidget, QScrollArea
import json

from python_GUI.Widgets.ButtonWithIdxWidget import idxButton
from python_GUI.Widgets.nameLoadRemoveRowWidget import Row


class LoadSettingsWindow(QScrollArea):
    """
    This "window" is alpha_plt QWidget. If it has no parent, it
    will appear as alpha_plt free-floating window as we want.
    """

    def __init__(self, settings_model):
        super().__init__()

        self.settings_file_path = "/Users/aaron/PycharmProjects/NRAO/python_GUI/Setting/settings.txt"
        self.settings_model = settings_model

        self.grid = QGridLayout()
        self.vbox = QVBoxLayout()

        holder = QWidget()
        holder.setLayout(self.grid)
        self.setWidgetResizable(True)

        self.setWindowTitle(f"saved setting for {settings_model.type}")

        settings = []

        with open(self.settings_file_path, "r") as settings_file:
            for line_number, line in enumerate(settings_file):
                line = line.split(" ", 2)
                setting_type = line[0]

                # filter out other model settings that are not settings for the current model
                if setting_type == settings_model.type:
                    setting_name = f"{setting_type} {line[1]}"
                    setting = json.loads(line[2])

                    settings.append((setting, setting_name, setting_type, line_number))

        if settings:
            self.rows = []

            for i, setting in enumerate(settings):
                setting, setting_name, setting_type, line_number = setting

                self.rows.append(Row(setting_name, i, line_number, self.Load, self.Delete, [i, setting, setting_type],
                                     [setting_name, i, line_number]))
                self.grid.addWidget(self.rows[i], i + 1, 0, Qt.AlignTop)

        self.cancel_button = QPushButton('Cancel', self, clicked=lambda: self.close())
        self.grid.addWidget(self.cancel_button, len(settings) + 1 if len(settings) else 2, 0)

        self.vbox.addWidget(holder)
        self.setWidget(holder)

        self.setFixedWidth(600)
        self.setFixedHeight(400)

    def Delete(self, argsArr):

        name, idx, linenumner = argsArr
        print(f"Deleting {name} idx in options list", idx, "line number in settings file", linenumner)

        # update the rest of the rows idx and line numbers that came after idx in rows array

        for i in range(idx, len(self.rows)):
            self.rows[i].DownShiftIdx()

        self.rows[idx].deleteLater()
        del self.rows[idx]

        with open(self.settings_file_path, "r+") as f:
            lines = f.readlines()
            f.seek(0)
            for i, line in enumerate(lines):
                if i != linenumner:
                    f.write(line)
            f.truncate()

    def Load(self, argsArr):

        idx, setting, setting_type = argsArr

        print("loading:", idx)
        if setting_type != self.settings_model.type:
            print(f"cant load  {setting_type} when currently on {self.settings_model.type}")
            self.close()

            return

        self.settings_model.set_values(setting)
        time.sleep(1)
        self.close()
