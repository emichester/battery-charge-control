#!/usr/bin/env python3
"""
See:
	https://stackoverflow.com/questions/38828578/python-threading-interrupt-sleep
	https://stackoverflow.com/questions/20044559/how-to-pip-or-easy-install-tkinter-on-windows

You can modify the parameters ( recommended_values		#		test_values ):
	TIME_TO_WAIT = 		5000		# 2000 ## in milliseconds 
	LOWER_THRESHOLD = 	40			# 100
	UPPER_THRESHOLD = 	80
	SEND_MESSAGE_TIME = 20.0		# 5.0

Requirements:
	threading
	tk
	psutil
"""

TIME_TO_WAIT = 5000 # in milliseconds 
LOWER_THRESHOLD = 45
UPPER_THRESHOLD = 75
SEND_MESSAGE_TIME = 20.0

from threading import Timer, Thread, Semaphore, Event
from time import time, sleep
import psutil
from tkinter import Tk, messagebox
import socket
## environment variables
from environ import server_address

def client(client_address=('localhost',8001)):
    """
    The client must receive in his own IP
    otherwise it will be not able to bind
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(client_address)
    data, addr = sock.recvfrom(4096)
    sock.close()
    return str(data.decode('ascii'))
    

def server(data, server_address=('localhost',8001)):
    """
    The server can send anywhere
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(data.encode('ascii'), server_address)
    sock.close()

def read_key(quit, quit_sem, event):
	value = input("To quit press 'q' + ENTER: ")
	if value == 'q' or value == 'Q':
		quit_sem.acquire(blocking=True, timeout=None)
		quit[0] = True
		event.set()
		quit_sem.release()

def check_battery():
	return int(psutil.sensors_battery().percent)

def send_message(state,server_address):
	if state == 0:
		server('on',server_address)
	else:
		server('off',server_address)

def th_send_message(quit, quit_sem, event, server_address):

	quit_sem.acquire(blocking=True, timeout=None)
	quit_l = quit[0]
	quit_sem.release()
	low_trigger = False
	high_trigger = False

	while not quit_l:
		percent = check_battery()
		print("\n%i"%percent) # borrar

		if percent <= LOWER_THRESHOLD:
			if not low_trigger:
				send_message(0,server_address)
			low_trigger = True
			high_trigger = False
		elif percent >= UPPER_THRESHOLD:
			if not high_trigger:
				send_message(1,server_address)
			low_trigger = False
			high_trigger = True
		
		
		event.wait(SEND_MESSAGE_TIME)

		quit_sem.acquire(blocking=True, timeout=None)
		quit_l = quit[0]
		quit_sem.release()
	
	server('off',server_address)



if __name__ == "__main__":

	event = Event()

	quit = [False]
	quit_sem = Semaphore(value=1)

	main_thread = Thread( target=read_key, args=(quit, quit_sem, event) )
	main_thread.start()

	threads = []
	threads.append(
		Thread( target=th_send_message, args=(quit, quit_sem, event, server_address) )
	)

	for t in threads:
		t.start()
	
	for t in threads:
		t.join()

	main_thread.join()
