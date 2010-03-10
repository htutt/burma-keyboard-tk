#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
	copyright (c) 2010, Phone Htut <phonehtut2@gmail.com>

	Burma-Keyboard is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

""" Burma-Keyboard - A program to install font and xkeyboard.
	It can be for font and xkb data installer and tries to help you 
	get your fonts and xkb data on your Linux/FreBSD system.
"""

""" burma-keyboard-nogui.py - Burma-keyboard program without GUI.
	It is CLI (command line interface) program.

"""

__author__ = "Phone Htut <phonehtut2@gmail.com>"
__copyright__ = "Copyright (c) 2010, Phone Htut"
__license__  = "GPLv3"


""" burma-keyboard-tk package """
__port__ = "burma-keyboard-tk"
__version__ = "0.1.1"
__metor__ = "Phone Htut <phonehtut2@gmail.com>"


import glob, re, os, subprocess, sys, platform

# Check Python version
py_ver = sys.version_info[:2]
if py_ver <= (2, 3) or py_ver >= (3, 0):
	print "\n" * 3
	print "="*75
	print "Running Python version:", py_ver
	print "Your system should have Python 2.4 or greater, but not yet 3 to use\nthis program."
	print "Terminating."
	print "="*75
	print "\n" * 3
	sys.exit(0)

from log_mod import *
from lookup_data import *


class Linux:
	fonts_dir = '/usr/share/fonts'
	doc_dir = '/usr/share/doc'
	xkb_dir = ['/usr/share/X11/xkb/symbols', '/etc/X11/xkb/symbols']
	def __init__(self):
		""" Classifying Linux FHS """

class FreeBSD:
	fonts_dir = '/usr/local/lib/X11/fonts'
	doc_dir = '/usr/local/share/doc'
	xkb_dir = '/usr/local/share/X11/xkb/symbols'
	def __init__(self):
		""" Classifying FreeBSD FHS """

# Checking Resources of font and xkb file
def resource(fontname, fontfolder, email):
	""" check resources of font and xkb file """
	global src_font, src_xkb_data
	
	src_path = './' + fontfolder + '/'
	xkb_data = 'mm'

	working_dir = os.getcwd()
	log("Checking '%s' source folder under '%s' directory..." % (src_path, working_dir))
	
	# finding fonts
	if os.path.exists(src_path):
		for src_font in os.listdir(src_path):
			if src_font.endswith('ttf'):
				# real working path
				src_font = os.path.join(src_path, src_font)
				# for show font only
				disp_src_font = src_font
				num_src_l = len(src_path)
				disp_src_font = disp_src_font[num_src_l:]
	 			print(log('Font : %s [ OK ]' % disp_src_font))
				break
		else:
			print(log('ERROR: Font not found in %s folder!' % src_path))
			print(log("You can download it from Internet and put it in the '%s' folder and then try again." % src_path) + "\n")
			sys.exit(0)
	
	# finding mm files
	src_xkb_data = os.path.join(src_path, xkb_data)
	if os.path.exists(src_xkb_data):
		xkb_data = open(src_xkb_data).read()
		if xkb_data.find(fontname)== -1 and xkb_data.find(email)== -1:
			print(log('You have NOT %s xkeyboard file!' % fontname))
			print(log("Your Xkeyboard mm file is not for %s you have chosen!" % fontname))
		else:
			print(log('Xkeyboard : %s Keyboard [ OK ]' % fontname))
	else:
		print(log('ERROR: mm xkeyboard file not found.'))
		print(log("Xkeyboard mm file not fonund in the source folder!"))
		print(log("Check your xkb mm file in the %s folder or download from net and put it in the folder then try again." % src_path) + "\n")
		sys.exit(0)

