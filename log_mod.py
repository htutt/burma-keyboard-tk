#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" log_mod.py is a module for logging.

"""
""" This file is part of burma-keyboard.

"""

import time

# log save to file
def log(text):
	date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
	try:
		file = open("logs.txt", "a")
		file.write("[%s] - %s\n" % (date, text))
		file.close()
		return text
	except IOError:
		print ("Connot create log file")
		
	

# read log file
def read_log(log_file):
    try:
        logs = []
        file_logs = open(log_file)
        for line in file_logs:
            logs.append(line.rstrip() + "\n" )
        return logs
    except IOError:
        print ("Cannot open log file")
