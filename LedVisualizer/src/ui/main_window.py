# src/ui/main_window.py

import sys
import time
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QInputDialog, QMessageBox, QComboBox
)
from PyQt6.QtGui import QPainter, QBrush, QColor
from PyQt6.QtCore import Qt, QTimer

from src.core.track_manager import Track, TrackManager
from src.core.profile_manager import ProfileManager
from src.ui.led_config_window import LEDConfigWindow

class LEDWidget(QWidget):
    def __init__(self, led, parent=None):
        super().__init__(parent)
        self.led = led
        self.setMinimumSize(30, 30)
        self.setMaximumSize(30, 30)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        config_window = LEDConfigWindow(self.led, self)
        config_window.exec()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect().adjusted(2, 2, -2, -2)
        color = QColor(0, 255, 0)
        color.setAlphaF(self.led.intensity)
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(rect)
        painter.end()

class LEDContainer(QWidget):
    def __init__(self, led, remove_callback=None, parent=None):
        super().__init__(parent)
        self.led = led
        self.remove_callback = remove_callback
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        self.led_widget = LEDWidget(self.led)
        self.remove_btn = QPushButton("x")
        self.remove_btn.setFixedSize(15, 15)
        self.remove_btn.setStyleSheet("background-color: red; color: white; font-size: 10px;")
        self.remove_btn.clicked.connect(self.handle_remove)
        layout.addWidget(self.led_widget)
        layout.addWidget(self.remove_btn)
        self.setLayout(layout)

    def handle_remove(self):
        if self.remove_callback:
            self.remove_callback(self)

class TrackRow(QWidget):
    def __init__(self, track, remove_callback=None, parent=None):
        super().__init__(parent)
        self.track = track
        self.remove_callback = remove_callback
        self.led_containers = []
        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(10)
        self.track_label = QLabel(f"{self.track.name}")
        self.track_label.setStyleSheet("color: white; font-weight: bold;")
        self.layout.addWidget(self.track_label, 1)
        self.led_area = QHBoxLayout()
        for led in self.track.leds:
            container = LEDContainer(led, remove_callback=self.remove_led)
            self.led_containers.append(container)
            self.led_area.addWidget(container)
        self.add_led_btn = QPushButton("+")
        self.add_led_btn.setFixedSize(30, 30)
        self.add_led_btn.setStyleSheet("background-color: #444; color: white; border: none;")
        self.add_led_btn.clicked.connect(self.add_led)
        self.led_area.addWidget(self.add_led_btn)
        self.layout.addLayout(self.led_area, 3)
        self.remove_track_btn = QPushButton("Eliminar Pista")
        self.remove_track_btn.setFixedSize(100, 30)
        self.remove_track_btn.setStyleSheet("background-color: #bb0000; color: white;")
        self.remove_track_btn.clicked.connect(self.handle_remove_track)
        self.layout.addWidget(self.remove_track_btn)
        self.setLayout(self.layout)

    def add_led(self):
        from src.core.led import LED
        new_led = LED(threshold=0.5, intensity=0.3)
        self.track.leds.append(new_led)
        container = LEDContainer(new_led, remove_callback=self.remove_led)
        self.led_containers.append(container)
        self.led_area.insertWidget(self.led_area.count()-1, container)

    def remove_led(self, container):
        if container in self.led_containers:
            index = self.led_containers.index(container)
            self.led_containers.remove(container)
            self.track.leds.pop(index)
            container.setParent(None)
            container.deleteLater()

    def handle_remove_track(self):
        if self.remove_callback:
            self.remove_callback(self)

    def refresh(self):
        for container in self.led_containers:
            container.led_widget.update()

