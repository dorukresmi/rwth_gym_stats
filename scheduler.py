from datetime import datetime
from data_store import DataStore
import schedule
import time

class Scheduler:
    def __init__(self, visitor_counter):
        self.visitor_counter = visitor_counter

    def job(self):
        self.visitor_counter.reconnect_driver()
        timestamp = self.visitor_counter.get_and_save_image()
        self.visitor_counter.close_driver()
        number = self.visitor_counter.recognize_number_from_image()
        # timestamp = datetime.now()
        print(f"Number: {number}, Timestamp: {timestamp}")
        DataStore.add_data(number, timestamp)

    def start(self, interval=1):
        schedule.every(interval).minutes.do(self.job)
        while True:
            schedule.run_pending()
            time.sleep(1)