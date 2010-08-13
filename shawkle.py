#!/usr/bin/env python


from __future__ import division     # overrides existing division function - this does NOT truncate
import os
import sys
import string
import sys
import shutil
import subprocess   # @@@@ for testing purposes
import tempfile

def stringblockistext(s, threshold=0.30):
    """Tests whether 's' (a string) is text or not.  Arguments:
    -- "s": a string
    -- optional "threshold": proportion  of string that can be non-text characters
       before the string is considered not to be text.  Default is 30%.
    See Python Cookbook, p. 25."""
    text_characters = "".join(map(chr, range(32, 127))) + "\n\r\t\b"
    _null_trans = string.maketrans("", "")        # ensure "import string"
    if "\0" in s:                                 # if s contains any null, it's not text
        return False
    if not s:                                     # an "empty" string is "text" (arbitrary but reasonable choice)
        return True
    t = s.translate(_null_trans, text_characters) # Get the substring of s made up of non-text characters
    return len(t)/len(s) <= threshold             # s is 'text' if less than 30% of its characters are non-text ones

def fileistextfile(filename, blocksize=512, **kwds):
    """Reads a block of characters (of length "blocksize", default 512 bytes)
    at the beginning of "filename".
    Calls "stringblockistext" function.  If character block does not pass test, says
    "x is not a text file" and exits."""
    if stringblockistext(open(filename).read(blocksize), **kwds) != True:
        print filename, 'is not a text file.  Exiting...'
        sys.exit()

def datals():
    """Return list of files in current directory, 
    excluding dot files and directories.
    Exits with error message if non-data files, or 
    files with swp or lock extensions are encountered."""
    filelist = []
    pathnamelist = os.listdir(os.getcwd())
    for pathname in pathnamelist:
        if os.path.isfile(pathname) == True:
            if pathname[0] != ".":
                if pathname[-3:] != "swp":
                    pass
                else:
                    print pathname, 'is apparently a swap file.  Exiting...'
                    sys.exit()
                if pathname[-4:] != "lock":
                    pass
                else:
                    print pathname, 'is apparently a lock file.  Exiting...'
                    sys.exit()
                filelist.append(pathname)
    return filelist

def datalines(datafileslisted):
    """Takes list of data files as argument.
    Checks to make sure the file is really a 'text file'.
    Creates list of all lines in all of the data files.
    Exits with error message if file with a blank line is encountered."""
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
    """Compute size of aggregate data lines. 
    Takes variable representing a list of data lines as argument.
    Returns an integer (i.e., the number of bytes)."""
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
    mustbelist(datals)
    backupdirs = ['.backup', '.backupi', '.backupii', '.backupiii']
    for dir in backupdirs:
        if os.path.isdir(dir) == False:
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

def getrawrules(listofrulefiles):
    """Creates a list of rules (each of which is a list of five components).
    First argument is a list of rule files (if only a list of just one item)."""
    mustbelist(listofrulefiles)
    rawrules = []
    for file in listofrulefiles:
        try:
            lines = open(file, 'rU').readlines()
            rawrules.extend(lines)
        except:
            print 'Rule file', file, 'does not exist.  Exiting...'
            sys.exit()
    return rawrules

def parserawrules(rawrules):
    """Parses raw rules into fields, deleting comments and blank lines."""
    mustbelist(rawrules)
    parsedrules = []
    for line in rawrules:
        w = line.strip()
        y = w.partition('#')[0]
        z = y.rstrip()
        x = z.split('|')
        if len(x) == 5:
            try:
                x[0] = int(x[0])
            except:
                print x
                print 'First field must be an integer.  Exiting...'
                sys.exit()
            if len(x[1]) > 0:
                if len(x[2]) > 0:
                    if len(x[3]) > 0:
                        parsedrules.append(x)
            else:
                print x
                print 'Fields 2, 3, and 4 must be non-empty.  Exiting...'
                sys.exit()
    return parsedrules

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

