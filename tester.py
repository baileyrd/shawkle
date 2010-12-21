#!/usr/bin/env python

import os
import sys

def getrules(listofrulefiles):
    listofrulesraw = []
    for file in listofrulefiles:
        try:
            lines = open(file, 'rU').readlines()
            listofrulesraw.extend(lines)
        except:
            print 'Rule file', file, 'does not exist.  Exiting...'
            sys.exit()
    listofrulesparsed = []
    for line in listofrulesraw:
        linestripped = line.strip()
        linedecommented = linestripped.partition('#')[0]
        linewithouttrailingwhitespace = linedecommented.rstrip()
        linesplitonorbar = linewithouttrailingwhitespace.split('|')
        if len(linesplitonorbar) == 5:
            try:
                linesplitonorbar[0] = int(linesplitonorbar[0])
            except:
                print linesplitonorbar
                print 'First field must be an integer.  Exiting...'
                sys.exit()
            if len(linesplitonorbar[1]) > 0:
                if len(linesplitonorbar[2]) > 0:
                    if len(linesplitonorbar[3]) > 0:
                        listofrulesparsed.append(linesplitonorbar)
            else:
                print linesplitonorbar
                print 'Fields 2, 3, and 4 must be non-empty.  Exiting...'
                sys.exit()
    targetfiles = []
    count = 0
    for rule in listofrulesparsed:
        sourcefilename = rule[2]
        targetfilename = rule[3]
        targetfiles.append(targetfilename)
        if not count == 0:
            if not sourcefilename in targetfiles:
                print sourcefilename
                print 'The sourcefilename has no precedent targetfilename.  Exiting...'
                sys.exit()
        count = count + 1
    return listofrulesparsed

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
    rules = getrules(['testdata/.ruleall', 'testdata/.rules'])
    #
    listofdatafiles = ['testdata/calendar.txt', 'testdata/huh.txt']
    listofdatalines = datalines(listofdatafiles)
    #
    #for rule in parsedrules:
    #    for line in listofdatalines:
    #        splitline = line.split()
    #        print splitline[1]

