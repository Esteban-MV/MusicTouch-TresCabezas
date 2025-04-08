# src/core/track_manager.py

from .led import LED

class Track:
    def __init__(self, track_number):
        self.track_number = track_number
        self.name = f"Pista {track_number}"
        # Se crean 4 LEDs por defecto
        self.leds = [LED(threshold=0.5, intensity=0.3) for _ in range(4)]

    def update_leds(self, level):
        """Actualiza la intensidad de todos los LEDs de la pista."""
        for led in self.leds:
            led.update_intensity(level)

class TrackManager:
    def __init__(self):
        self.tracks = []

    def add_track(self, track):
        self.tracks.append(track)

    def remove_track(self, track):
        if track in self.tracks:
            self.tracks.remove(track)

    def update_track(self, track_index, level):
        """Actualiza la pista en la posición track_index con el nivel recibido."""
        if 0 <= track_index < len(self.tracks):
            self.tracks[track_index].update_leds(level)

    def load_configuration(self, config):
        """Carga la configuración (perfil) desde un diccionario."""
        self.tracks = []
        for track_data in config.get("tracks", []):
            track = Track(track_data.get("track_number", 0))
            track.name = track_data.get("name", f"Pista {track.track_number}")
            track.leds = []
            for led_data in track_data.get("leds", []):
                from .led import LED  # Importación local para evitar dependencias circulares
                led = LED(
                    threshold=led_data.get("threshold", 0.5),
                    intensity=led_data.get("intensity", 0.3),
                    response=led_data.get("response", "RMS")
                )
                track.leds.append(led)
            self.tracks.append(track)

    def export_configuration(self):
        """Exporta la configuración actual a un diccionario."""
        config = {"tracks": []}
        for track in self.tracks:
            track_conf = {"track_number": track.track_number, "name": track.name, "leds": []}
            for led in track.leds:
                track_conf["leds"].append({
                    "threshold": led.threshold,
                    "intensity": led.intensity,
                    "response": led.response
                })
            config["tracks"].append(track_conf)
        return config

    def sync_track(self, track_id, track_name, num_leds):
        """
        Sincroniza o crea/actualiza una pista a partir de la información recibida (por OSC).
        track_id: ID numérico (de Reaper)
        track_name: Nombre de la pista
        num_leds: Número deseado de LEDs
        """
        found = False
        for track in self.tracks:
            if track.track_number == track_id:
                track.name = track_name
                current_leds = len(track.leds)
                if current_leds < num_leds:
                    for _ in range(num_leds - current_leds):
                        track.leds.append(LED(threshold=0.5, intensity=0.3))
                elif current_leds > num_leds:
                    track.leds = track.leds[:num_leds]
                found = True
                break
        if not found:
            new_track = Track(track_id)
            new_track.name = track_name
            new_track.leds = [LED(threshold=0.5, intensity=0.3) for _ in range(num_leds)]
            self.add_track(new_track)

    def remove_track_by_id(self, track_id):
        for track in self.tracks:
            if track.track_number == track_id:
                self.remove_track(track)
                break
