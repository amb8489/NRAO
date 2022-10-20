# todo general class for unit cell

class UnitCell:

    def __int__(self, line_model_type: str, cell_length: int, number_of_loads: int, load_lengths: [float],
                load_widths: [float], load_Xpositions: [float]):

        self.line_model_type = line_model_type
        self.cell_length = cell_length
        self.number_of_loads = number_of_loads
        self.load_lengths = load_lengths
        self.load_widths = load_widths
        self.load_positions = load_Xpositions




