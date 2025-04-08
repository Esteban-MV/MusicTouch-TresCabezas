# src/midi/midi_handler.py

import threading
import time
import mido

class MIDIHandler:
    def __init__(self, track_manager, port_name=None):
        self.track_manager = track_manager
        self.port_name = port_name
        self.input_port = None
        self.running = False

    def start(self):
        try:
            if self.port_name:
                self.input_port = mido.open_input(self.port_name)
            else:
                self.input_port = mido.open_input()  # Abre el puerto MIDI predeterminado
            self.running = True
            self.thread = threading.Thread(target=self.listen)
            self.thread.daemon = True
            self.thread.start()
            print("MIDIHandler iniciado.")
        except Exception as e:
            print("Error abriendo el puerto MIDI:", e)

    def listen(self):
        while self.running:
            for message in self.input_port.iter_pending():
                self.handle_message(message)
            time.sleep(0.01)

    def handle_message(self, message):
        print("Mensaje MIDI recibido:", message)
        if message.type == 'control_change':
            try:
                track_id = message.control  # Se usa el número de control como ID de pista
                level = message.value / 127.0
                self.track_manager.update_track(track_id - 1, level)
            except Exception as e:
                print("Error procesando mensaje MIDI:", e)

    def stop(self):
        self.running = False
        if self.input_port:
            self.input_port.close()
            print("MIDIHandler detenido.")
