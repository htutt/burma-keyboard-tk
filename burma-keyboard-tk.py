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

""" Burma-Keyboard - A GUI program to install font and xkeyboard.
	It can be for font and xkb data installer and tries to help you 
	get your fonts and xkb data on your Linux/FreBSD system.
"""

__author__ = "Phone Htut <phonehtut2@gmail.com>"
__copyright__ = "Copyright (c) 2010, Phone Htut"
__license__  = "GPLv3"


""" burma-keyboard-tk package """
__port__ = "burma-keyboard-tk"
__version__ = "0.1.1"
__metor__ = "Phone Htut <phonehtut2@gmail.com>"


import glob, re, os, subprocess, sys, platform

from version_mod import *
check_python_version()

# Generally, Tkinter includes in Python standard library,
# but Tkinter needs tcl/tk, need to install tcl/tk on your system.
# On Debian and Ubuntu Linux, install 'python-tk'

try:
    from Tkinter import *
except ImportError:
    print>>sys.__stderr__, "** Burma-Keyboard-Tk can't import Tkinter.  " \
                           "Your Python may not be configured for Tk. **"
    sys.exit(1)
check_tk_version()

from tkMessageBox import *
from log_mod import *
from lookup_data import *
from text_view import *


class BurmaKeyboardTk(Tk):
	def __init__(self, parent):
		Tk.__init__(self, parent)
		self.initialize()
		self.protocol("WM_DELETE_WINDOW", self.Ok)
		self.parent = parent

	def initialize(self):
		""" initialize """
		frame = Frame(self, borderwidth=10)
		frame.pack(side=TOP, expand=TRUE, fill=BOTH, padx=10, pady=5)
		labelTitle = Label(frame, text='Burma-Keyboard',
							font=('Sans', 11, 'normal'))
		labelTitle.pack(side=LEFT)
		global __version__, __copyright__
		labelVer = Label(frame, text=" v" + __version__, justify=RIGHT)
		labelVer.pack(side=LEFT)
		labelC = Label(frame, text=__copyright__, fg="dimgray", justify=LEFT)
		labelC.pack(side=RIGHT)
		
	def Ok(self, event=None):
		""" app shutdown """
		if askokcancel(title="Quit Burma-Keyboard", message="Do you want to exit?"):
			log('Application exits.\n')
			self.destroy()

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
	
	t1.delete("1.0", END)
		
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
	 			t1.insert(END, log('Font : %s [ OK ]' % disp_src_font) + "\n")
				break
		else:
			t1.insert(END, log('ERROR: Font not found in %s folder!' % src_path))
			showerror(title="Error", message=("Font not fonund in the '%s' folder!" % src_path))
			showinfo(title='Suggest', message=(log("You can download it from Internet and put it in the '%s' folder and then try again." % src_path)))
			return
	
	# finding mm files
	src_xkb_data = os.path.join(src_path, xkb_data)
	if os.path.exists(src_xkb_data):
		xkb_data = open(src_xkb_data).read()
		if xkb_data.find(fontname)== -1 and xkb_data.find(email)== -1:
			t1.insert(END, log('You have NOT %s xkeyboard file!' % fontname) + "\n")
			showwarning(title="Xkeyboard file is not correct!", message=("Your Xkeyboard mm file is not for %s you have chosen!" % fontname))
			if askokcancel(title="Confirm", message="Do you want to continue installation?"):
				pass
			else:
				showinfo(title="Info", message="Please restart the program and try another font or contact the authors!")
				return
		else:
			t1.insert(END, log('Xkeyboard : %s Keyboard [ OK ]' % fontname) + "\n")
	else:
		t1.insert(END, log('ERROR: mm xkeyboard file not found.') + "\n")
		showerror(title="Error", message="Xkeyboard mm file not fonund in the source folder!")
		showinfo(title='Suggest', message=log("Check your xkb mm file in the %s folder or download from net and put it in the folder then try again" % src_path))
		return

