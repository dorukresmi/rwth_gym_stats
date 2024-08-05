import os
import logging
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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

    visitor_counter = VisitorCounter(driver_path_ff)
    scheduler = Scheduler(visitor_counter, db_name, table_name)
    scheduler.start() 

if __name__ == "__main__":
    main()