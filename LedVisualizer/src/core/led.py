# src/core/led.py

class LED:
    def __init__(self, threshold=0.5, intensity=0.3, response="RMS"):
        self.threshold = threshold
        self.intensity = intensity
        self.response = response  # "RMS" o "Picos"
        self.recent_levels = []  # Historial para calibración automática

    def update_intensity(self, level):
        """Actualiza la intensidad y realiza calibración si es necesario."""
        self.recent_levels.append(level)
        if len(self.recent_levels) > 10:
            self.recent_levels.pop(0)
        if self.response.upper() == "RMS":
            avg = sum(self.recent_levels) / len(self.recent_levels)
            self.intensity = avg
        elif self.response.upper() == "PICOS":
            self.intensity = max(self.recent_levels)
        if self.intensity > self.threshold:
            self.calibrate()

    def calibrate(self):
        """Ajusta el threshold en función del promedio de los niveles."""
        if self.recent_levels:
            avg = sum(self.recent_levels) / len(self.recent_levels)
            self.threshold = avg * 0.9
