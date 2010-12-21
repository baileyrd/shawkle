#!/usr/bin/env python

import os
import sys
import string
import sys
import shutil
import shawkle

def stringblockistext(s, threshold=0.30):
    """Tests whether a given string consists of text or not.  
        Used in fileistextfile().  From: Python Cookbook, p.25.
    Takes as arguments:
        "s" - a string
        Optional "threshold" -
            proportion of the string that can be non-text characters before the string 
            is considered not to be text.  Default is 30%.
    Calls:
        string.maketrans()
    Called by:
        fileistextfile()
    Requires:
        import string"""
    text_characters = "".join(map(chr, range(32, 127))) + "\n\r\t\b"
    _null_trans = string.maketrans("", "")
    if "\0" in s:     # if s contains any null, it's not text
        return False
    if not s:         # an "empty" string is "text" (arbitrary but reasonable choice)
        return True
    t = s.translate(_null_trans, text_characters) # Get the substring of s made up of non-text characters
    return len(t)/len(s) <= threshold             # s is 'text' if less than 30% of its characters are non-text ones

def fileistextfile(filename, blocksize=512):
    """Tests whether a given file consists of text.
        Does this by reading block of characters at beginning of file.
    Takes as arguments:
        filename
        blocksize - default is 512 bytes
    Calls:
        stringblockistext()  
        open(filename).read(blocksize)
    Ends program with error message:
        If character block does not pass test.
    Returns:
        Nothing returned ("fruitless" function)."""
    if not stringblockistext(open(filename).read(blocksize)):
        print filename, 'is not a text file.  Exiting...'
        sys.exit()

def datals():
    """Takes as argument
        none - by default looks at $PWD/*
    Returns:
        List of files in current directory, 
        excluding dot files and subdirectories.
    Ends program with error message:
        On encountering a file ending in .swp or .lock.
    Calls:
        os.listdir() os.getcwd() os.path.isfile()
        sys.exit
    """
    filelist = []
    pathnamelist = os.listdir(os.getcwd())
    for pathname in pathnamelist:
        if os.path.isfile(pathname) == True:
            if pathname[0] != ".":
                if pathname[-3:] == "swp":
                    print pathname, 'is apparently a swap file.  Exiting...'
                    sys.exit()
                if pathname[-4:] == "lock":
                    print pathname, 'is apparently a lock file.  Exiting...'
                    sys.exit()
                filelist.append(pathname)
    return filelist

def datalines(datafileslisted):
    """Takes as argument: 
        List of data files.
    What it does:
        Checks to make sure the file is really a 'text file'.
        Creates list of all lines in all of the data files.
    Exits with error message:
        On encountering a file with blank lines.
    Returns:
        List of all lines from all (plain-text) files in the working directory.
    Calls:
        mustbelist()
        fileistextfile()
        open(file).readlines() - reads in whole file at once and splits by line
        LIST.append()
        sys.exit
    """
    mustbelist(datafileslisted)
    alldatalines = []
    for file in datafileslisted:
        fileistextfile(file)
        fin = open(file).readlines()
        for line in fin:
            if len(line) == 1:
                print 'file', file, 'has blank lines.  Exiting...'
                sys.exit()
            else:
                alldatalines.append(line)
    return alldatalines

def datasize(alldatalines):
    """Compute aggregate size of a given list of data lines. 
    Takes as argument:
        alldatalines - variable represents a list of data lines
    Calls:
        shawkle.mustbelist()
        sys.exit()
    Exits with error message:
        If computed size is zero.
    Returns:
        datasize - an integer (number of bytes)."""
    mustbelist(alldatalines)
    datasize = 0
    for line in alldatalines:
        datasize = datasize + len(line)
    if datasize == 0:
        print 'No data to process?'
        sys.exit()
    return datasize

def mustbelist(argument):
    if type(argument) != list:
        print 'Argument be a list, if only a list of one.  Exiting...'
        sys.exit()

