import sqlite3
from utils.global_cls import GlobalLanguage


class DatabaseConnection:
    def __init__(self, host: str):
        self.connection = None
        self.host = GlobalLanguage.file_path + host

    def __enter__(self):
        self.connection = sqlite3.connect(self.host)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            self.connection.close() # in case of errors
        else:
            self.connection.commit()
            self.connection.close()