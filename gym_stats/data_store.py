import sqlite3



class DataStore:
    def __init__(self, db_name, table_name):
        
        self.db_name = db_name
        self.table_name = table_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.initialize_db()


    def initialize_db(self):
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT,
            recognized_number INTEGER,
            timestamp DATETIME
        );''')
        self.conn.commit()
    
    def add_data(self, image_path, recognized_number, timestamp):
        self.cursor.execute(f"INSERT INTO {self.table_name} (image_path, recognized_number, timestamp) VALUES (?, ?, ?)",
                            (image_path, recognized_number, timestamp))
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

    def close(self):
        self.conn.close()