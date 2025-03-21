import json
import os

class ConfigManager:
    CONFIG_FILE = os.path.join(os.path.dirname(__file__), "profiles.json")

    def __init__(self):
        self.configurations = self.load_profiles()

    def load_profiles(self):
        """Carga los perfiles desde el archivo JSON."""
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, "r") as file:
                return json.load(file)
        return {}

    def save_profiles(self):
        """Guarda los perfiles en el archivo JSON."""
        with open(self.CONFIG_FILE, "w") as file:
            json.dump(self.configurations, file, indent=4)

    def save_profile(self, profile_name, led_config):
        """
        Guarda una nueva configuración de LEDs bajo un nombre de perfil.
        :param profile_name: Nombre del perfil.
        :param led_config: Configuración de LEDs.
        """
        self.configurations[profile_name] = led_config
        self.save_profiles()

    def load_profile(self, profile_name):
        """
        Carga un perfil guardado.
        :param profile_name: Nombre del perfil.
        :return: Configuración de LEDs o None si no existe.
        """
        return self.configurations.get(profile_name, None)

    def delete_profile(self, profile_name):
        """Elimina un perfil guardado."""
        if profile_name in self.configurations:
            del self.configurations[profile_name]
            self.save_profiles()
