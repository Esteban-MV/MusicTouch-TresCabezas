class Led:
    def __init__(self, led_id, threshold=50, response_type="RMS"):
        self.led_id = led_id
        self.threshold = threshold
        self.response_type = response_type
        self.intensity = 0  # Valor entre 0 y 100 para representar la luminosidad

    def update_intensity(self, audio_value):
        if audio_value > self.threshold:
            self.intensity = min(100, (audio_value / self.threshold) * 100)
        else:
            self.intensity = 0
