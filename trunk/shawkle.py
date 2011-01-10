#!/usr/bin/env python

from __future__ import division
from __future__ import with_statement
import os
import re
import shutil
import string
import sys
import datetime

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

def databackup(filelist):
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
    #2011-01-01: will move files to .backup only in slurpdata() function now
    #for file in filelist:
    #    print 'Copying file', file, "to", backupdirs[0]
    #    shutil.copy2(file, backupdirs[0])

def totalsize():
    totalsize = 0
    listoffiles = os.listdir(os.getcwd())
    for file in listoffiles:
        if os.path.isfile(file):
            filesize = os.path.getsize(file)
            if filesize == 0:
                # print 'Removing zero-length file:', file # MAYBE RESTORE THIS
                os.remove(file)
            else:
                if file[0] != ".":
                    totalsize = totalsize + filesize
    return totalsize

def slurpdata(datafileslisted):
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

def ckthatfilesaretext(datafiles):
    """Tests whether a file consists of text; exits if not - based on Python Cookbook, p.25."""
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
            openrulefile = open(file, 'rU')
            openrulefilelines = openrulefile.readlines()
            listofrulesraw.extend(openrulefilelines)
        except:
            print 'Rule file', file, 'does not exist - exiting...'
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
                print 'First field must be an integer - exiting...'
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
            print 'SourceFile:', sourcefilename, '...is the same as TargetFile:', targetfilename, '- exiting...'
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

def datacleanup():
    listofpathnames = os.listdir(os.getcwd())
    for file in listofpathnames:
        if os.path.isfile(file):
            if os.path.getsize(file) == 0:
                os.remove(file)
                # print 'Removing zero-length file:', file # MAYBE restore this

def getfilemappings(filemappings):
    mappingsraw = []
    try:
        mappings = open(filemappings, 'rU')
        mappingsraw = mappings.readlines()
    except:
        print 'Mapping file', filemappings, 'does not exist - exiting...'
        sys.exit()
    mappings.close()
    mappingsparsed = []
    for line in mappingsraw:
        linestripped = line.strip()
        linedecommented = linestripped.partition('#')[0]
        linewithouttrailingwhitespace = linedecommented.rstrip()
        linesplitonorbar = linewithouttrailingwhitespace.split('|')
        if len(linesplitonorbar) == 2:
            mappingsparsed.append(linesplitonorbar)
    return mappingsparsed

def movefiles(filemappings):
    timestamp = datetime.datetime.now()
    prefix = timestamp.isoformat('.')
    for line in filemappings:
        filename = line[0]
        dirpath = line[1]
        timestampedpathname = dirpath + '/' + prefix[0:13] + prefix[14:16] + prefix[17:19] + '.' + filename
        try:
            shutil.move(filename, timestampedpathname)
            print 'Moving', filename, 'to', timestampedpathname
        except:
            if os.path.exists(filename):
                print 'Keeping', filename, 'where it is - directory', dirpath, 'does not exist...'
            else:
                #print 'File', filename, 'does not exist...' # MAYBE RESTORE THIS
                pass

if __name__ == "__main__":
    datacleanup()
    listofdatafiles = datals()
    ckthatfilesaretext(listofdatafiles)
    sizebefore = totalsize()
    rules = [[0, '^2010-', 'aaa.txt', '2010.txt', ''],
     [0, '^A ', 'aaa.txt', 'agendaa.txt', ''],
     [0, '.', 'aaa.txt', 'HUH.txt', ''],
     [7, '=2', 'HUH.txt', 'calendar.txt', ''],
     [1, 'LATER', 'HUH.txt', 'LATER.txt', ''],
     [1, 'NOW', 'HUH.txt', 'NOW.txt', '']]
    rules = getrules(['/home/tbaker/u/scripts/PYFFLE/shawkle/.ruleall', '.rules'])
    databackup(listofdatafiles)
    datalines = ['2010-02 To be archived...\n',
     '=2010-02-15\n',
     '=2010-02-15 Tue 1400 TELECON\n',
     '=2010-02-15 Tue 1900 RDF2 http://decentralyze.com/2009/10/30/rdf-2-wishlist/\n',
     '=2010-02-17 Wed 0800 TELECON\n',
     '=2010-08-24 Tue 0800 TELECON\n',
     'A LATER Belongs in agendaa\n',
     'LATER Haircut\n',
     'LATER http://www.asis.org/\n',
     'NOW Buy milk\n',
     'NOW Shovel snow\n']
    datalines = slurpdata(listofdatafiles)
    rulenumber = 0
    for rule in rules:
        rulenumber += 1
        field = rule[0]
        searchkey = rule[1]
        source = rule[2]
        target = rule[3]
        print '%s [%s] "%s" to "%s"' % (field, searchkey, source, target)
        if rulenumber == 1:
            data = datalines
        else:
            readonlysource = open(source, 'r')
            data = readonlysource.readlines()
            readonlysource.close()
        sfile = open(source, 'w')
        tfile = open(target, 'a')
        if field == 0:
            if searchkey == ".":
                tfile.writelines([ line for line in data ])
            else:
                sfile.writelines([ line for line in data if not re.search(searchkey, line) ])
                tfile.writelines([ line for line in data if re.search(searchkey, line) ])
        else:
            ethfield = field - 1
            for line in data:
                if field > len(line.split()):
                    sfile.write(line)
                else:
                    if re.search(searchkey, line.split()[ethfield]):
                        tfile.write(line)
                    else:
                        sfile.write(line)
        sfile.close()
        tfile.close()
    datacleanup()
    sizeafter = totalsize()
    print 'Size before is', sizebefore
    print 'Size after is', sizeafter
    if sizebefore == sizeafter:
        print 'Done: data shawkled and intact!'
    else:
        print 'Warning: data may have been lost - revert to backup!'
    filemappings = getfilemappings('/home/tbaker/u/scripts/PYFFLE/shawkle/.filemappings')
    movefiles(filemappings)

