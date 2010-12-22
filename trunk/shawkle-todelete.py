#!/usr/bin/env python

import os
import sys
import string
import sys
import shutil
import shawkle

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
