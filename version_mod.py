#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" version_mod.py check Python version and Tk version.

"""
""" This file is part of burma-keyboard.

"""

import sys
def check_python_version():
	py_ver = sys.version_info[:2]
	if py_ver <= (2, 3) or py_ver >= (3, 0):
		print "\n" * 3
		print "="*75
		print "Running Python version:", py_ver
		print "Your system should have Python 2.4 or greater, but not yet 3 to use\nthis GUI program."
		print "Terminating."
		print "="*75
		print "\n" * 3
		sys.exit(0)


from Tkinter import *
def check_tk_version():
	if TkVersion < 8.0 :
		print "\n" * 3
		print "="*75
		print "Running Tk version:", TkVersion
		print "You must be using Tk version 8.0 or greater to use this GUI program."
		print "Terminating."
		print "="*75
		print "\n" * 3
		sys.exit(0)
