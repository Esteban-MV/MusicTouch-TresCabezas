# src/custom/custom_socket_listener.py

import socket
import threading

class CustomSocketListener:
    def __init__(self, track_manager, ip="127.0.0.1", port=9100):
        self.track_manager = track_manager
        self.ip = ip
        self.port = port
        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.listen)
        self.thread.daemon = True
        self.thread.start()
        print(f"CustomSocketListener iniciado en {self.ip}:{self.port}")

    def listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.ip, self.port))
        while self.running:
            try:
                data, addr = sock.recvfrom(1024)
                message = data.decode("utf-8")
                print("Mensaje Custom recibido:", message)
                self.process_message(message)
            except Exception as e:
                print("Error en CustomSocketListener:", e)
        sock.close()

    def process_message(self, message):
        parts = message.split("|")
        if parts[0] == "TRACK_INFO":
            try:
                track_id = int(parts[1])
                track_name = parts[2]
                num_leds = int(parts[3])
                self.track_manager.sync_track(track_id, track_name, num_leds)
            except Exception as e:
                print("Error procesando TRACK_INFO:", e)
        elif parts[0] == "TRACK_LEVEL":
            try:
                track_id = int(parts[1])
                level = float(parts[2])
                self.track_manager.update_track(track_id - 1, level)
            except Exception as e:
                print("Error procesando TRACK_LEVEL:", e)
        else:
            print("Mensaje desconocido:", message)

    def stop(self):
        self.running = False
