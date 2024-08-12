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
        store.add_data(image_path, number, timestamp)
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