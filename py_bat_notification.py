#!/usr/bin/env python3
"""
See:
	https://stackoverflow.com/questions/38828578/python-threading-interrupt-sleep
	https://stackoverflow.com/questions/20044559/how-to-pip-or-easy-install-tkinter-on-windows

You can modify the parameters ( recommended_values		#		test_values ):
	TIME_TO_WAIT = 		5000		# 2000 ## in milliseconds 
	LOWER_THRESHOLD = 	40			# 100
	SHOW_MESSAGE_TIME = 20.0		# 5.0

Requirements:
	threading
	tk
	psutil
"""

TIME_TO_WAIT = 5000 # in milliseconds 
LOWER_THRESHOLD = 40
UPPER_THRESHOLD = 80
SHOW_MESSAGE_TIME = 20.0

from threading import Timer, Thread, Semaphore, Event
from time import time, sleep
from psutil import sensors_battery
from tkinter import Tk, messagebox

def read_key(quit, quit_sem, event):
	value = input("To quit press 'q' + ENTER: ")
	if value == 'q' or value == 'Q':
		quit_sem.acquire(blocking=True, timeout=None)
		quit[0] = True
		event.set()
		quit_sem.release()

def check_battery():
	return int(sensors_battery().percent)

def show_message(state=0):
	window = Tk()
	try:
		window.wm_withdraw()
		window.after(TIME_TO_WAIT, window.destroy)
		if state == 0:
			messagebox.showinfo(title="¡¡¡ALERTA!!!", message="¡Batería baja!")
		else:
			messagebox.showinfo(title="¡¡¡ALERTA!!!", message="¡Batería muy alta!")
	except:
		pass
	finally:
		try:
			window.destroy()
		except:
			pass
		finally:
			return 0

def th_show_message(quit, quit_sem, event):

	quit_sem.acquire(blocking=True, timeout=None)
	quit_l = quit[0]
	quit_sem.release()

	while not quit_l:
		print("\n%i"%check_battery()) # borrar

		if check_battery() <= LOWER_THRESHOLD:
			show_message(0)
		elif check_battery() >= UPPER_THRESHOLD:
			show_message(1)
		
		
		event.wait(SHOW_MESSAGE_TIME)

		quit_sem.acquire(blocking=True, timeout=None)
		quit_l = quit[0]
		quit_sem.release()



if __name__ == "__main__":

	event = Event()

	quit = [False]
	quit_sem = Semaphore(value=1)

	main_thread = Thread( target=read_key, args=(quit, quit_sem, event) )
	main_thread.start()

	threads = []
	threads.append(
		Thread( target=th_show_message, args=(quit, quit_sem, event) )
	)

	for t in threads:
		t.start()
	
	for t in threads:
		t.join()

	main_thread.join()
