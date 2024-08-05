from gym_stats.data_store import DataStore
import schedule
import time

class Scheduler:
    def __init__(self, visitor_counter, db_name, table_name):
        self.visitor_counter = visitor_counter
        self.db_name = db_name
        self.table_name = table_name

    def job(self):
        self.visitor_counter.reconnect_driver()
        image_path, timestamp = self.visitor_counter.get_and_save_image()
        self.visitor_counter.close_driver()
        number = self.visitor_counter.recognize_number_from_image()
        store = DataStore(self.db_name, self.table_name)
        store.add_data(image_path, number, timestamp)
        store.close()

    def start(self, interval=1):
        schedule.every(interval).minutes.do(self.job)
        while True:
            schedule.run_pending()
            time.sleep(1)