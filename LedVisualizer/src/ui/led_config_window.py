# src/ui/led_config_window.py

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QComboBox
from PyQt6.QtCore import Qt

class LEDConfigWindow(QDialog):
    def __init__(self, led, parent=None):
        super().__init__(parent)
        self.led = led
        self.setWindowTitle("Configurar LED")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        # Campo para el threshold
        self.threshold_edit = QLineEdit(str(self.led.threshold))
        layout.addWidget(QLabel("Threshold:"))
        layout.addWidget(self.threshold_edit)
        
        # Menú desplegable para seleccionar el parámetro de reacción
        layout.addWidget(QLabel("Parámetro de reacción:"))
        self.response_combo = QComboBox()
        self.response_combo.addItems(["RMS", "Picos"])
        index = self.response_combo.findText(self.led.response, Qt.MatchFlag.MatchFixedString)
        if index >= 0:
            self.response_combo.setCurrentIndex(index)
        layout.addWidget(self.response_combo)
        
        # Botones Guardar/Cancelar
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Guardar")
        cancel_btn = QPushButton("Cancelar")
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        save_btn.clicked.connect(self.save_config)
        cancel_btn.clicked.connect(self.reject)
        
        self.setLayout(layout)

    def save_config(self):
        try:
            self.led.threshold = float(self.threshold_edit.text())
        except ValueError:
            pass  # Se puede agregar manejo de error
        self.led.response = self.response_combo.currentText()
        self.accept()
