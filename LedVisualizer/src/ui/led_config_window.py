from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QSlider, QPushButton

class LedConfigWindow(QDialog):
    def __init__(self, led):
        super().__init__()
        self.led = led

        self.setWindowTitle(f"Configuración LED {led.led_id}")

        layout = QVBoxLayout()

        self.threshold_label = QLabel(f"Umbral: {self.led.threshold}")
        self.threshold_slider = QSlider()
        self.threshold_slider.setMinimum(0)
        self.threshold_slider.setMaximum(100)
        self.threshold_slider.setValue(self.led.threshold)
        self.threshold_slider.valueChanged.connect(self.update_threshold)

        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.save_config)

        layout.addWidget(self.threshold_label)
        layout.addWidget(self.threshold_slider)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def update_threshold(self, value):
        self.threshold_label.setText(f"Umbral: {value}")

    def save_config(self):
        self.led.threshold = self.threshold_slider.value()
        self.accept()