# Installation fonts and keyboard data
def install():
	""" Install font and xkeyboard data """
	t2.delete("1.0", END)
	t2.insert(END, log('Start Installation...') + "\n")

	global src_font, src_xkb_data
	# making directories 
	t2.insert(END, log('Installing directories...') + "\n")
	new_font_dir = os.path.join(FONT_DIR, FONTNAME)
	new_doc_dir = os.path.join(DOC_DIR, FONTNAME)

	try:
		os.mkdir(new_font_dir)
		#os.mkdir(new_doc_dir)
		t2.insert(END, log('Installing directories done.') + "\n")
	except Exception as ex:
		showerror(title="Error", message=log(ex))
		t2.insert(END, log('You should uninstall previous package to continue new installation!') + "\n")
		log('You are being asked to uninstall previous install package.')
		if askyesno(title="Uninstall Previous Package?", message="Do  you want to unistall previous package?"):
			log('You do uninstall previous install package.')
			remove()
			log('Checking another font which can make problem...')
			really_clean()
			
			if askokcancel(title=log("Uninstallation finished!"), message="New Installation will continue."):
				log('You are being asked to continue Installation.')
				install()
				showinfo(title="Info", message=log("Installation is finished!"))
				return
			else:
				t2.insert(END, log('You stop the install progress after removing previous package!') + "\n")
				return
		else:
			t2.insert(END, log('You cancel installation!') + "\n")
			return
			

	# installing font file
	t2.insert(END, log('Installing %s font...' % FONTNAME) + "\n")
	if os.path.exists(new_font_dir):
		os.system('cp %s %s' % (src_font, new_font_dir))
		t2.insert(END, log('Installing %s font done.' % FONTNAME) + "\n")
	else:
		t2.insert(END, log('error: Font not installed!') + "\n")
	
	# backing up existing mm file
	t2.insert(END, log('Backuping original mm xkb file...') + "\n")
	mm_orig = os.path.join(XKB_DIR, 'mm')
	os.rename(mm_orig, mm_orig + '_bak')
	mm_bak = os.path.join(XKB_DIR, 'mm_bak')
	if os.path.exists(mm_bak):
		t2.insert(END, log('Backuping original mm xkb file done.') + "\n")
	else:
		t2.insert(END, log('ERROR: Not backup original xkb file!') + "\n")
		
	# install mm3 xkeyboard
	t2.insert(END, log('Installing %s xkeyboard...' % FONTNAME) + "\n")
	os.system('cp %s %s' % (src_xkb_data, XKB_DIR))
	mm_new = os.path.join(XKB_DIR, 'mm')
	if os.path.exists(mm_new):
		t2.insert(END, log('Installing %s keyboard done.' % FONTNAME) + "\n")
	else:
		t2.insert(END, log('ERROR: Not install xkeyboard!') + "\n")
		
	# installation finished
	t2.insert(END, log('Installation is finished!') + "\n")
	showinfo(title="Finished!", message=log("You may need to Log out or Restart your system to correct your keyboard."))
	
# Removing fonts and keyboard data
def remove():
	""" Remove the previous installation files and data """
	log('Start Uninstallation...')
	t2.delete("1.0", END)
	# check and delete previous installed package 
	dest_font_dir = os.path.join(FONT_DIR, FONTNAME)
	dest_doc_dir = os.path.join(DOC_DIR, FONTNAME)
	
	if os.path.exists(dest_font_dir):
		t2.insert(END, log('Removing previous installed %s font directory...' % FONTNAME) + "\n")
		os.system('rm -rf ' + dest_font_dir)
	if os.path.exists(dest_doc_dir):
		t2.insert(END, log('Removing previous installed %s doc directory...' % FONTNAME) + "\n")
		os.system('rm -rf ' + dest_doc_dir)

	# restore origial or backup xkb_data file
	mm_backup = os.path.join(XKB_DIR, 'mm_bak')
	mm_original = os.path.join(XKB_DIR, 'mm')
	if os.path.exists(mm_backup):
		t2.insert(END, log('Restoring mm backup file...') + "\n")
		os.rename(mm_backup, mm_original)
		if os.path.exists(mm_original):
			t2.insert(END, log('Restoring origianl or backup mm file done.') + "\n")
		else:
			t2.insert(END, log('ERROR: Not restore from backup file!') + "\n")
	else:
		t2.insert(END, log('Skip Restoring backup file : You do not have a backup file.') + "\n")
	t2.insert(END, log('Previous package removal done successfully!') + "\n")
	
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
		t2.insert(END,log('You still have to remove %s folder.' % f_dirs) + "\n")
		showwarning(title="Caution!", message=log("I'm going to remove it!"))
		log('Removing %s folder...' % f_dirs)
		try:
			os.system('rm -rf ' + f_dirs[0])
			t2.insert(END, log('%s folder successfully removed!' % f_dirs) + "\n")
		except Exception as ex:
			showerror(title="Error", message=log(ex))

# Test install
def install_test():
	""" install_test function go ahead before showing error """
	try:
		install()
	except Exception as ex:
		showerror(title="Error", message=log(ex))
		showinfo(title='Suggest', message=log('You must use sudo if error is Permission denied OR You need to choose a font and confirm before install.'))

# Log Display function
def display_log():
	""" displaying log file """
	log('You are reading logs.')
	t2.delete("1.0", END)
	log_file = read_log("logs.txt")
	for item in log_file:
		t2.insert(END, item)

# Read fonts function for OptionMenu
def read_fonts(filename):
	""" read font or font folder from specific file """
	fonts = [] # start with an empty array
	file_fonts = open(filename) # open the file
	for line in file_fonts: # Read from the file one line at a time
		fonts.append(line.rstrip()) # Append a stripped copy of line to array
	return fonts # return the list to the calling code.

