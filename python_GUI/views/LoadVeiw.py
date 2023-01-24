import time

from PySide6.QtWidgets import QPushButton, QLabel, QGridLayout, QVBoxLayout, QWidget, QScrollArea


class LoadSettingsWindow(QScrollArea):
    """
    This "window" is alpha_plt QWidget. If it has no parent, it
    will appear as alpha_plt free-floating window as we want.
    """

    def __init__(self):
        super().__init__()

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
        time.sleep(1)
        self.close()