def datashuffle(parsedrules, listofdatalines):
    """Perform data shuffle, reporting success or error.
    Arguments are:
    -- parsedrules: a list of rules, already created and verified
    -- listofdatalines, handle for a list of data lines (already aggregated from all data files in directory)."""
    mustbelist(parsedrules)
    mustbelist(listofdatalines)
    for line in parsedrules:
        searchfield = line[0]
        searchkey = line[1]
        sourcefilename = line[2]
        targetfilename = line[3]
        sortorder = line[4]
        sourcefile = open(sourcefilename, 'a+').close()   # like "touch", to ensure that sourcefile exists
        sourcefile = open(sourcefilename, 'r')            # sourcefilemust already exist, opened in read-only mode
        for line in sourcefile:       # iterate to split each line into awk-like "fields"
              listofdatalines.append(line)
              # what about: sourcefile = open(sourcefilename, 'a+').readlines()  # first open source file for reading?
              # or something like: listofdatalines = open(sourcefilename, 'r').readlines()
        sourcefile.close() # once lines sucked from sourcefile to listofdatalines, readable sourcefile no longer needed
        sourcefile = open(sourcefilename, 'w')     # opened write-only, overwritten if exists, else created
        targetfile = open(targetfilename, 'a+')    # opened for reading/writing, kept intact, appended, maybe created
        print "%-2s %-15s %-15s %-15s" % (searchfield, searchkey, sourcefilename, targetfilename)
        number = 0
        for line in listofdatalines:
            print line

            #if line[0] == 0:
            #    print 'searchfield in line 1 is zero'
            #if line[0]  == 1:
            #    print 'searchfield in line 1 is 1'
            #else:
            #    print 'line is neither'
        # 1/0
        #     #    #print searchkey, searchfield
        #     if searchkey in ' '.join(line):
        #         targetfile.write(listofdatalines.pop(number)) # pop line, appending to to targetfilename
        #     else:
        #         sourcefile.write(listofdatalines.pop(number)) # pop line, appending to new sourcefile
        #         # or something like: sourcefile.write(line)
        # targetfile.close()
        # sourcefile.close()

        #for dataline in listofdatalines:
        #    if searchkey in dataline[:]:     # or listofdatalines[0] (if field 1 is 1)...
        #        # This is okay for testing, but clearly need to replace ":" with searchfield
        #        # if searchkey in x[searchkey-1]:  # "0" to be replaced with regular expression using searchfield
        #        # if searchkey in linestripped[searchfield-1] == True: # searchkey matches field# searchfield minus 1
        #        targetfile.write(listofdatalines.pop(number)) # pop line, appending to to targetfilename
        #        number = number + 1
        #number = 0
        #for dataline in listofdatalines: # for all remaining lines (lines that do not have searchkey in searchfield)
        #    number = number + 1

def datacleanup():
    listofdatafiles = datals()
    for file in listofdatafiles:
        if os.path.getsize(file) == 0:
            os.remove(file)

if __name__ == "__main__":
    listofdatafiles = datals()
    listofdatalines = datalines(listofdatafiles)
    listofdatalinesbefore = datalines(listofdatafiles)
    datasizebefore = datasize(listofdatalines)
    rawrules = getrawrules(['./.ruleall', './.rules'])
    parsedrules = parserawrules(rawrules)
    rulesanitycheck(parsedrules)
    # databackup(listofdatafiles)
    # datashuffle(parsedrules, listofdatalines)
    # datacleanup()

    #datalsafter = datals('combined.dat')
    #datalinesafter = datalines(datalsafter)
    #datasizeafter = datasize(datalinesafter)
    # Compares aggregate size of data before and after and reports discrepancies."""
    #if datasizebefore == datasizeafter:
    #    print "Done: data shuffled and intact!"
    #else:
    #    print 'Size before:', datasizebefore
    #    print 'Size after:', datasizeafter
    #    print "Warning: data may have been lost--use backup!"

