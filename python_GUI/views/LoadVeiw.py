import time

from PySide6.QtWidgets import QPushButton, QLabel, QGridLayout, QVBoxLayout, QWidget, QScrollArea


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
        with open("/Users/aaron/PycharmProjects/NRAO/python_GUI/Setting/settings.txt", "r") as settings_file:
            for line in settings_file:
                settings.append(line)

        if not settings:
            self.layout().addWidget(QLabel("no setting have been saved"), 0, 0)

        for i, setting in enumerate(settings):
            name_label = QLabel(setting)
            load_button = QPushButton('Load', self)
            load_button.clicked.connect(self.Load)

            delete_button = QPushButton(f'Delete {i}', self)
            delete_button.clicked.connect(lambda: self.Delete(-1))

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

    def Load(self):
        # todo pass loaded inout back to main window and have them loaded into the UI
        print("loading ")

        inputs = {
            'SC': {'er': 0.0, 'h': 0.0, 'ts': 0.0, 'tg': 0.0, 't': 0.0, 'tc': 0.0, 'jc': 0.0, 'normal_resistivity': 0.0,
                   'tand': 0.0},
            'Dimensions': {'loads': [[0, 0], [0, 0]], 'Unit Cell Length []': 0.0, 'Central Line Width []': 0.0},
            'Frequency Range': {'Start Freq [GHZ]': 0.0, 'End Freq [GHZ]': 0.0, 'resolution': 0.0},
            'Gain': {'As0': 0.0, 'Ai0': 0.0, 'Ap0': 0.0, 'Pump Frequency [GHZ]': 0.0}}

        self.settings_model.set_values(inputs)
        time.sleep(1)
        self.close()
