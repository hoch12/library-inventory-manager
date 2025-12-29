import mysql.connector
from config.config_loader import ConfigLoader

class BaseDao:
    def __init__(self):
        self.config = ConfigLoader().load_config()

    def get_connection(self):
        try:
            connection = mysql.connector.connect(**self.config)
            return connection
        except mysql.connector.Error as err:
            print(f"Chyba připojení k DB: {err}")
            raise