import mysql.connector
from config.config_loader import ConfigLoader

class BaseDao:
    def __init__(self):
        self.config = ConfigLoader().load_config()

    def get_connection(self):
        try:
            return mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
            print(f"Database connection error: {err}")
            raise