def databackup(datals):
    """Backs up list of files to directory ".backup".
        Rotates contents of backup directories:
            ".backupii" to ".backupiii"
            ".backupi" to ".backupii"
            ".backup" to ".backupi"
    Takes as argument:
        none - by default looks at $PWD/*
    """
    mustbelist(datals)
    backupdirs = ['.backup', '.backupi', '.backupii', '.backupiii']
    for dir in backupdirs:
        if not os.path.isdir(dir):
            os.mkdir(dir)
    shutil.rmtree(backupdirs[3])
    print 'Removing', backupdirs[3]
    shutil.move(backupdirs[2], backupdirs[3])
    print 'Moving contents of', backupdirs[2], "to", backupdirs[3]
    shutil.move(backupdirs[1], backupdirs[2])
    print 'Moving contents of', backupdirs[1], "to", backupdirs[2]
    shutil.move(backupdirs[0], backupdirs[1])
    os.mkdir(backupdirs[0])
    for file in datals:
        print 'Moving to', backupdirs[0], ":", file
        shutil.move(file, backupdirs[0])

def mklistofrulesraw(listofrulefiles):
    """Makes a consolidated list of rules
        Each rule is itself a list of five components.
    First argument is a list of rule files (if only a list of just one item).
    Parses raw rules into fields, deleting comments and blank lines."""
    mustbelist(listofrulefiles)
    listofrulesraw = []
    for file in listofrulefiles:
        try:
            lines = open(file, 'rU').readlines()
            listofrulesraw.extend(lines)
        except:
            print 'Rule file', file, 'does not exist.  Exiting...'
            sys.exit()
    return listofrulesraw

def mklistofrulesparsed(listofrulesraw):
    listofrulesparsed = []
    for line in listofrulesraw:
        listofulesparsed.append(line)
    return listofrulesparsed

        # w = line.strip()
        # y = w.partition('#')[0]
        # z = y.rstrip()
        # x = z.split('|')
        # if len(x) == 5:
        #     try:
        #         x[0] = int(x[0])
        #     except:
        #         print x
        #         print 'First field must be an integer.  Exiting...'
        #         sys.exit()
        #     if len(x[1]) > 0:
        #         if len(x[2]) > 0:
        #             if len(x[3]) > 0:
        #                 listofrules.append(x)
        #     else:
        #         print x
        #         print 'Fields 2, 3, and 4 must be non-empty.  Exiting...'
        #         sys.exit()

def rulesanitycheck(parsedrules):
    """Check rules for sanity."""
    # Maybe this function should create a dictionary!
    sourcefiles = []
    targetfiles = []
    count = 0
    for line in parsedrules:
        if count == 0:  # Ensures that _first_ sourcefilename is listed even in absence of precedent targetfilename.
            sourcefilename = line[2]
            targetfiles.append(sourcefilename)
        count = count + 1
        searchfield = line[0]
        searchkey = line[1]
        sourcefilename = line[2]
        targetfilename = line[3]
        targetfiles.append(targetfilename)
        sortorder = line[4]
        if sourcefilename in targetfiles:
            pass  
        else:
            print sourcefilename
            print 'The sourcefilename has no precedent targetfilename.  Exiting...'
            sys.exit()

def getrulecomponents(parsedrules):
    """For each rule in listofrules, return parsed rule."""
    mustbelist(parsedrules)
    for line in parsedrules:
        searchfield = line[0]
        searchkey = line[1]
        sourcefilename = line[2]
        targetfilename = line[3]
        sortorder = line[4]
        x = (searchfield, searchkey, sourcefilename, targetfilename)
        print "%-2s %-15s %-15s %-15s" % x
        return x

def datacleanup():
    listofdatafiles = datals()
    for file in listofdatafiles:
        if os.path.getsize(file) == 0:
            os.remove(file)

if __name__ == "__main__":
    os.chdir('/home/tbaker/u/scripts/PYFFLE/shawkle/testdata')
    listofdatafiles = shawkle.datals()
    listofdatalines = shawkle.datalines(listofdatafiles)
    listofdatalinestoconsume = listofdatalines
    rulesraw = shawkle.mklistofrulesraw(['./.ruleall', './.rules'])
    parsedrules = mklistofrulesparsed(rulesraw)
    rulecomponents = getrulecomponents(parsedrules)
    for rule in rulesraw:
        for line in listofdatalines:
            splitline = line.split()
            print splitline[1]






