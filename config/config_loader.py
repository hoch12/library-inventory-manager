import json
import os


class ConfigLoader:
    def __init__(self, config_path="config/db_config.json"):
        self.config_path = config_path

    def load_config(self):
        # Ověření existence souboru
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Konfigurační soubor nenalezen: {self.config_path}")

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            raise ValueError("Neplatný formát JSON v konfiguračním souboru.")