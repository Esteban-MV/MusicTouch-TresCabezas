# src/main.py

import sys
from PyQt6.QtWidgets import QApplication
from src.core.track_manager import TrackManager, Track
from src.ui.main_window import MainWindow
from src.osc.osc_listener import OSCListener
from src.midi.midi_handler import MIDIHandler
from src.custom.custom_socket_listener import CustomSocketListener

def main():
    app = QApplication(sys.argv)
    
    # Crear el TrackManager y pistas de ejemplo
    track_manager = TrackManager()
    for i in range(1, 4):
        new_track = Track(i)
        new_track.name = f"Pista {i}"
        track_manager.add_track(new_track)
    
    osc_listener = OSCListener(track_manager)
    osc_listener.start()
    midi_handler = MIDIHandler(track_manager)
    custom_listener = CustomSocketListener(track_manager)
    
    # Por defecto se inicia en OSC, pero el usuario puede cambiar el modo en la interfaz.
    window = MainWindow(track_manager, osc_listener, midi_handler, custom_listener)
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
