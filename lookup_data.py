#!/user/bin/env python
# -*- coding: utf-8 -*-
""" lookup_data.py is a module to look up fonts data.

"""
""" This file is part of burma-keyboard.

"""

def find_details(name2find):
    fonts_f = open("fonts_data.csv")
    for each_line in fonts_f:
        s = {} # this is hash table called dictionary
        (s['fontname'],s['fontfolder'],s['email']) = each_line.split(",")
        if name2find == s['fontfolder']:
            fonts_f.close()
            return (s)
    fonts_f.close
    return({})

if __name__ == '__main__':
	#Test this module
	# raw_input is required to change if porting to Python 3
	lookup_font = raw_input("Enter the name of fontfolder: ")
	font = find_details(lookup_font)
	if font:
	    print("Font Name:   	 " + font['fontname'])
	    print("Font Folder: 	 " + font['fontfolder'])
	    print("Email in mm file: " + font['email'])

