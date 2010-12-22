#!/usr/bin/env python

import os
import sys

def datalines(datafileslisted):
    alldatalines = []
    for file in datafileslisted:
        fin = open(file).readlines()
        for line in fin:
            if len(line) == 1:
                print 'file', file, 'has blank lines.  Exiting...'
                sys.exit()
            else:
                alldatalines.append(line)
    return alldatalines

def getrulecomponents(parsedrules):
    """For each rule in listofrules, return parsed rule."""
    for line in parsedrules:
        searchfield = line[0]
        searchkey = line[1]
        sourcefilename = line[2]
        targetfilename = line[3]
        sortorder = line[4]
        x = (searchfield, searchkey, sourcefilename, targetfilename)
        print "%-2s %-15s %-15s %-15s" % x
        return x

if __name__ == "__main__":
    rules = [[0, '.', 'combined.data', 'lines', ''], [0, '^2010-.. ', 'lines', 'agenday', ''], [0, '^A ', 'lines', 'agendaa', ''], [0, '.', 'lines', 'HUH.txt', ''], [0, '.', 'agendaa', 'HUH.txt', ''], [1, '^=2', 'HUH.txt', 'calendar.txt', ''], [1, 'LATER', 'HUH.txt', 'LATER.txt', ''], [1, 'NOW', 'HUH.txt', 'NOW.txt', '']]
    #
    listofdatafiles = ['testdata/calendar.txt', 'testdata/huh.txt']
    listofdatalines = datalines(listofdatafiles)
    #
    #for rule in parsedrules:
    #    for line in listofdatalines:
    #        splitline = line.split()
    #        print splitline[1]

