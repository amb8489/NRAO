class GUI_setting():

    def __init__(self, name: str, setting_type: str, setting_vals: dict, idx: int, setting_file_line_number: int):
        self.setting_file_idx = setting_file_line_number
        self.name = name
        self.setting_type = setting_type
        self.setting_vals_dict = setting_vals
        self.setting_row_idx = idx



