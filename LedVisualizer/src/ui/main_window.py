from PyQt6.QtWidgets import QMainWindow, QPushButton, QStackedWidget
from src.ui.grid_view.py import GridView
from src.ui.led_widget import LEDWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LED Visualizer")
        self.setGeometry(100, 100, 800, 600)

        # Contenedor principal con vistas intercambiables
        self.view_container = QStackedWidget()
        self.list_view = QWidget()  # La vista en fila original
        self.grid_view = GridView()  # Nueva vista en cuadrícula

        self.view_container.addWidget(self.list_view)
        self.view_container.addWidget(self.grid_view)

        # Botón para cambiar vista
        self.toggle_view_btn = QPushButton("Cambiar Vista")
        self.toggle_view_btn.clicked.connect(self.toggle_view)

        # Agregar a la interfaz
        self.layout.addWidget(self.toggle_view_btn)
        self.layout.addWidget(self.view_container)

        self.setCentralWidget(self.view_container)

    def toggle_view(self):
        """Alterna entre la vista en fila y la vista en cuadrícula."""
        current_index = self.view_container.currentIndex()
        self.view_container.setCurrentIndex(1 if current_index == 0 else 0)
