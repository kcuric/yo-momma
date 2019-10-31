import time
import os
import signal
import sys
import logging
from joker import Joker

joker = Joker()

def sigint_handler(signum, frame):
    """
    Function for handling the program abort
    via CTRL + C (SIGINT).
    """
    global joker
    logging.info('Program is terminating!')
    del joker
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, sigint_handler)

    logging.info('USE CTRL+C TO STOP THE PROGRAM! :)')
    while True:
        if joker.take_picture():
            joker.tell_joke()
        elif joker.take_picture() == -1:
            logging.error("ERROR: Picture not taken!")
        time.sleep(2)

if __name__ == "__main__":
    main()