class MainWindow(QMainWindow):
    def __init__(self, track_manager, osc_listener, midi_handler):
        super().__init__()
        self.setWindowTitle("LedVisualizer")
        self.resize(800, 600)
        self.track_manager = track_manager
        self.osc_listener = osc_listener
        self.midi_handler = midi_handler
        self.profile_manager = ProfileManager()
        self.active_input = "OSC"  # Valor predeterminado
        self.setStyleSheet("background-color: #1e1e1e;")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.top_bar = QHBoxLayout()
        self.add_track_btn = QPushButton("Agregar Pista")
        self.add_track_btn.setStyleSheet("background-color: #444; color: white; padding: 5px 10px;")
        self.add_track_btn.clicked.connect(self.add_track)
        self.top_bar.addWidget(self.add_track_btn)
        self.top_bar.addStretch()
        self.select_profile_btn = QPushButton("Seleccionar Perfil")
        self.save_profile_btn = QPushButton("Guardar Perfil")
        self.delete_profile_btn = QPushButton("Eliminar Perfil")
        self.connection_info_btn = QPushButton("Información Reaper")
        button_style = """
            QPushButton {
                background-color: #444;
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """
        self.select_profile_btn.setStyleSheet(button_style)
        self.save_profile_btn.setStyleSheet(button_style)
        self.delete_profile_btn.setStyleSheet(button_style)
        self.connection_info_btn.setStyleSheet(button_style)
        self.select_profile_btn.clicked.connect(self.select_profile)
        self.save_profile_btn.clicked.connect(self.save_profile)
        self.delete_profile_btn.clicked.connect(self.delete_profile)
        self.connection_info_btn.clicked.connect(self.show_connection_info)
        # Se agrega QComboBox para seleccionar el modo de entrada
        self.input_mode_combo = QComboBox()
        self.input_mode_combo.addItems(["OSC", "MIDI"])
        self.input_mode_combo.currentTextChanged.connect(self.switch_input_mode)
        self.top_bar.addWidget(QLabel("Modo de entrada:"))
        self.top_bar.addWidget(self.input_mode_combo)
        self.top_bar.addWidget(self.select_profile_btn)
        self.top_bar.addWidget(self.save_profile_btn)
        self.top_bar.addWidget(self.delete_profile_btn)
        self.top_bar.addWidget(self.connection_info_btn)
        self.main_layout.addLayout(self.top_bar)
        self.status_layout = QHBoxLayout()
        self.reaper_connected_label = QLabel("Conectado a Reaper: No")
        self.reaper_listening_label = QLabel("Escuchando Reaper: No")
        self.reaper_connected_label.setStyleSheet("color: white;")
        self.reaper_listening_label.setStyleSheet("color: white;")
        self.status_layout.addWidget(self.reaper_connected_label)
        self.status_layout.addWidget(self.reaper_listening_label)
        self.main_layout.addLayout(self.status_layout)
        self.header_frame = QFrame()
        self.header_frame.setStyleSheet("background-color: #2e2e2e;")
        self.header_layout = QHBoxLayout(self.header_frame)
        self.header_layout.setContentsMargins(10, 5, 10, 5)
        self.header_layout.setSpacing(10)
        header_pistas = QLabel("Pistas")
        header_pistas.setStyleSheet("color: white; font-weight: bold;")
        header_leds = QLabel("LEDs")
        header_leds.setStyleSheet("color: white; font-weight: bold;")
        self.header_layout.addWidget(header_pistas, 1)
        self.header_layout.addWidget(header_leds, 3)
        self.main_layout.addWidget(self.header_frame)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.track_container = QWidget()
        self.track_layout = QVBoxLayout(self.track_container)
        self.track_layout.setSpacing(5)
        self.track_layout.setContentsMargins(0, 0, 0, 0)
        self.track_rows = []
        for track in self.track_manager.tracks:
            self.create_track_row(track)
        self.scroll_area.setWidget(self.track_container)
        self.main_layout.addWidget(self.scroll_area)
        self.legend_frame = QFrame()
        self.legend_frame.setStyleSheet("background-color: #2e2e2e;")
        self.legend_layout = QHBoxLayout(self.legend_frame)
        self.legend_layout.setContentsMargins(10, 5, 10, 5)
        self.legend_layout.setSpacing(20)
        dummy_led = type('Dummy', (), {'intensity': 0.8})()
        led_icon = LEDWidget(dummy_led)
        led_label = QLabel("LED: Visualización de intensidad")
        led_label.setStyleSheet("color: white;")
        led_legend = QHBoxLayout()
        led_legend.addWidget(led_icon)
        led_legend.addWidget(led_label)
        config_btn = QPushButton("⚙")
        config_btn.setFixedSize(30, 30)
        config_btn.setStyleSheet("background-color: #444; color: white; border: none;")
        config_label = QLabel("Configurar LED")
        config_label.setStyleSheet("color: white;")
        config_legend = QHBoxLayout()
        config_legend.addWidget(config_btn)
        config_legend.addWidget(config_label)
        add_led_btn = QPushButton("+")
        add_led_btn.setFixedSize(30, 30)
        add_led_btn.setStyleSheet("background-color: #444; color: white; border: none;")
        add_label = QLabel("Agregar LED")
        add_label.setStyleSheet("color: white;")
        add_legend = QHBoxLayout()
        add_legend.addWidget(add_led_btn)
        add_legend.addWidget(add_label)
        self.legend_layout.addLayout(led_legend)
        self.legend_layout.addLayout(config_legend)
        self.legend_layout.addLayout(add_legend)
        self.main_layout.addWidget(self.legend_frame)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_ui)
        self.timer.start(100)

    def switch_input_mode(self, mode):
        self.active_input = mode
        if mode == "OSC":
            if self.midi_handler.running:
                self.midi_handler.stop()
            if not self.osc_listener.thread.is_alive():
                self.osc_listener.start()
        elif mode == "MIDI":
            if self.osc_listener:
                self.osc_listener.stop()
            if not self.midi_handler.running:
                self.midi_handler.start()

    def create_track_row(self, track):
        row = TrackRow(track, remove_callback=self.remove_track_row)
        self.track_rows.append(row)
        self.track_layout.addWidget(row)

    def add_track(self):
        new_track_number = len(self.track_manager.tracks) + 1
        from src.core.track_manager import Track
        new_track = Track(new_track_number)
        new_track.name = f"Pista {new_track_number}"
        self.track_manager.add_track(new_track)
        self.create_track_row(new_track)

    def remove_track_row(self, row):
        ret = QMessageBox.question(self, "Eliminar pista", f"¿Desea eliminar {row.track.name}?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if ret == QMessageBox.StandardButton.Yes:
            if row in self.track_rows:
                self.track_rows.remove(row)
                self.track_layout.removeWidget(row)
                row.setParent(None)
                row.deleteLater()
                self.track_manager.remove_track(row.track)
                self.refresh_track_numbers()

    def refresh_track_numbers(self):
        for idx, row in enumerate(self.track_rows, start=1):
            row.track.track_number = idx
            row.track.name = f"Pista {idx}"
            row.track_label.setText(row.track.name)

    def save_profile(self):
        config = self.track_manager.export_configuration()
        name, ok = QInputDialog.getText(self, "Guardar Perfil", "Ingrese el nombre del perfil:")
        if ok and name:
            self.profile_manager.save_profile(config, name)
            QMessageBox.information(self, "Perfil guardado", f"Perfil '{name}' guardado exitosamente.")

    def select_profile(self):
        profiles = self.profile_manager.list_profiles()
        if not profiles:
            QMessageBox.warning(self, "Sin perfiles", "No hay perfiles guardados.")
            return
        profile, ok = QInputDialog.getItem(self, "Seleccionar Perfil", "Perfiles:", profiles, 0, False)
        if ok and profile:
            config = self.profile_manager.load_profile(profile)
            self.track_manager.load_configuration(config)
            for row in self.track_rows:
                self.track_layout.removeWidget(row)
                row.setParent(None)
                row.deleteLater()
            self.track_rows = []
            for track in self.track_manager.tracks:
                self.create_track_row(track)
            self.refresh_track_numbers()
            QMessageBox.information(self, "Perfil cargado", f"Perfil '{profile}' cargado exitosamente.")

    def delete_profile(self):
        profiles = self.profile_manager.list_profiles()
        if not profiles:
            QMessageBox.warning(self, "Sin perfiles", "No hay perfiles guardados para eliminar.")
            return
        profile, ok = QInputDialog.getItem(self, "Eliminar Perfil", "Seleccione el perfil a eliminar:", profiles, 0, False)
        if ok and profile:
            ret = QMessageBox.question(self, "Eliminar Perfil", f"¿Está seguro de eliminar el perfil '{profile}'?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if ret == QMessageBox.StandardButton.Yes:
                self.profile_manager.delete_profile(profile)
                QMessageBox.information(self, "Perfil eliminado", f"Perfil '{profile}' eliminado exitosamente.")

    def show_connection_info(self):
        info_text = (
            "Para conectar LEDVisualizer con Reaper, configure Reaper de la siguiente manera:\n\n"
            "1. IP y Puerto:\n"
            "   - IP: 127.0.0.1\n"
            "   - Puerto: 9000\n\n"
            "2. Mensajes OSC (ejemplos):\n"
            "   - Información de pista:\n"
            "     /reaper/track/<track_id>/info \"Nombre Pista\" <num_leds>\n\n"
            "   - Nivel de audio:\n"
            "     /reaper/track/<track_id>/level <nivel>\n\n"
            "   - Eliminación de pista (opcional):\n"
            "     /reaper/track/<track_id>/remove\n\n"
            "Para la entrada MIDI, LEDVisualizer leerá mensajes de Control Change donde:\n"
            "   - El número de control se usará como ID de pista\n"
            "   - El valor (0-127) se convertirá en un nivel (0.0 a 1.0)\n\n"
            "Seleccione el modo de entrada (OSC o MIDI) en la interfaz para activar el receptor deseado."
        )
        QMessageBox.information(self, "Información de Conexión a Reaper", info_text)

    def refresh_ui(self):
        for row in self.track_rows:
            row.refresh()
        if self.active_input == "OSC":
            if self.osc_listener.connected:
                self.reaper_connected_label.setText("Conectado a Reaper: Sí")
            else:
                self.reaper_connected_label.setText("Conectado a Reaper: No")
            if self.osc_listener.last_msg_time and (time.time() - self.osc_listener.last_msg_time) < 5:
                self.reaper_listening_label.setText("Escuchando Reaper: Sí")
            else:
                self.reaper_listening_label.setText("Escuchando Reaper: No")
        elif self.active_input == "MIDI":
            # Para MIDI, podríamos definir indicadores basados en mensajes recibidos, aquí simplificamos:
            if self.midi_handler.running:
                self.reaper_connected_label.setText("Conectado a Reaper (MIDI): Sí")
                self.reaper_listening_label.setText("Escuchando Reaper (MIDI): Sí")
            else:
                self.reaper_connected_label.setText("Conectado a Reaper (MIDI): No")
                self.reaper_listening_label.setText("Escuchando Reaper (MIDI): No")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    from src.core.track_manager import TrackManager, Track
    tm = TrackManager()
    for i in range(1, 4):
        new_track = Track(i)
        new_track.name = f"Pista {i}"
        tm.add_track(new_track)
    from src.osc.osc_listener import OSCListener
    osc_listener = OSCListener(tm)
    osc_listener.start()
    from src.midi.midi_handler import MIDIHandler
    midi_handler = MIDIHandler(tm)
    # Por defecto iniciamos en OSC; el usuario podrá cambiar a MIDI desde el combo
    window = MainWindow(tm, osc_listener, midi_handler)
    window.show()
    sys.exit(app.exec())
