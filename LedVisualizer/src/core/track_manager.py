from src.core.led import Led

class Track:
    def __init__(self, track_id, name):
        self.track_id = track_id
        self.name = name
        self.leds = []

    def add_led(self):
        led_id = len(self.leds) + 1
        self.leds.append(Led(led_id))

    def remove_led(self, led_id):
        self.leds = [led for led in self.leds if led.led_id != led_id]

class TrackManager:
    def __init__(self):
        self.tracks = {}

    def add_track(self, track_id, name):
        self.tracks[track_id] = Track(track_id, name)

    def remove_track(self, track_id):
        if track_id in self.tracks:
            del self.tracks[track_id]
