# src/core/profile_manager.py

import os
import json

class ProfileManager:
    def __init__(self, profiles_dir="profiles"):
        self.profiles_dir = profiles_dir
        if not os.path.exists(self.profiles_dir):
            os.makedirs(self.profiles_dir)
    
    def list_profiles(self):
        """Devuelve una lista de nombres de perfiles (sin extensión)."""
        files = [f[:-5] for f in os.listdir(self.profiles_dir) if f.endswith('.json')]
        return files
    
    def save_profile(self, config, profile_name):
        """Guarda la configuración en un archivo JSON con el nombre dado."""
        file_name = profile_name + ".json"
        with open(os.path.join(self.profiles_dir, file_name), "w") as f:
            json.dump(config, f, indent=4)
    
    def load_profile(self, profile_name):
        """Carga la configuración de un perfil dado."""
        file_name = profile_name + ".json"
        with open(os.path.join(self.profiles_dir, file_name), "r") as f:
            return json.load(f)
    
    def delete_profile(self, profile_name):
        """Elimina el perfil (archivo JSON) con el nombre dado."""
        file_name = profile_name + ".json"
        path = os.path.join(self.profiles_dir, file_name)
        if os.path.exists(path):
            os.remove(path)
