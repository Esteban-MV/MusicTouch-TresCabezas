from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt
from src.leds.led_widget import LEDWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LED Visualizer")
        self.setGeometry(100, 100, 800, 600)

        # Aplicar tema oscuro
        self.set_dark_theme()

        # Contenedor principal
        container = QWidget()
        layout = QVBoxLayout()

        # Etiqueta de información
        label = QLabel("Visualización de LEDs por pista", self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # Zona de LEDs (simulación de varias pistas)
        self.leds_container = QVBoxLayout()
        self.leds = []  # Lista de LEDs por pista

        # Crear LEDs para 3 pistas de prueba
        for _ in range(3):  
            row_layout = QHBoxLayout()
            track_leds = []
            for _ in range(5):  # 5 LEDs por pista
                led = LEDWidget()
                row_layout.addWidget(led)
                track_leds.append(led)
            self.leds.append(track_leds)
            self.leds_container.addLayout(row_layout)

        layout.addLayout(self.leds_container)
        container.setLayout(layout)
        self.setCentralWidget(container)

    def set_dark_theme(self):
        """Aplica un tema oscuro a la interfaz."""
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(25, 25, 25))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 220, 220))
        self.setPalette(palette)
