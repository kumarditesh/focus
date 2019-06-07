#!/usr/bin/env python
from argparse import ArgumentParser
from enum import Enum
import logging
import sys
import subprocess
import time

logger = logging.getLogger()

def configure_logger():
    # Log to console for now
    ch = logging.StreamHandler(sys.stdout)
    logger.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.debug('Testing logger')

_supported_ = 1
_unsupported_ = 0

class Operation(Enum):
    start = 'start'
    stop = 'stop'
    pause = 'pause'
    _continue = '_continue'
    reset = 'reset'
    schedule = 'schedule'
    till = 'till'

    def __str__(self):
        return self.name

def get_duration(args):
    if args.seconds:
        return args.seconds
    elif args.minutes:
        return args.minutes*60
    else:
        raise ValueError('Abe kab tak chalana hai??')

def display_osx_notification(message):
    subprocess.run(["osascript", "-e", 'display notification \"{}\" with title \"{}\"'.format(message, message)])

def dnd_on():
    subprocess.run(["do-not-disturb", "on"])

def dnd_off():
    subprocess.run(["do-not-disturb", "off"])

def start(seconds):
    minutes = int(seconds/60)
    message = 'DND on for {} mins!!'.format(minutes)
    logger.info(message)
    display_osx_notification(message)
    time.sleep(1)
    dnd_on()
    time.sleep(seconds)
    dnd_off()
    off_message = 'DND off!!'
    display_osx_notification(off_message)
    logger.info(off_message)

def main():
    configure_logger()
    parser = ArgumentParser()

    # Add more options if you like
    parser.add_argument(dest="operation", type=Operation, choices=list(Operation),
                        help="operations to manage focus states like start, stop...")
    parser.add_argument("-s", "--seconds", type=int, dest="seconds", help="focus run in seconds")
    parser.add_argument("-m", "--minutes", type=int, dest="minutes", help="focus run in seconds")

    args = parser.parse_args()
    operation = args.operation
    duration_in_seconds = get_duration(args)
    if operation == Operation.start:
        start(duration_in_seconds)

if __name__ == '__main__':
    main()