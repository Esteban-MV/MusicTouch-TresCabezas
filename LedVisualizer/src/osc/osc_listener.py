# src/osc/osc_listener.py

import threading
import time
from pythonosc import dispatcher, osc_server

class OSCListener:
    def __init__(self, track_manager, ip='127.0.0.1', port=9000):
        self.track_manager = track_manager
        self.ip = ip
        self.port = port
        self.dispatcher = dispatcher.Dispatcher()
        # Mapeo de mensajes OSC
        self.dispatcher.map("/reaper/track/*/info", self.handle_track_info)
        self.dispatcher.map("/reaper/track/*/level", self.handle_track_level)
        self.dispatcher.map("/reaper/track/*/remove", self.handle_track_remove)
        # Atributos de estado para conexión y recepción
        self.connected = False
        self.last_msg_time = None
        self.server = None
        self.thread = None

    def _update_status(self):
        self.connected = True
        self.last_msg_time = time.time()

    def handle_track_info(self, address, *args):
        try:
            self._update_status()
            parts = address.split('/')
            track_id = int(parts[3])
            track_name = args[0] if len(args) > 0 else f"Pista {track_id}"
            num_leds = int(args[1]) if len(args) > 1 else 4
            self.track_manager.sync_track(track_id, track_name, num_leds)
        except Exception as e:
            print("Error en handle_track_info:", e)

    def handle_track_level(self, address, *args):
        try:
            self._update_status()
            parts = address.split('/')
            track_id = int(parts[3])
            level = float(args[0]) if args else 0.0
            self.track_manager.update_track(track_id - 1, level)
        except Exception as e:
            print("Error en handle_track_level:", e)

    def handle_track_remove(self, address, *args):
        try:
            self._update_status()
            parts = address.split('/')
            track_id = int(parts[3])
            self.track_manager.remove_track_by_id(track_id)
        except Exception as e:
            print("Error en handle_track_remove:", e)

    def start(self):
        self.server = osc_server.ThreadingOSCUDPServer((self.ip, self.port), self.dispatcher)
        print(f"Servidor OSC corriendo en {self.server.server_address}")
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            print("Servidor OSC detenido.")
