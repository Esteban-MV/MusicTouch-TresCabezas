from pythonosc import dispatcher, osc_server
import threading

class OSCListener:
    def __init__(self, track_manager, ip="127.0.0.1", port=9000):
        self.track_manager = track_manager
        self.ip = ip
        self.port = port
        self.server_thread = None

    def start_listener(self):
        disp = dispatcher.Dispatcher()
        disp.map("/track/*", self.process_osc_message)

        self.server_thread = threading.Thread(target=self.run_server, args=(disp,))
        self.server_thread.daemon = True
        self.server_thread.start()

    def run_server(self, disp):
        server = osc_server.ThreadingOSCUDPServer((self.ip, self.port), disp)
        server.serve_forever()

    def process_osc_message(self, address, *args):
        try:
            track_id = int(address.split("/")[2])  # Extrae el ID de la pista del mensaje OSC
            audio_value = args[0]  # Nivel de audio recibido

            if track_id in self.track_manager.tracks:
                for led in self.track_manager.tracks[track_id].leds:
                    led.update_intensity(audio_value)
        except Exception as e:
            print(f"Error procesando OSC: {e}")
