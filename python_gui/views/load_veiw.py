import json

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QGridLayout, QVBoxLayout, QWidget, QScrollArea

from python_gui.utills.setting_gui import GUI_setting
from python_gui.utills.utills_gui import SETTINGS_FILE_PATH
from python_gui.widgets.setting_button_row import Setting_Button_Row


class LoadSettingsWindow(QScrollArea):
    """
    This "window" is alpha_plt QWidget. If it has no parent, it
    will appear as alpha_plt free-floating window as we want.
    """

    def __init__(self, settings_model):
        super().__init__()

        # todo make not relitive to my computer
        self.settings_model = settings_model

        self.grid = QGridLayout()
        self.vbox = QVBoxLayout()

        holder = QWidget()
        holder.setLayout(self.grid)
        self.setWidgetResizable(True)

        self.setWindowTitle(f"saved setting for {settings_model.type}")

        settings = []

        # getting all the settings from the settings file that ar for the current simulation line type

        with open(SETTINGS_FILE_PATH, "r") as settings_file:
            row_idx = 0
            for line_number, line in enumerate(settings_file):

                setting_type, setting_name, setting_vals_json_str = line.split(" ", 2)

                # filter out other model settings that are not settings for the current model
                if setting_type == settings_model.type:
                    setting_vals_dict = json.loads(setting_vals_json_str)
                    settings.append(GUI_setting(setting_name, setting_type, setting_vals_dict, row_idx, line_number))
                    row_idx += 1

        self.setting_rows = []

        for row_idx, setting in enumerate(settings):
            self.setting_rows.append(Setting_Button_Row(setting, self.load_setting, self.delete_setting,self.update_setting))
            self.grid.addWidget(self.setting_rows[row_idx], row_idx + 1, 0, Qt.AlignTop)

        self.cancel_button = QPushButton('Cancel', self, clicked=lambda: self.close())
        self.grid.addWidget(self.cancel_button, len(settings) + 1 if len(settings) else 2, 0)

        self.vbox.addWidget(holder)
        self.setWidget(holder)
        self.setFixedWidth(600)
        self.setFixedHeight(400)

    # setting or row number
    def delete_setting(self, row_idx: int):

        # update the rest of the setting_rows idx and line numbers that came after idx in setting_rows array

        row = self.setting_rows[row_idx]

        setting = row.setting

        print(
            f"Deleting:{setting.name} row idx:{setting.setting_row_idx} file line:{setting.setting_file_idx}, {setting.setting_vals_dict}")

        with open(SETTINGS_FILE_PATH, "r+") as f:
            lines = f.readlines()

            f.seek(0)
            for line_idx, line in enumerate(lines):
                if line_idx != row.setting.setting_file_idx:
                    f.write(line)

            f.truncate()

        # shift down the settings in the rows
        for i in range(row_idx, len(self.setting_rows)):
            self.setting_rows[i].DownShiftIdx()

        # delete settings roiw from idx
        self.setting_rows[row_idx].deleteLater()
        del self.setting_rows[row_idx]

    def load_setting(self, setting: GUI_setting):

        print(
            f"Loading: {setting.name} type: {setting.setting_type} row idx: {setting.setting_row_idx} values: {setting.setting_vals_dict}")
        self.settings_model.set_setting(setting)
        self.settings_model.set_values(setting.setting_vals_dict)
        self.close()

    # setting or row number
    def update_setting(self, row_idx: int):

        # update the rest of the setting_rows idx and line numbers that came after idx in setting_rows array

        row = self.setting_rows[row_idx]

        setting = row.setting

        print(
            f"updating:{setting.name} row idx:{setting.setting_row_idx} file line:{setting.setting_file_idx}")

        with open(SETTINGS_FILE_PATH, "r+") as f:
            lines = f.readlines()

            f.seek(0)
            for line_idx, line in enumerate(lines):
                if line_idx != row.setting.setting_file_idx:
                    f.write(line)

                # write new values
                else:
                    new_settings = self.settings_model.get_inputs()
                    f.write(f"{setting.setting_type} {setting.name} " + str(new_settings).replace("'", "\"") + "\n")

            f.truncate()


