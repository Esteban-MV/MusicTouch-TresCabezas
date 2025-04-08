# src/main.py

import sys
from PyQt6.QtWidgets import QApplication
from src.core.track_manager import TrackManager, Track
from src.ui.main_window import MainWindow
from src.osc.osc_listener import OSCListener

def main():
    app = QApplication(sys.argv)
    
    # Crear el TrackManager y añadir pistas de ejemplo
    track_manager = TrackManager()
    for i in range(1, 4):
        new_track = Track(i)
        new_track.name = f"Pista {i}"
        track_manager.add_track(new_track)
    
    # Iniciar el receptor OSC (escuchando en localhost:9000)
    osc_listener = OSCListener(track_manager)
    osc_listener.start()
    
    # Mostrar la ventana principal, pasando la referencia al OSCListener
    main_window = MainWindow(track_manager, osc_listener)
    main_window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
