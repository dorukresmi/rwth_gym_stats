from gym_stats.data_store import DataStore
import schedule
import time
import threading

class Scheduler:
    def __init__(self, visitor_counter, db_name, table_name):
        self.visitor_counter = visitor_counter
        self.db_name = db_name
        self.table_name = table_name
        self.stop_event = threading.Event()
        self.pause_event = threading.Event()
        self.pause_event.set()

    def job(self):

        self.pause_event.wait()

        if self.stop_event.is_set():
            return

        self.visitor_counter.reconnect_driver()
        image_path, timestamp = self.visitor_counter.get_and_save_image()
        self.visitor_counter.close_driver()
        number = self.visitor_counter.recognize_number_from_image()
        store = DataStore(self.db_name, self.table_name)

        year = timestamp[:4]
        month = timestamp[5:7]
        day = timestamp[8:10]
        week = time.strftime("%W", time.strptime(timestamp, "%Y-%m-%d %H:%M:%S"))
        weekday = time.strftime("%w", time.strptime(timestamp, "%Y-%m-%d %H:%M:%S"))
        hour = timestamp[11:13]

        store.add_data(image_path, number, timestamp, year, month, day, week, weekday, hour)
        store.close()
    
    def start(self, interval=1):
        schedule.every(interval).minutes.do(self.job_wrapper)
        while not self.stop_event.is_set():
            schedule.run_pending()
            time.sleep(1)

    def job_wrapper(self):
        job_thread = threading.Thread(target=self.job)
        job_thread.start()

    def stop(self):
        self.stop_event.set()

    def pause(self):
        self.pause_event.clear()

    def resume(self):
        self.pause_event.set()