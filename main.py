import os
import tensorflow as tf

# Suppress TensorFlow oneDNN messages by setting the environment variable
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Suppress TensorFlow deprecation warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

from visitor_counter import VisitorCounter
from scheduler import Scheduler

#TODO
#replace with the global driver path
#maybe take it as an argument
driver_path_ff = r"C:\Users\Doruk\Repos\personal\fun\rwth_gym_stats\geckodriver.exe"

visitor_counter = VisitorCounter(driver_path_ff)
scheduler = Scheduler(visitor_counter)
scheduler.start() 