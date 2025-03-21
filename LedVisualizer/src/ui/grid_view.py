from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
from src.ui.led_widget import LEDWidget

class GridView(QWidget):
    def __init__(self, num_rows=3, num_cols=5):
        super().__init__()

        self.num_rows = num_rows
        self.num_cols = num_cols
        self.leds = []

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.create_led_grid()

    def create_led_grid(self):
        """Crea la cuadrícula de LEDs."""
        for row in range(self.num_rows):
            led_row = []
            for col in range(self.num_cols):
                led = LEDWidget()
                self.layout.addWidget(led, row, col)
                led_row.append(led)
            self.leds.append(led_row)

    def update_leds(self, track, brightness):
        """Actualiza los LEDs según la señal recibida."""
        for row in self.leds:
            for led in row:
                led.set_brightness(brightness)

    def set_led_threshold(self, track, threshold):
        """Configura el umbral de los LEDs."""
        for row in self.leds:
            for led in row:
                led.set_threshold(threshold)
