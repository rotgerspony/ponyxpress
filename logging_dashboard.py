
import logging

def setup_logs():
    logging.basicConfig(filename='ponyxpress.log', level=logging.INFO)

def log_event(msg):
    logging.info(msg)
