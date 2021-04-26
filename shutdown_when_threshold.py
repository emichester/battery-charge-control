#!/usr/bin/env python3
"""

Must be executed with sudo

"""
TIME_TO_WAIT = 5000 # in milliseconds
THRESHOLD = 80

from time import sleep
from psutil import sensors_battery
import os

def check_battery():
	return int(sensors_battery().percent)

if __name__ == "__main__":

    try:
        while True:
            if check_battery() <= 80:
                os.system("shutdown now")
            else:
                print("Battery level: %d"%check_battery())
            sleep(1000)
    except KeyboardInterrupt:
        print("Shutdown stopped")
    except Exception as e:
        print("Exception: %s"%e)