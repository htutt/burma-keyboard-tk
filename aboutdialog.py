#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" About Dialog for Burma-Keyboard

"""
""" This file is part of burma-keyboard.

"""

from Tkinter import *
import os
import text_view

class AboutDialog(Toplevel):
	""" Modal about dialog """
	def __init__(self,parent,title):
		Toplevel.__init__(self, parent)
		self.configure(borderwidth=5)
		self.geometry("+%d+%d" % (parent.winfo_rootx()+30,
								  parent.winfo_rooty()+30))
		self.Initialize()
		self.resizable(height=FALSE, width=FALSE)
		self.title(title)
		self.transient(parent)
		self.grab_set()
		self.protocol("WM_DELETE_WINDOW", self.Ok)
		self.parent = parent
		self.buttonOk.focus_set()
		self.bind('<Return>',self.Ok) #dismiss dialog
		self.bind('<Escape>',self.Ok) #dismiss dialog
		self.wait_window()

	def Initialize(self):
		frame0 = Frame(self, borderwidth=2, relief=SUNKEN)
		frameButtons = Frame(self)
		frameButtons.pack(side=BOTTOM, fill=X)
		frame0.pack(side=TOP, expand=TRUE, fill=BOTH)
		self.buttonOk = Button(frameButtons, text='Close', command=self.Ok)
		self.buttonOk.pack(padx=5, pady=5)
		frame1 = Frame(frame0)
		frame1.pack(expand=TRUE, fill=BOTH)
		labelTitle = Label(frame1, text='Burma-Keyboard',
							font=('Sans', 16, 'bold'))
		labelTitle.grid(row=0, column=0, sticky=W, padx=10, pady=10)
		description = "Myanmar Font and XKeyboard Installer" + 2*'\n'
		labelDesc = Label(frame1, text=description, justify=LEFT)
		labelDesc.grid(row=2, column=0, sticky=W, columnspan=3, padx=10, pady=5)
		labelEmail = Label(frame1, text='email:	phonehtut2@gmail.com',
							justify=LEFT)
		labelEmail.grid(row=6, column=0, columnspan=2, sticky=W, padx=10, pady=5)
		labelWWW = Label(frame1, text='www:	http://zawgyi-keyboard.googlecode.com',
							justify=LEFT)
		labelWWW.grid(row=7, column=0, columnspan=2, sticky=W, padx=10, pady=5)
		# button group 0		
		button_grp0 = Frame(frame1)
		button_grp0.grid(row=10, column=0, columnspan=2, sticky=NSEW)
		## License Button
		buttonLicense = Button(button_grp0, text='License', width=8,
								command=self.ShowLicense)
		buttonLicense.pack(side=LEFT, padx=10, pady=10)
		## Copyright Button
		buttonCopyright = Button(button_grp0, text='Copyright', width=8,
								command=self.ShowCopyright)
		buttonCopyright.pack(side=LEFT, padx=10, pady=10)
		## Credits Button
		buttonCredits = Button(button_grp0, text='Credits', width=8,
								command=self.ShowCredits)
		buttonCredits.pack(side=LEFT, padx=10, pady=10)
		# button group 1
		button_grp1 = Frame(frame1)
		button_grp1.grid(row=13, column=0, columnspan=3, sticky=NSEW)
		## ReadMe Button
		buttonReadMe = Button(button_grp1, text='README', width=8,
								command=self.ShowReadMe)
		buttonReadMe.pack(side=LEFT, padx=10, pady=10)
		## Authors Button
		buttonAuthors = Button(button_grp1, text='Authors', width=8,
								command=self.ShowAuthors)
		buttonAuthors.pack(side=LEFT, padx=10, pady=10)
		## Changelog Button
		buttonChangelog = Button(button_grp1, text='Changelog', width=8,
								command=self.ShowChangelog)
		buttonChangelog.pack(side=LEFT, padx=10, pady=10)

	def ShowLicense(self):
		self.display_text_file('About - License', 'LICENSE')
	
	def ShowCopyright(self):
		self.display_text_file('About - Copyright', 'COPYRIGHT')

	def ShowCredits(self):
		self.display_text_file('About - Credits', 'CREDITS')

	def ShowReadMe(self):
		self.display_text_file('About - Readme', 'README')

	def ShowAuthors(self):
		self.display_text_file('About - Authors', 'AUTHORS')

	def ShowChangelog(self):
		self.display_text_file('About - Changelog', 'changelog')

	def display_text_file(self, title, filename):
		fn = os.path.join(os.getcwd(), filename)
		text_view.view_file(self, title, fn)

	def Ok(self, event=None):
		self.destroy()

if __name__ == '__main__':
	# test
	root = Tk()
	def run():
		import aboutdialog
		aboutdialog.AboutDialog(root, 'About')
	Button(root, text='Dialog', command=run).pack()
	root.mainloop()