# Installation fonts and keyboard data
def install():
	""" Install font and xkeyboard data """
	print(log('Start Installation...'))

	global src_font, src_xkb_data
	# making directories 
	print(log('Installing directories...'))
	new_font_dir = os.path.join(FONT_DIR, FONTNAME)
	new_doc_dir = os.path.join(DOC_DIR, FONTNAME)

	try:
		os.mkdir(new_font_dir)
		#os.mkdir(new_doc_dir)
		print(log('Installing directories done.'))
	except Exception as ex:
		print(log(ex))
		print(log('You should uninstall previous package to continue new installation!'))
		log('You are being asked to uninstall previous install package.')
		ans4uninstall = raw_input("Do  you want to unistall previous package? Y/n ")
		if ans4uninstall == 'y' or ans4uninstall == 'Y':
			log('You do uninstall previous installed package.')
			remove()
			log('Checking another font which can make problem...')
			really_clean()
			
			ans4newinstall = raw_input("New Installation will continue? Y/n ")
			if ans4newinstall == 'y' or ans4newinstall == 'Y':
				log('You are being asked to continue Installation.')
				install()
				return
			else:
				print(log('You stop the install progress after removing previous package!'))
				return
		else:
			print(log('You cancel installation!'))
			return
			

	# installing font file
	print(log('Installing %s font...' % FONTNAME))
	if os.path.exists(new_font_dir):
		os.system('cp %s %s' % (src_font, new_font_dir))
		print(log('Installing %s font done.' % FONTNAME))
	else:
		print(log('error: Font not installed!'))
	
	# backing up existing mm file
	print(log('Backuping original mm xkb file...'))
	mm_orig = os.path.join(XKB_DIR, 'mm')
	os.rename(mm_orig, mm_orig + '_bak')
	mm_bak = os.path.join(XKB_DIR, 'mm_bak')
	if os.path.exists(mm_bak):
		print(log('Backuping original mm xkb file done.'))
	else:
		print(log('ERROR: Not backup original xkb file!'))
		
	# install mm3 xkeyboard
	print(log('Installing %s xkeyboard...' % FONTNAME))
	os.system('cp %s %s' % (src_xkb_data, XKB_DIR))
	mm_new = os.path.join(XKB_DIR, 'mm')
	if os.path.exists(mm_new):
		print(log('Installing %s keyboard done.' % FONTNAME))
	else:
		print(log('ERROR: Not install xkeyboard!'))
		
	# installation finished
	print(log('Installation is finished!') + "\n")
	print(log("You may need to Log out or Restart your system to correct your keyboard.") + "\n")
	
# Removing fonts and keyboard data
def remove():
	""" Remove the previous installation files and data """
	print '\n'
	print(log('Start Uninstallation...'))
	# check and delete previous installed package 
	dest_font_dir = os.path.join(FONT_DIR, FONTNAME)
	dest_doc_dir = os.path.join(DOC_DIR, FONTNAME)
	
	if os.path.exists(dest_font_dir):
		print(log('Removing previous installed %s font directory...' % FONTNAME))
		os.system('rm -rf ' + dest_font_dir)
	if os.path.exists(dest_doc_dir):
		print(log('Removing previous installed %s doc directory...' % FONTNAME))
		os.system('rm -rf ' + dest_doc_dir)

	# restore origial or backup xkb_data file
	mm_backup = os.path.join(XKB_DIR, 'mm_bak')
	mm_original = os.path.join(XKB_DIR, 'mm')
	if os.path.exists(mm_backup):
		print(log('Restoring mm backup file...'))
		os.rename(mm_backup, mm_original)
		if os.path.exists(mm_original):
			print(log('Restoring origianl or backup mm file done.'))
		else:
			print(log('ERROR: Not restore from backup file!'))
	else:
		print(log('Skip Restoring backup file : You do not have a backup file.'))
	print(log('Previous package removal done successfully!') + "\n")
	
# Not keep two fonts together
def really_clean():
	""" really_clean function prevent not being together zawgyi and mm fonts
	in your system """
	f_dirs = []
	if os.path.exists(os.path.join(FONT_DIR, 'mm3')):
		f_dirs.append(os.path.join(FONT_DIR, 'mm3'))
	if os.path.exists(os.path.join(FONT_DIR, 'zawgyi')):
		f_dirs.append(os.path.join(FONT_DIR, 'zawgyi'))
		
	if f_dirs:
		print(log('You still have to remove %s folder.' % f_dirs))
		print(log("I'm going to remove it!"))
		print(log('Removing %s folder...' % f_dirs))
		try:
			os.system('rm -rf ' + f_dirs[0])
			print(log('%s folder successfully removed!' % f_dirs[0]) + '\n')
		except Exception as ex:
			print(log(ex))
		try:
			os.system('rm -rf ' + f_dirs[1])
			print(log('%s folder successfully removed!' % f_dirs[1]))
		except IndexError:
			pass
		except IOError:
			print(log('Permission denied! or You must use Sudo.!'))

