import os
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


logging.getLogger('tensorflow').setLevel(logging.ERROR)
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

from gym_stats.visitor_counter import VisitorCounter
from gym_stats.scheduler import Scheduler

def main():

    #TODO
    #replace with the global driver path
    #maybe take it as an argument
    driver_path_ff = r"C:\Users\Doruk\Repos\personal\fun\rwth_gym_stats\geckodriver.exe"
    db_name = "gym_stats.db"
    table_name = "gym_stats_table"

    while True:
        try:
            visitor_counter = VisitorCounter(driver_path_ff)
            scheduler = Scheduler(visitor_counter, db_name, table_name)
            scheduler.start()
        except ConnectionError as conn_err:
            logging.error(f"Connection error occurred: {conn_err}")
            time.sleep(900)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    main()