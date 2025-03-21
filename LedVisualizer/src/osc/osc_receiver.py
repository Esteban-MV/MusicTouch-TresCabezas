from python-osc import osc_server, dispatcher
import threading

class OSCReceiver:
    def __init__(self, ip="127.0.0.1", port=8000, callback=None):
        self.ip = ip
        self.port = port
        self.callback = callback

    def start(self):
        """Inicia la recepción de mensajes OSC en un hilo separado."""
        thread = threading.Thread(target=self.run_server, daemon=True)
        thread.start()

    def run_server(self):
        """Ejecuta el servidor OSC y recibe datos de REAPER."""
        dispatch = dispatcher.Dispatcher()
        dispatch.map("/track/*/level", self.handle_osc_message)

        server = osc_server.ThreadingOSCUDPServer((self.ip, self.port), dispatch)
        print(f"OSC Server iniciado en {self.ip}:{self.port}")
        server.serve_forever()

    def handle_osc_message(self, address, *args):
        """Procesa los mensajes OSC y actualiza los LEDs."""
        track = address.split("/")[2]
        level = float(args[0])  # Nivel de audio recibido
        if self.callback:
            self.callback(track, level)
