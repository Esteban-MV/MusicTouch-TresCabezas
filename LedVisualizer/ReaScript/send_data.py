# ReaScript: send_data.py
# Este script se encarga de enviar información de pista y niveles mediante UDP a LEDVisualizer.

import socket
import time
from reaper_python import *

UDP_IP = "127.0.0.1"
UDP_PORT = 9100

def send_udp_message(message):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message.encode('utf-8'), (UDP_IP, UDP_PORT))
    finally:
        sock.close()

def get_all_tracks_info():
    num_tracks = RPR_CountTracks(0)
    tracks = []
    for i in range(num_tracks):
        track = RPR_GetTrack(0, i)
        # Desempaquetamos tres valores y descartamos el tercero
        retval, track_name, _ = RPR_GetSetMediaTrackInfo_String(track, "P_NAME", "", False)
        # Para este ejemplo se asumen 4 LEDs por pista
        tracks.append((i + 1, track_name, 4))
    return tracks

def send_tracks_info():
    tracks = get_all_tracks_info()
    for t in tracks:
        track_id, name, num_leds = t
        message = f"TRACK_INFO|{track_id}|{name}|{num_leds}"
        send_udp_message(message)

def send_tracks_levels():
    num_tracks = RPR_CountTracks(0)
    for i in range(num_tracks):
        track = RPR_GetTrack(0, i)
        # Se obtiene el valor de D_PEAK, que representa el nivel de audio (ajusta según sea necesario)
        level = RPR_GetMediaTrackInfo_Value(track, "D_PEAK")
        message = f"TRACK_LEVEL|{i+1}|{level}"
        send_udp_message(message)

def main():
    # Envía la información de las pistas al inicio
    send_tracks_info()
    # Envía niveles de audio de forma periódica
    while True:
        send_tracks_levels()
        time.sleep(0.1)

main()