# Font define
def define_font():
	""" define font which have chosen """
	global FONTNAME
	font = find_details(choose_font.get())
	log('You choose %s font.' % choose_font.get())
	if font:		
		FONTNAME = font['fontname'] # name for font directory in system
		fontname = font['fontname'] # name for font name inside mm file
		fontfolder = font['fontfolder'] # folder name in package source folder
		email = font['email'] # email in xkb mm file
	
	if askokcancel(title="Confirm font", message=("Are you going with %s font?" % choose_font.get())):
		log('You confirmed %s font to install or uninstall.' % choose_font.get())
	else:
		return
	resource(fontname, fontfolder, email)

# About
def about():
	""" about dialog """
	import aboutdialog
	aboutdialog.AboutDialog(root, 'About')


if __name__ == "__main__":

	root = BurmaKeyboardTk(None)
	root.title('Burma-Keyboard')

	# system platform frame
	g4 = Frame(root)
	g4.pack(padx=20, pady=10, fill=BOTH, expand=YES)

	# choose font frame
	g0_lfmt = "Choose your favorite font first, then click Confirm button"
	g0 = LabelFrame(root, text=g0_lfmt, padx=5, pady=5)
	g0.pack(padx=20, pady=10, fill=BOTH, expand=YES)
	g0.config(labelanchor=NW)

	# source status frame
	g1 = LabelFrame(root, text="Sources Status:", padx=5, pady=5)
	g1.pack(padx=20, pady=10, fill=BOTH, expand=YES)
	g1.config(labelanchor=NW)
	t1 = Text(g1, height=2, width=80)
	t1.pack(side=BOTTOM,fill=BOTH)
	t1.delete("1.0", END)

	# operating status frame
	g2_lfmt = "Operating Status:"
	g2 = LabelFrame(root, text=g2_lfmt, padx=5, pady=5)
	g2.pack(padx=20, pady=10, fill=BOTH, expand=YES)
	g2.config(labelanchor=NW)
	# Scrollbar for Text boxes
	scrollbar = Scrollbar(g2)
	scrollbar.pack(side=RIGHT, fill=Y)
	t2 = Text(g2, height=15, width=80, yscrollcommand=scrollbar.set)
	scrollbar.config(command=t2.yview)
	t2.pack(fill=BOTH)
	
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
		Label(g4, text=(log("System platform : %s [ OK ]" % platform.system()))).pack(side=LEFT)
		log('Your Linux Distro is %s %s %s.' %(distro[0],distro[1],distro[2]))
	elif sys.platform.startswith('freebsd'):
		use_fhs = FreeBSD()
		FONT_DIR = use_fhs.fonts_dir
		DOC_DIR = use_fhs.doc_dir
		XKB_DIR= use_fhs.xkb_dir
		distro = platform.uname()
		Label(g4, text=("System platform : %s [ OK ]" % distro[0])).pack(side=LEFT)
		log('Your FreeBSD Release is %s.' % distro[2])
	else:
		sys.exit('Sorry, please try on Linux/Unix system!\n')

	# font options variables and option menu
	choose_font = StringVar()
	choose_font.set(None)
	options = read_fonts("fontfolders.txt")
	OptionMenu(g0, choose_font, *options).pack(side=LEFT)
	b0 = Button(g0, text="Confirm", width=6, command=define_font)
	b0.pack(side=LEFT)

	# command buttons frame
	g3 = LabelFrame(root, text="Commands:", padx=5, pady=5)
	g3.pack(padx=20, pady=10, fill=BOTH, expand=YES)
	g3.config(labelanchor=NW)
	
	b1 = Button(g3, text="Install", width=6, command=install_test)
	b1.pack(side=LEFT, padx=2, pady=2)

	b2 = Button(g3, text="Uninstall", width=6, command=remove)
	b2.pack(side=LEFT, padx=2, pady=2)
		
	b3 = Button(g3, text="Logs", width=6, command=display_log)
	b3.pack(side=LEFT, padx=2, pady=2)

	b4 = Button(g3, text="About", width=6, command=about)
	b4.pack(side=RIGHT, padx=2, pady=2)

	# log file browser button
	log_file_name = './logs.txt'
	b5 = Button(g3, text='View log',command=lambda:view_file(root, 'logs.txt', log_file_name))
	b5.pack(side=LEFT, padx=2, pady=2)

	# layout help file browser button
	l_help_file = './layout_help.txt'
	b6 = Button(g3, text='Layout help',command=lambda:view_file(root, 'layout_help.txt', l_help_file))
	b6.pack(side=LEFT, padx=2, pady=2)

	# quit
	b7 = Button(g3, text="Quit", width=6, command=root.Ok)
	b7.pack(side=LEFT, padx=2, pady=2)

	log('Application initializes and Ready.')

	root.mainloop()
