from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QListWidget, QHBoxLayout
from src.ui.led_config_window import LedConfigWindow
from src.core.track_manager import TrackManager
from src.utils.profile_manager import ProfileManager
from src.osc.osc_listener import OSCListener

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Control de LEDs - REAPER")
        self.setGeometry(100, 100, 700, 500)

        self.track_manager = TrackManager()
        self.profile_manager = ProfileManager(self.track_manager)
        self.osc_listener = OSCListener(self.track_manager)
        self.osc_listener.start_listener()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.track_list = QListWidget()
        self.track_list.currentItemChanged.connect(self.update_led_list)

        self.led_list = QListWidget()

        self.add_track_button = QPushButton("Agregar Pista")
        self.add_track_button.clicked.connect(self.add_track)

        self.remove_track_button = QPushButton("Eliminar Pista")
        self.remove_track_button.clicked.connect(self.remove_track)

        self.add_led_button = QPushButton("Agregar LED")
        self.add_led_button.clicked.connect(self.add_led)

        self.config_led_button = QPushButton("Configurar LED")
        self.config_led_button.clicked.connect(self.open_led_config)

        self.save_profile_button = QPushButton("Guardar Perfil")
        self.save_profile_button.clicked.connect(self.save_profile)

        self.load_profile_button = QPushButton("Cargar Perfil")
        self.load_profile_button.clicked.connect(self.load_profile)

        track_layout = QHBoxLayout()
        track_layout.addWidget(self.track_list)
        track_layout.addWidget(self.add_track_button)
        track_layout.addWidget(self.remove_track_button)

        led_layout = QHBoxLayout()
        led_layout.addWidget(self.led_list)
        led_layout.addWidget(self.add_led_button)
        led_layout.addWidget(self.config_led_button)

        layout.addLayout(track_layout)
        layout.addLayout(led_layout)
        layout.addWidget(self.save_profile_button)
        layout.addWidget(self.load_profile_button)

        self.central_widget.setLayout(layout)

    def add_track(self):
        track_id = len(self.track_manager.tracks) + 1
        self.track_manager.add_track(track_id, f"Pista {track_id}")
        self.track_list.addItem(f"Pista {track_id}")

    def remove_track(self):
        selected_item = self.track_list.currentItem()
        if selected_item:
            track_id = int(selected_item.text().split()[-1])
            self.track_manager.remove_track(track_id)
            self.track_list.takeItem(self.track_list.row(selected_item))

    def add_led(self):
        selected_item = self.track_list.currentItem()
        if selected_item:
            track_id = int(selected_item.text().split()[-1])
            self.track_manager.tracks[track_id].add_led()
            self.update_led_list()

    def update_led_list(self):
        self.led_list.clear()
        selected_item = self.track_list.currentItem()
        if selected_item:
            track_id = int(selected_item.text().split()[-1])
            leds = self.track_manager.tracks[track_id].leds
            for led in leds:
                self.led_list.addItem(f"LED {led.led_id}")

    def open_led_config(self):
        selected_item = self.led_list.currentItem()
        if selected_item:
            led_id = int(selected_item.text().split()[-1])
            track_id = int(self.track_list.currentItem().text().split()[-1])

            led = self.track_manager.tracks[track_id].get_led(led_id)
            config_window = LedConfigWindow(led)
            config_window.exec()

    def save_profile(self):
        self.profile_manager.save_profile()

    def load_profile(self):
        self.profile_manager.load_profile()
        self.update_led_list()
