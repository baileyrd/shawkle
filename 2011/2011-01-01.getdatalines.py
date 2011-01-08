#!/usr/bin/env python

from __future__ import division
import os
import re
import shutil
import string
import sys

def getdatalines(datafileslisted):
    alldatalines = []
    for file in datafileslisted:
        try:
            openfile = open(file, 'r')
            openfilelines = openfile.readlines()
            for line in openfilelines:
                if len(line) == 1:
                    print 'File', file, 'has blank lines - exiting...'
                    sys.exit()
        except:
            print 'Cannot open', file, '- exiting...'
            sys.exit()
        openfile.close()
    for file in datafileslisted:
        openfile = open(file, 'r')
        openfilelines = openfile.readlines()
        for line in openfilelines:
            alldatalines.append(line)
        openfile.close()
        shutil.move(file, '.backup')
    alldatalines.sort()
    return alldatalines

if __name__ == "__main__":
    datalines = getdatalines(['huh.txt', 'malendar.txt'])
    print datalines
