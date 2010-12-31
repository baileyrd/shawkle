#!/usr/bin/env python

from __future__ import division
import os
import sys
import string

def getdatalines(datafileslisted):
    alldatalines = []
    for file in datafileslisted:
        try:
            fin = open(file).readlines()
        except:
            print 'Cannot open', file, '-- exiting...'
            sys.exit()
        fin = open(file).readlines()
        for line in fin:
            if len(line) == 1:
                print 'File', file, 'has blank lines - exiting...'
                sys.exit()
            else:
                alldatalines.append(line)
    alldatalines.sort()
    return alldatalines

def ckfilesaretext(datafiles):
    """Tests whether a file consists of text - see Python Cookbook, p.25."""
    for file in datafiles:
        givenstring = open(file).read(512)
        text_characters = "".join(map(chr, range(32, 127))) + "\n\r\t\b"
        _null_trans = string.maketrans("", "")
        if "\0" in givenstring:     # if givenstring contains any null, it's not text
            print file, 'contains a null and is therefore not a text file - exiting...'
            sys.exit()
        if not givenstring:         # an "empty" string is "text" (arbitrary but reasonable choice)
            return True
        substringwithnontextcharacters = givenstring.translate(_null_trans, text_characters)
        lengthsubstringwithnontextcharacters = len(substringwithnontextcharacters)
        lengthgivenstring = len(givenstring)
        proportion = lengthsubstringwithnontextcharacters / lengthgivenstring
        if proportion >= 0.30: # s is 'text' if less than 30% of its characters are non-text ones
            print file, 'has more than 30% non-text characters and is therefore not a text file - exiting...'
            sys.exit()

if __name__ == "__main__":
    datafiles = ['testdata/calendar.txt', 'testdata/huh.txt']
    ckfilesaretext(datafiles)
    datalines = getdatalines(datafiles)

    #for rule in parsedrules:
    #    for line in listofdatalines:
    #        splitline = line.split()
    #        print splitline[1]
    # rules = [[0, '.', 'combined.data', 'lines', ''], [0, '^2010-.. ', 'lines', 'agenday', ''], [0, '^A ', 'lines', 'agendaa', ''], [0, '.', 'lines', 'HUH.txt', ''], [0, '.', 'agendaa', 'HUH.txt', ''], [1, '^=2', 'HUH.txt', 'calendar.txt', ''], [1, 'LATER', 'HUH.txt', 'LATER.txt', ''], [1, 'NOW', 'HUH.txt', 'NOW.txt', '']]


# def mustbelist(argument):
#     if type(argument) != list:
#         print 'Argument be a list, if only a list of one.  Exiting...'
#         sys.exit()

