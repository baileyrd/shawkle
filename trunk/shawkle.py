#!/usr/bin/env python

from __future__ import division
import os
import re
import shutil
import string
import sys

def datals():
    """Returns list of files in current directory, excluding dot files and subdirectories.
        Ends program with error message on encountering a file ending in .swp."""
    filelist = []
    pathnamelist = os.listdir(os.getcwd())
    for pathname in pathnamelist:
        if os.path.isfile(pathname):
            if pathname[-3:] == "swp":
                print 'Detected swap file', pathname, '- which should be closed before proceeding - exiting...'
                sys.exit()
            if pathname[0] != ".":
                filelist.append(pathname)
    return filelist

def datamovetobackup(filelist):
    """Backs up list of files in $PWD to ".backup", bumping previous to ".backupi", ".backupii", ".backupiii"."""
    if not filelist:
        print 'No data here to back up, or process... - exiting...'
        sys.exit()
    backupdirs = ['.backup', '.backupi', '.backupii', '.backupiii']
    for dir in backupdirs:
        if not os.path.isdir(dir):
            os.mkdir(dir)
    print 'Deleting directory', backupdirs[3]
    shutil.rmtree(backupdirs[3])
    print 'Moving directory', backupdirs[2], "to", backupdirs[3]
    shutil.move(backupdirs[2], backupdirs[3])
    print 'Moving directory', backupdirs[1], "to", backupdirs[2]
    shutil.move(backupdirs[1], backupdirs[2])
    print 'Moving directory', backupdirs[0], "to", backupdirs[1]
    shutil.move(backupdirs[0], backupdirs[1])
    os.mkdir(backupdirs[0])
    for file in filelist:
        print 'Moving file', file, "to", backupdirs[0]
        shutil.move(file, backupdirs[0])

def totalsize():
    totalsize = 0
    listoffiles = os.listdir(os.getcwd())
    for file in listoffiles:
        if os.path.isfile(file):
            filesize = os.path.getsize(file)
            if filesize == 0:
                print 'Removing zero-length file:', file
                os.remove(file)
            else:
                if file[0] != ".":
                    totalsize = totalsize + filesize
    return totalsize

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
    createdfiles = []
    count = 0
    for rule in listofrulesparsed:
        sourcefilename = rule[2]
        targetfilename = rule[3]
        createdfiles.append(targetfilename)
        if count == 0:
            createdfiles.append(sourcefilename)
        if sourcefilename == targetfilename:
            print 'In rules:', rule
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
    listofdatafiles = datals()
    print 'list of data files is:', listofdatafiles
    ckfilesaretext(listofdatafiles)
    sizebefore = totalsize()
    datalines = getdatalines(listofdatafiles)
    print datalines
    rules = getrules(['.ruleall', '.rules'])
    print rules
    #datamovetobackup(listofdatafiles)
    #count = 0
    #for rule in rules:
    #    searchfield = rule[0]
    #    searchkey = rule[1]
    #    source = rule[2]
    #    target = rule[3]
    #    if count > 0:
    #        data = datalines
    #    else:
    #        with open(source, 'r') as datatoread:
    #            data = datatoread.readlines()
    #    sourcefile = open(source, 'w')
    #    targetfile = open(target, 'a')
    #    print "%-10s %-10s %-10s %-10s" % (searchfield, searchkey, source, target)
    #    if searchfield == 0:
    #        sourcefile.writelines([ dataline for dataline in data if re.match(searchkey, dataline) ])
    #        sourcefile.writelines([ dataline for dataline in data if not re.match(searchkey, dataline) ])
    #    else:
    #        searchfield = searchfield - 1
    #        sourcefile.writelines([ dataline for dataline in data if searchkey in dataline.split()[searchfield] ])
    #        targetfile.writelines([ dataline for dataline in data if not searchkey in dataline.split()[searchfield] ])
    #    sourcefile.close()
    #    targetfile.close()

#    sizeafter = totalsize()
#    print 'size of files before was:', sizebefore
#    print 'size of files after is:', sizeafter

# Notes:
# 2010-12-25
#    sourcefile.writelines([ dataline for dataline in data if re.match(searchkey, dataline) ])
#    sourcefile.writelines([ dataline for dataline in data if re.search(searchkey, dataline) ])
#    - "search" matches anywhere, "match" matches at start of string
#    - typically, want to assume start of string
#    - but what about if "^AGENDA" is supposed to come after "^A "...?
#    Next: maybe need to test for list?
#        def mustbelist(argument):
#            if type(argument) != list:
#                print 'Argument be a list, if only a list of one.  Exiting...'
#                sys.exit()