# Test install
def install_test():
	""" install_test function go ahead before showing error """
	try:
		remove()
		really_clean()
		install()
	except Exception as ex:
		print(log(ex))
		print(log('You must use sudo if error is Permission denied OR You need to choose a font and confirm before install.'))

# Read fonts function
def read_fonts(filename):
	""" read font or font folder from specific file """
	fonts = [] # start with an empty array
	file_fonts = open(filename) # open the file
	for line in file_fonts: # Read from the file one line at a time
		fonts.append(line.rstrip()) # Append a stripped copy of line to array
	return fonts # return the list to the calling code.

# Choose font
def choose_font():
	print(log("Choose a font..."))
	options = read_fonts("fontfolders.txt")
	print('This is a list of font folder names.' + '\n')
	print options
	print '\n'
	t = 0
	while ( t == 0 ):
		choose_font = raw_input("Enter your fontfolder name: ")
		rusure = raw_input("Are you going with %s font? Y/n " % choose_font)
		if rusure == 'Y' or rusure == 'y':
			print(log('You confirmed %s font to install or uninstall.' % choose_font))
			try:
				define_font(choose_font)
				break
			except NameError:
				print(log('The %s you chosen is not in source folder.' % choose_font))
				print(log('You should type correct name only in the list.'))
				t = 0
		else:
			print(log('You did confirm %s font yet.' % choose_font))
			tryagain = raw_input("Would you like to choose new font? Y/n ")
			if tryagain == 'Y' or tryagain == 'y':
				t = 0
			else:
				print(log("You didn't choose any font."))
				sys.exit("Nothing to do. Bye!\n")
		

# Font define
def define_font(chose_font):
	""" define font which have chosen """
	global FONTNAME
	font = find_details(chose_font)
	print(log('You choose %s font.' % chose_font))
	if font:		
		FONTNAME = font['fontname'] # name for font directory in system
		fontname = font['fontname'] # name for font name inside mm file
		fontfolder = font['fontfolder'] # folder name in package source folder
		email = font['email'] # email in xkb mm file
	
	resource(fontname, fontfolder, email)

# Display text file in the shell
def display_txt_in_shell(filename):
    try:
        file_txts = open(filename)
        for line in file_txts:
            print(line.strip("\n"))
    except IOError:
        print("Cannot open %s file" % filename)


if __name__ == "__main__":

	# for shell beauty
	print '\n' * 2

	# Detecting distributions and finding correct paths for installation
	log('Checking your system platform...')
	if sys.platform.startswith('linux'):
		use_fhs = Linux()
		possible_xkb_dirs = use_fhs.xkb_dir
		for correct_xkb_dir in possible_xkb_dirs:
			if os.path.exists(correct_xkb_dir):
				XKB_DIR = correct_xkb_dir
				break
		FONT_DIR = use_fhs.fonts_dir
		DOC_DIR = use_fhs.doc_dir
		distro = platform.dist()
		print(log("System platform : %s [ OK ]" % platform.system()))
		print(log('Your Linux Distro is %s %s %s.' %(distro[0],distro[1],distro[2])))
	elif sys.platform.startswith('freebsd'):
		use_fhs = FreeBSD()
		FONT_DIR = use_fhs.fonts_dir
		DOC_DIR = use_fhs.doc_dir
		XKB_DIR= use_fhs.xkb_dir
		distro = platform.uname()
		print(log("System platform : %s [ OK ]" % distro[0]))
		print(log('Your FreeBSD Release is %s.' % distro[2]))
	else:
		sys.exit('Sorry, please try on Linux/Unix system!\n')

	log('Application initializes and Ready.')

	choose_font()

	# asking what to do ( install or uninstall, something like that)
	print "\n"
	while 1:
		ans = raw_input('[i] install, [r] remove, [h] layout help,\n[l] logs, [q] exit : ')
		if ans == 'i':
			install_test()
		elif ans == 'r':
			remove()
		elif ans ==  'h':
			print "\n" * 4
			print "-"*75
			display_txt_in_shell("layout_help.txt")
			print "-"*75
			print "\n" * 2
		elif ans == 'l':
			print "\n" * 2
			print "-"*75
			display_txt_in_shell("logs.txt")
			print "-"*75
			print "\n" * 1
		elif ans == 'q':
			sys.exit('\nHave a nice day, Good bye!\n')
		else:
			print '\nPlease press *small letter* [i] [r] [h] [l] [q] !\n'


