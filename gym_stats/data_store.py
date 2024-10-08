import sqlite3
import os

class DataStore:
    def __init__(self, db_name, table_name, db_path=None):
        
        if db_path is not None:
            self.db_path = db_path
        else:
            self.db_path = "data/"

        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)

        self.db_name = db_name
        self.table_name = table_name
        self.conn = sqlite3.connect(os.path.join(self.db_path, db_name))
        self.cursor = self.conn.cursor()
        self.initialize_db()

    def initialize_db(self):
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT,
            recognized_number INTEGER DEFAULT 0,
            timestamp DATETIME,
            year INTEGER,
            month INTEGER,
            day_of_month INTEGER,
            week INTEGER,
            weekday INTEGER CHECK(weekday BETWEEN 0 AND 6),
            hour INTEGER
        );''')
        self.conn.commit()
    
    def add_data(self, image_path, recognized_number, timestamp, year: int, month: int, day: int, week: int, weekday: int, hour: int):
        self.cursor.execute(f"INSERT INTO {self.table_name} (image_path, recognized_number, timestamp, year, month, day_of_month, week, weekday, hour) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (image_path, recognized_number, timestamp, year, month, day, week, weekday, hour))
        self.conn.commit()

    def get_custom_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_data(self, since=None):
        if since:
            query = f"SELECT * FROM {self.table_name} WHERE timestamp >= ?"
            self.cursor.execute(query, (since,))
        else:
            query = f"SELECT * FROM {self.table_name}"
            self.cursor.execute(query)
        
        return self.cursor.fetchall()

    def get_only_numbers_and_timestamps(self, since=None):
        if since:
            query = f"SELECT recognized_number, timestamp FROM {self.table_name} WHERE timestamp >= ?"
            self.cursor.execute(query, (since,))
        else:
            query = f"SELECT recognized_number, timestamp FROM {self.table_name}"
            self.cursor.execute(query)
        
        return self.cursor.fetchall()
    
    #TODO
    #add more methods to get data from the database

    def close(self):
        self.conn.close()