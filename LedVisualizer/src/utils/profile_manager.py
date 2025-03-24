import json

class ProfileManager:
    def __init__(self, track_manager):
        self.track_manager = track_manager

    def save_profile(self, filename="profile.json"):
        data = {tid: {"name": track.name, "leds": len(track.leds)} for tid, track in self.track_manager.tracks.items()}
        with open(filename, "w") as file:
            json.dump(data, file)

    def load_profile(self, filename="profile.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                self.track_manager.tracks = {int(tid): Track(int(tid), info["name"]) for tid, info in data.items()}
        except FileNotFoundError:
            pass
