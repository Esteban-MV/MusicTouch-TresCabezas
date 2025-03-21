from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QSlider
from PyQt6.QtGui import QColor, QPainter, QBrush
from PyQt6.QtCore import Qt

class LEDWidget(QWidget):
    def __init__(self, brightness=0, threshold=50):
        super().__init__()
        self.brightness = brightness
        self.threshold = threshold

        # Interfaz de LED con Slider
        self.layout = QVBoxLayout(self)
        self.led_display = QLabel()
        self.led_display.setFixedSize(30, 30)
        self.layout.addWidget(self.led_display, alignment=Qt.AlignmentFlag.AlignCenter)

        # Slider de umbral
        self.threshold_slider = QSlider(Qt.Orientation.Vertical)
        self.threshold_slider.setRange(0, 100)
        self.threshold_slider.setValue(self.threshold)
        self.threshold_slider.valueChanged.connect(self.set_threshold)

        self.layout.addWidget(self.threshold_slider, alignment=Qt.AlignmentFlag.AlignCenter)

        self.update_led()

    def set_brightness(self, value):
        """Ajusta la luminosidad del LED según el valor de entrada."""
        self.brightness = max(0, min(value, 100))
        self.update_led()

    def set_threshold(self, value):
        """Configura el umbral mínimo de activación."""
        self.threshold = value
        self.update_led()

    def update_led(self):
        """Dibuja el LED con la luminosidad ajustada."""
        color = QColor(0, 255, 0)  # Verde
        if self.brightness >= self.threshold:
            color.setAlpha(int((self.brightness / 100) * 255))
        else:
            color.setAlpha(50)  # Transparente si está por debajo del umbral

        painter = QPainter(self.led_display)
        painter.setBrush(QBrush(color, Qt.BrushStyle.SolidPattern))
        painter.drawEllipse(0, 0, self.led_display.width(), self.led_display.height())
