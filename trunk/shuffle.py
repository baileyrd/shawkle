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
        # sourcefiles.append(sourcefilename) # is this needed?
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
        sourcefile = open(sourcefilename, 'a+').close()   # the equivalent of "touch", to ensure that sourcefile exists
        sourcefile = open(sourcefilename, 'r')            # sourcefilemust already exist, opened in read-only mode
        for line in sourcefile:       # iterate to split each line into awk-like "fields"
              listofdatalines.append(line)
        sourcefile.close() # once lines sucked out of sourcefile, put into listofdatalines, sourcefile no longer needed
        sourcefile = open(sourcefilename, 'w')     # opened write-only, overwritten if exists, else created
        targetfile = open(targetfilename, 'a+')    # opened for reading/writing, kept intact, appended, maybe created
        number = 0
        for dataline in listofdatalines:
            if searchkey in dataline[:]:     # or listofdatalines[0] (if field 1 is 1)...
                # This is okay for testing, but clearly need to replace ":" with searchfield
                # if searchkey in x[searchkey-1]:  # "0" to be replaced with regular expression using searchfield
                # if searchkey in linestripped[searchfield-1] == True: # searchkey matches field# searchfield minus 1
                targetfile.write(listofdatalines.pop(number)) # pop line, appending to to targetfilename
                number = number + 1
        targetfile.close()
        number = 0
        for dataline in listofdatalines: # for all remaining lines (lines that do not have searchkey in searchfield)
            sourcefile.write(listofdatalines.pop(number)) # pop line, appending to new sourcefile
            number = number + 1
            # or something like: sourcefile.write(line)
            # or something like: listofdatalines = open(sourcefilename, 'r').readlines()
            # what about: sourcefile = open(sourcefilename, 'a+').readlines()  # first open the source file for reading

if __name__ == "__main__":
    # listofdatafiles = datals()
    # listofdatalines = datalines(listofdatafiles)
    # datasizebefore = datasize(listofdatalines)
    # databackup(listofdatafiles)  # in practice, would not want to do this until rules have passed the test
    # rawrules = getrawrules(['/home/tbaker/u/folders/PYTH/SHUFFLE/.ruleall', './.rules'])
    # parsedrules = parserawrules(rawrules)
    # rulesanitycheck(parsedrules)

    parsedrules = [['0', '.', 'foobar.dat', 'lines', 'sort -bdf'], ['0', '^2010-.. ', 'lines', 'agendaa', ''], ['0', '.', 'lines', 'HUH.txt', ''], ['0', '.', 'agendaa', 'HUH.txt', 'sort'], ['1', '^=$', 'HUH.txt', 'A.txt', ''], ['1', 'LATER', 'HUH.txt', 'B.txt', ''], ['1', '^=20', 'HUH.txt', 'calendar.txt', '']]

    listofdatalines = ['=2010-02-16 Tue 1400-1500 EST (1100-1200 PST) UWASHTELECON\n', '=2010-02-16 Tue 1900 RDF2 http://decentralyze.com/2009/10/30/rdf-2-wishlist/\n', '=2010-02-16 Tue 1900 RDF2 http://semweb.meetup.com/31/calendar/12335279/ \n', '=2010-02-17 Wed 0800 KIMTWR telecon\n', '=2010-02-24 Wed 0800 Jury Summons\n', '= http://www.w3.org/2009/07/skos-pr.html.en\n', 'FTMP e:/u/folders/DUTCH/VOCAMP/.index.html\n', '= e:/u/folders/+FTMP/Reading-notes-roy-on-rest.txt\n', 'WORK DC2009   e:/u/folders/DC/TUTORIAL - 0900-1030, 1100-1230\n']

    datashuffle(parsedrules, listofdatalines)




    #subprocess.call(["rm", "combined.dat"]) # @@@ for testing!
    #subprocess.call(["ls", "-l"])        # @@@ for testing!
    #datashuffle(rulelist, datalinesbefore, 'lines.txt', 'target.tmp')
    # print "%-2s %-10s %-10s %-10s" % (searchfield, searchkey, sourcefilename, targetfilename)
    #datacleanup()
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

# ----------------------------------------------------------------
# Sort field
# ----------------------------------------------------------------
# 1. what are the possible values for field 5 ("sort")?
#    for item in rulelist:
#        # sortorder must contain valid parameters for sort.
#        #     else print "X: sort parameters not valid."
#        #         print offending rule; exit
# if sortorder (for targetfilename) is specified...
#     sort targetfilename according to sortorder
#         need to find a sort function.
#     else print Bad rule-file sort command: sortorder" and exit
#         if sortorder is bad, should be caught before datarelocate starts.

# ----------------------------------------------------------------
# Datarelocate
# ----------------------------------------------------------------
## def datarelocate():
##     """Parses ./.locations and relocates files on its basis."""
##     pass
##     # destinations = open('/home/tbaker/u/agenda/.destinations')
##     # timestamp = $(date +%Y-%m-%d.%H%M)
##     # read destinations
##     #     $1 = file
##     #     $2 = destination directory
##     # defaultdestination is /home/tbaker/u/folders/+FTMP
##     # try to open file (1)
##     #     if not exist, then next
##     #     if exist then
##     #         rename file to file.$timestamp
##     #         if destination directory (2) exists, then move file.$timestamp there.
##     #             print Moving file.$timestamp to $2.
##     #         else move the file to defaultdestination
##     #             print Moving file.$timestamp to $2.
## 
## # This is the data structure that needs to be encoded in .locations:
## # agendaa /home/tbaker/u/agenda
## # agendab /home/tbaker/u/agendab
## # agendai /home/tbaker/u/folders/WASHDC/INVENTORY/agendai
## # agendan /home/tbaker/u/agendab
## # agendac /home/tbaker/u/agendac
## # agendad /home/tbaker/u/folders/TOM/dreams
## # agendaf /home/tbaker/u/agendaf
## # agendap /home/tbaker/person/agendap
## # agendapy /home/tbaker/u/folders/PY/agendapy
## # agendaw /home/tbaker/u/agendaf
## # agendax /home/tbaker/acct/agendax
## # agenday /home/tbaker/u/agenday
## # agendaz /home/tbaker/person/agendaz

# ----------------------------------------------------------------
# Datacleanup
# ----------------------------------------------------------------
#def datacleanup():
#    filelist = []
#    pathnamelist = os.listdir(os.getcwd())
#    for pathname in pathnamelist:
#        if os.path.isfile(pathname) == True:
#            if pathname[0] != ".":
#                filelist.append(pathname)
#    for file in filelist:
#        if os.path.getsize(file) == 0:
#            os.remove(file)

# ----------------------------------------------------------------
# tempfile module, if needed
# ----------------------------------------------------------------
# Tempfile module, Nutshell p223
