import os
import logging

logging.getLogger('tensorflow').setLevel(logging.ERROR)
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

from visitor_counter import VisitorCounter
from scheduler import Scheduler

def main():

    driver_path_ff = r"C:\Users\Doruk\Repos\personal\fun\rwth_gym_stats\geckodriver.exe"
    db_name = "gym_stats.db"
    table_name = "gym_stats_table"

    visitor_counter = VisitorCounter(driver_path_ff)
    scheduler = Scheduler(visitor_counter, db_name, table_name)
    scheduler.start() 

if __name__ == "__main__":
    main()