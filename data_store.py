import sqlite3

class DataStore:
    def __init__(self, db_name="screenshots.db"):
        
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.initialize_db()

    def initialize_db(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS screenshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT,
            recognized_number TEXT,
            timestamp DATETIME
        );''')
        self.conn.commit()
    
    def add_data(self, image_path, recognized_number, timestamp):
        self.cursor.execute("INSERT INTO screenshots (image_path, recognized_number, timestamp) VALUES (?, ?, ?)",
                            (image_path, recognized_number, timestamp))
        self.conn.commit()

    def get_data(self, since=None):
        if since:
            query = "SELECT * FROM screenshots WHERE timestamp >= ?"
            self.cursor.execute(query, (since,))
        else:
            query = "SELECT * FROM screenshots"
            self.cursor.execute(query)
        
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

    # @classmethod
    # def add_data(cls, number, timestamp):
    #     cls.data.append((number, timestamp))

    # @classmethod
    # def get_data(cls):
    #     return cls.data
    
# class Statistics:
#     @staticmethod
#     def calculate_statistics():
#         data = DataStore.get_data()
#         # Analyze data
#         return "Statistics"