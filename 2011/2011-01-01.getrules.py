#!/usr/bin/env python

from __future__ import division
import os
import re
import shutil
import string
import sys

def getrules(listofrulefiles):
    """Makes a consolidated list of rules, each rule itself a list of components.
        Argument: list of rule files (if only a list of just one item).
        Parses raw rules into fields, deleting comments and blank lines."""
    listofrulesraw = []
    for file in listofrulefiles:
        try:
            openrulefile = open(file, 'rU')
            openrulefilelines = openrulefile.readlines()
            listofrulesraw.extend(openrulefilelines)
        except:
            print 'Rule file', file, 'does not exist.  Exiting...'
            sys.exit()
        openrulefile.close()
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
    createdfiles = []
    count = 0
    for rule in listofrulesparsed:
        sourcefilename = rule[2]
        targetfilename = rule[3]
        createdfiles.append(targetfilename)
        if count == 0:
            createdfiles.append(sourcefilename)
        if sourcefilename == targetfilename:
            print 'In rule:', rule
            print 'SourceFile:', sourcefilename, '...is the same as TargetFile:', targetfilename, '-- exiting...'
            sys.exit()
        if not sourcefilename in createdfiles:
            print rule
            print 'The sourcefilename', sourcefilename, 'has no precedent targetfilename.  Exiting...'
            sys.exit()
        try:
            open(sourcefilename, 'a+').close()  # like "touch", ensures that sourcefile is writable
            open(targetfilename, 'a+').close()  # like "touch", ensures that targetfile is writable
        except:
            print 'Cannot open', sourcefilename, 'or', targetfilename, 'as a file for appending - exiting...'
            sys.exit()
        count = count + 1
    return listofrulesparsed

if __name__ == "__main__":
    rules = getrules(['.ruleall', '.rules'])
    print rules
