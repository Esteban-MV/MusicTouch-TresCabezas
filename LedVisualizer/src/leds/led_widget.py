from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt

class LEDWidget(QWidget):
    def __init__(self, size=40, color=(0, 255, 0), parent=None):
        super().__init__(parent)
        self.size = size
        self.base_color = QColor(*color)  # Color base del LED
        self.brightness = 0  # Nivel de brillo (0-100%)

        self.setFixedSize(size, size)  # Tamaño fijo del LED

    def set_brightness(self, level):
        """Ajusta el brillo del LED (0-100%)."""
        self.brightness = max(0, min(100, level))  # Asegurar valores válidos
        self.update()  # Redibujar el LED

    def paintEvent(self, event):
        """Dibuja el LED con la intensidad actual."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Ajustar color según brillo
        brightness_factor = self.brightness / 100
        color = QColor(
            int(self.base_color.red() * brightness_factor),
            int(self.base_color.green() * brightness_factor),
            int(self.base_color.blue() * brightness_factor)
        )

        # Dibujar círculo
        painter.setBrush(color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, self.size, self.size)