## #######################################
## 
##     # listofdatalinesfielded = shawkle.datalinesfielded(listofdatalines)
## 
## # 2010-12-19 This is not actually necessary if refer to, say, line[2] in listofdatalines
## # def datalinesfielded(listofdatalines):
## #     for line in listofdatalines:
## #         fieldedline = line.split()
## #         listofdata...
## 
## # From main
## 
##     #datalsafter = datals('combined.dat')
##     #datalinesafter = datalines(datalsafter)
##     #datasizeafter = datasize(datalinesafter)
##     # Compares aggregate size of data before and after and reports discrepancies."""
##     #if datasizebefore == datasizeafter:
##     #    print "Done: data shuffled and intact!"
##     #else:
##     #    print 'Size before:', datasizebefore
##     #    print 'Size after:', datasizeafter
##     #    print "Warning: data may have been lost--use backup!"
## 
##     # datasizebefore = shawkle.datasize(listofdatalines)
##     # rulesanitycheck(parsedrules)
##     # databackup(listofdatafiles)
##     # datashuffle(parsedrules, listofdatalines)
##     # datacleanup()
## 
## # From datashuffle
##             #if line[0] == 0:
##             #    print 'searchfield in line 1 is zero'
##             #if line[0]  == 1:
##             #    print 'searchfield in line 1 is 1'
##             #else:
##             #    print 'line is neither'
## 
##         # 1/0
##         #     #    #print searchkey, searchfield
##         #     if searchkey in ' '.join(line):
##         #         targetfile.write(listofdatalines.pop(number)) # pop line, appending to to targetfilename
##         #     else:
##         #         sourcefile.write(listofdatalines.pop(number)) # pop line, appending to new sourcefile
##         #         # or something like: sourcefile.write(line)
##         # targetfile.close()
##         # sourcefile.close()
## 
##         #for dataline in listofdatalines:
##         #    if searchkey in dataline[:]:     # or listofdatalines[0] (if field 1 is 1)...
##         #        # This is okay for testing, but clearly need to replace ":" with searchfield
##         #        # if searchkey in x[searchkey-1]:  # "0" to be replaced with regular expression using searchfield
##         #        # if searchkey in linestripped[searchfield-1] == True: # searchkey matches field# searchfield minus 1
##         #        targetfile.write(listofdatalines.pop(number)) # pop line, appending to to targetfilename
##         #        number = number + 1
##         #number = 0
##         #for dataline in listofdatalines: # for all remaining lines (lines that do not have searchkey in searchfield)
##         #    number = number + 1
## 
## 
## # From initial declarations
##     # from __future__ import division     # overrides existing division function - this does NOT truncate
##     # import tempfile

# 2010-12-21 def datashuffle(parsedrules, listofdatalines):
# 2010-12-21     """Perform data shuffle, reporting success or error.
# 2010-12-21     Arguments are:
# 2010-12-21     -- parsedrules: a list of rules, already created and verified
# 2010-12-21     -- listofdatalines, handle for a list of data lines (already aggregated from all data files in directory)."""
# 2010-12-21     mustbelist(parsedrules)
# 2010-12-21     mustbelist(listofdatalines)
# 2010-12-21     for iteration in range[1]:
# 2010-12-21         for line in parsedrules:
# 2010-12-21             searchfield = line[0]
# 2010-12-21             searchkey = line[1]
# 2010-12-21             sourcefilename = line[2]
# 2010-12-21             targetfilename = line[3]
# 2010-12-21             sortorder = line[4]
# 2010-12-21             ## sourcefile = open(sourcefilename, 'a+').close()   # like "touch", to ensure that sourcefile exists
# 2010-12-21             ## sourcefile = open(sourcefilename, 'r')  # sourcefilemust already exist, opened in read-only mode
# 2010-12-21             for line in sourcefile:       # iterate to split each line into awk-like "fields"
# 2010-12-21                   listofdatalines.append(line)
# 2010-12-21                   # what about: sourcefile = open(sourcefilename, 'a+').readlines()  # first open source file for reading?
# 2010-12-21                   # or something like: listofdatalines = open(sourcefilename, 'r').readlines()
# 2010-12-21             ## sourcefile.close() # once lines sucked from sourcefile, readable sourcefile no longer needed
# 2010-12-21             ## sourcefile = open(sourcefilename, 'w')     # opened write-only, overwritten if exists, else created
# 2010-12-21             ## targetfile = open(targetfilename, 'a+')    # opened for reading/writing, kept intact, appended, maybe created
# 2010-12-21             print "%-2s %-15s %-15s %-15s" % (searchfield, searchkey, sourcefilename, targetfilename)
# 2010-12-21             number = 0
# 2010-12-21             for line in listofdatalines:
# 2010-12-21                 print line
