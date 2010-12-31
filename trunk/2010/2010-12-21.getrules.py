#!/usr/bin/env python

import os
import sys

def getrules(listofrulefiles):
    """Makes a consolidated list of rules, each rule itself a list of components.
        Argument: list of rule files (if only a list of just one item).
        Parses raw rules into fields, deleting comments and blank lines."""
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
                print 'Fields 2, 3, and 4 must be non-empty - exiting...'
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
        try:
            open(targetfilename, 'a+').close()  # like "touch", ensures that sourcefile exists
        except:
            print 'Cannot open', targetfilename, 'as a file for appending - exiting...'
            sys.exit()
        count = count + 1
    return listofrulesparsed

if __name__ == "__main__":
    rules = getrules(['testdata/.ruleall', 'testdata/.rules'])
    #for rule in parsedrules:
    #    for line in listofdatalines:
    #        splitline = line.split()
    #        print splitline[1]

