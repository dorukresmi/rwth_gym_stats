import os
import logging
import time
import threading

logging.getLogger('tensorflow').setLevel(logging.ERROR)
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

from gym_stats.visitor_counter import VisitorCounter
from gym_stats.scheduler import Scheduler

def main():

    db_name = "gym_stats.db"
    table_name = "gym_stats_table"
    
    try:
        while True:
            try:
                visitor_counter = VisitorCounter()
                scheduler = Scheduler(visitor_counter, db_name, table_name)

                scheduler_thread = threading.Thread(target=scheduler.start)
                scheduler_thread.start()

                while True:
                    command = input("Enter 'pause', 'resume', 'stop', or 'exit': ").strip().lower()

                    if command == 'pause':
                        scheduler.pause()
                    elif command == 'resume':
                        scheduler.resume()
                    elif command == 'stop':
                        scheduler.stop()
                        scheduler_thread.join()
                        break
                    elif command == 'exit':
                        scheduler.stop()
                        scheduler_thread.join()
                        return          
            except ConnectionError as conn_err:
                logging.error(f"Connection error occurred: {conn_err}")
                time.sleep(900)
            except Exception as e:
                logging.error(f"An error occurred: {e}")
                break

    except KeyboardInterrupt:
        if scheduler:
            scheduler.stop()
        if scheduler_thread:
            scheduler_thread.join()
        logging.info("Program interrupted and exiting.")

        
if __name__ == "__main__":
    main()