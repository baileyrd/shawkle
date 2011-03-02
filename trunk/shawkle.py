#!/usr/bin/env python

from __future__ import division
from __future__ import with_statement
import os, re, shutil, string, sys, datetime
import optparse

def getoptions():
    p = optparse.OptionParser(description="Shawkle - Rule-driven processor of plain-text lists",
                              prog="shawkle.py", version="0.4", usage="%prog")
    p.add_option("--cloud", action="store", type="string", dest="cloud",
                help="file, contents of which to be prefixed to each urlified HTML file; default ''", default="")
    p.add_option("--files2dirs", action="store", type="string", dest="files2dirs",
                help="files with corresponding target directories; default './.files2dirs'",
                default='.files2dirs')
    p.add_option("--globalrules", action="store", type="string", dest="globalrules",
                help="rules used globally (typically an absolute pathname), processed first; default '.globalrules'",
                default='.globalrules')
    p.add_option("--localrules", action="store", type="string", dest="localrules",
                help="rules used locally (typically a relative pathname), processed second; default './.rules'",
                default=".rules")
    p.add_option("--sedtxt", action="store", type="string", dest="sedtxt",
                help="stream edits for plain text, eg, expanding drive letters to URIs; default './.sedtxt'",
                default=".sedtxt")
    p.add_option("--sedhtml", action="store", type="string", dest="sedhtml",
                help="stream edits for urlified HTML, eg, shortening visible pathnames; default './.sedhtml'",
                default=".sedhtml")
    ( options, arguments ) = p.parse_args()
    return options

def datals():
    """Returns list of files in current directory, excluding dot files and subdirectories.
        If swap files, backup files, or non-text files are encountered, exits with error message."""
    filelist = []
    pathnamelist = os.listdir(os.getcwd())
    for pathname in pathnamelist:
        if os.path.isfile(pathname):
            if pathname[-3:] == "swp":
                print 'Detected swap file', pathname, '- which should be closed before proceeding - exiting...'
                sys.exit()
            if pathname[-1] == "~":
                print 'Detected temporary file', pathname, 'which should be renamed or deleted - exiting...'
                sys.exit()
            if pathname[0] != ".":
                filelist.append(pathname)
    ckthatfilesaretext(filelist)
    return filelist

def databackup(filelist):
    """Backs up the given list of files to directory "$PWD/.backup", 
    bumping previous backups to ".backupi", ".backupii", and ".backupiii"."""
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

def totalsize():
    """Returns total size in bytes of files in current directory,
    verbosely removing files of length zero."""
    totalsize = 0
    listoffiles = os.listdir(os.getcwd())
    filesremoved = []
    for file in listoffiles:
        if os.path.isfile(file):
            filesize = os.path.getsize(file)
            if filesize == 0:
                print 'Removing zero-length file:', file
                filesremoved.append(file)
                os.remove(file)
            else:
                if file[0] != ".":
                    totalsize = totalsize + filesize
    return totalsize

def slurpdata(datafileslisted):
    """If all files in the given list are readable and contain no blank lines.
    returns a consolidated, sorted list of lines from all files.
    Otherwise, exits with helpful error message."""
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
    """Tests whether a file consists of text and exits if not.
    Based on O'Reilly Python Cookbook, p.25."""
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

def getrules(globalrules, localrules):
    """Consolidates the lines of raw global and local rule files into one list.
    Deletes comments and blank lines.  Performs sanity checks to ensure well-formedness of rules.
    Returns a consolidated list of rules, each item itself a list of rule components."""
    globalrules = os.path.expanduser(globalrules)
    localrules = os.path.expanduser(localrules)
    listofrulefiles = [ str(globalrules), str(localrules) ]
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
    print "Using config file:", localrules, "- local rule file"
    print "Using config file:", globalrules, "- global rule file"
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
            try:
                re.compile(linesplitonorbar[1])
            except:
                print 'In rule:', linesplitonorbar
                print '...in order to match the data string:', str(linesplitonorbar[1])
                print '...the rule component must be escaped like this:', re.escape(linesplitonorbar[1])
                sys.exit()
            if len(linesplitonorbar[4]) > 0:
                if not linesplitonorbar[4].isdigit():
                    print linesplitonorbar
                    print 'Fifth field must be an integer or zero-length string - exiting...'
                    sys.exit()
            if linesplitonorbar[4] < 1:
                print linesplitonorbar
                print 'Fifth field integer must be greater than zero - exiting...'
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

def getmappings(mappings, helpmessage):
    """Parses the given file, the lines are supposed to consist of two fields separated by a vertical bar.
    Strips comments, commented lines, and blank lines.
    Ignores lines with more than two vertical-bar-delimited fields.
    Returns list, each item of which is a list of two items ."""
    helpmessage = str(helpmessage)
    mappings = os.path.expanduser(mappings)
    print "Using config file:", mappings, helpmessage
    mappingsraw = []
    mappingsparsed = []
    try:
        mappings = open(mappings, 'rU')
        mappingsraw = mappings.readlines()
    except:
        print 'Mapping file', mappings, 'does not exist - exiting...'
        return mappingsparsed
        #sys.exit()
    mappings.close()
    for line in mappingsraw:
        linestripped = line.strip()
        linedecommented = linestripped.partition('#')[0]
        linewithouttrailingwhitespace = linedecommented.rstrip()
        linesplitonorbar = linewithouttrailingwhitespace.split('|')
        if len(linesplitonorbar) == 2:
            mappingsparsed.append(linesplitonorbar)
    return mappingsparsed

def movefiles(files2dirs):
    """Given the list of mappings of filenames to target directories:
        if file and directory both exist, moves file to directory,
        if file exists but not the target directory, reports that the file is staying put."""
    timestamp = datetime.datetime.now()
    prefix = timestamp.isoformat('.')
    for line in files2dirs:
        filename = line[0]
        dirpath = line[1]
        timestampedpathname = dirpath + '/' + prefix[0:13] + prefix[14:16] + prefix[17:19] + '.' + filename
        try:
            shutil.move(filename, timestampedpathname)
            print 'Moving', filename, 'to', timestampedpathname
        except:
            if os.path.exists(filename):
                print 'Keeping file', filename, 'where it is - directory', dirpath, 'does not exist...'

def shuffle(rules, datalines):
    """Takes as arguments a list of rules and a list of data lines.
    For the first rule only: 
        writes data lines matching a regular expression to the target file,
        writes data lines not matching the regular expression to the source file.
    For each subsequent rule: 
        reads data lines from source file, 
        writes lines matching a regular expression to the target file, 
        writes lines not matching a regular expression to the source file, overwriting the source file."""
    rulenumber = 0
    for rule in rules:
        rulenumber += 1
        field = rule[0]
        searchkey = rule[1]
        source = rule[2]
        target = rule[3]
        sortorder = rule[4]
        if sortorder:
            print '%s [%s] "%s" to "%s", sorted by field %s' % (field, searchkey, source, target, sortorder)
        else:
            print '%s [%s] "%s" to "%s"' % (field, searchkey, source, target)
        if rulenumber == 1:
            data = datalines
        else:
            readonlysource = open(source, 'r')
            data = readonlysource.readlines()
            readonlysource.close()
        targetlines =  []
        sourcelines =  []
        if field == 0:
            if searchkey == ".":
                targetlines = [ line for line in data ]
            else:
                sourcelines = [ line for line in data if not re.search(searchkey, line) ]
                targetlines = [ line for line in data if re.search(searchkey, line) ]
        else:
            ethfield = field - 1
            for line in data:
                if field > len(line.split()):
                    sourcelines.append(line)
                else:
                    if re.search(searchkey, line.split()[ethfield]):
                        targetlines.append(line)
                    else:
                        sourcelines.append(line)
        sfile = open(source, 'w')
        tfile = open(target, 'a')
        sfile.writelines(sourcelines)
        tfile.writelines(targetlines)
        sfile.close()
        tfile.close()
        if sortorder:
            readonlytfile = open(target, 'r')
            data = readonlytfile.readlines()
            readonlytfile.close()
            tfile = open(target, 'w')
            targetlines = dsusort(data, sortorder)
            tfile.writelines(targetlines)
            tfile.close()

def comparesize(sizebefore, sizeafter):
    """Given the aggregate size in bytes of files "before" and "after":
        reports if sizes are the same, or
        warns if sizes are different."""
    print 'Size pre was', sizebefore
    print 'Size post is', sizeafter
    if sizebefore == sizeafter:
        print 'Done: data shawkled and intact!'
    else:
        print 'Warning: data may have been lost - revert to backup!'

def urlify_string(s):
    """Puts HTML links around a URL, i.e., a string ("s") starting
    with "http", "file", or "irc", etc.
    This code, found on Web, appears to be based on Perl Cookbook, section 6.21 ("urlify")."""
    urls = r'(http|https|telnet|gopher|file|wais|ftp|irc)'
    ltrs = r'\w';
    gunk = r'/#~:.?+=&%@!\-'
    punc = r'.:?\-'
    any  = ltrs + gunk + punc 
    pat = re.compile(r"""
      \b                    # start at word boundary
      (                     # begin \1  {
       %(urls)s  :          # need resource and a colon
       [%(any)s] +?         # followed by one or more
                            #  of any valid character, but
                            #  be conservative and take only
                            #  what you need to....
      )                     # end   \1  }
      (?=                   # look-ahead non-consumptive assertion
       [%(punc)s]*          # either 0 or more punctuation
       [^%(any)s]           #   followed by a non-url char
       |                    # or else
       $                    #   then end of the string
      )
    """%locals(), re.VERBOSE | re.IGNORECASE)
    return re.sub(pat, r"<A HREF=\1>\1</A>", s)

def urlify(listofdatafiles, sedtxt, sedhtml, htmldir, cloud):
    """For each file in list of files (listofdatafiles): 
        create a urlified (HTML) file in the specified directory (htmldir), 
        prepending the contents of an optional cloud file (cloud) to each urlified file,
        optionally stream-editing the plain text using before-and-after transforms (sedtxt), and
        optionally stream-editing the urlified text using before-and-after transforms (sedhtml)."""
    cloud = os.path.expanduser(cloud)
    cloudlines = []
    if os.path.isfile(cloud):
        cloudfile = open(cloud, 'r')
        cloudlines = cloudfile.readlines()
        cloudfile.close()
    if not os.path.isdir(htmldir):
        print 'Creating directory', htmldir
        os.mkdir(htmldir)
    else:
        try:
            shutil.rmtree(htmldir)
            print 'Removing and re-creating directory', htmldir
            os.mkdir(htmldir)
        except:
            print 'Could not remove and re-create directory', htmldir, '- HTML files are therefore out of date'
            sys.exit()
    if cloud != '': print "Prepending file:", cloud, "to each urlified file"
    for file in listofdatafiles:
        try:
            openfile = open(file, 'r')
            openfilelines = openfile.readlines()
            openfilelines = cloudlines + openfilelines
        except:
            print 'Cannot open', file, '- exiting...'
            sys.exit()
        openfile.close()
        urlifiedlines = []
        for line in openfilelines:
            for sedmap in sedtxt:
                try:
                    old = sedmap[0]
                    new = sedmap[1]
                    line = line.replace(old, new)
                except:
                    pass
            line = urlify_string(line)
            for visualimprovement in sedhtml:
                try:
                    ugly = visualimprovement[0]
                    pretty = visualimprovement[1]
                    line = line.replace(ugly, pretty)
                except:
                    pass
            urlifiedlines.append(line)
        filehtml = htmldir + '/' + file + '.html'
        try:
            openfilehtml = open(filehtml, 'w')
            print 'Creating urlified file', filehtml
        except:
            print 'Cannot open', filehtml, '- exiting...'
            sys.exit()
        openfilehtml.write('<PRE>\n')
        linenumber = 1
        field1before = ''
        for urlifiedline in urlifiedlines:
            field1 = urlifiedline.split()[0]
            if linenumber > 1:
                if field1before != field1:
                    openfilehtml.write('\n')
            field1before = field1
            linenumber += 1
            openfilehtml.write(urlifiedline)
        openfilehtml.write('</PRE>\n')
        openfilehtml.close()

def dsusort(dlines, field):
    """Given a list of datalines (list "dlines"):
        returns list sorted by given field (greater-than-zero integer "field")."""
    intfield = int(field)
    ethfield = intfield - 1
    dlinesdecorated = []
    for line in dlines:
        linelength = len(line.split())
        if intfield > linelength:
            fieldsought = ''
        else:
            fieldsought = line.split()[ethfield]
        decoratedline = (fieldsought, line)
        dlinesdecorated.append(decoratedline)
    dlinesdecorated.sort()
    dlinessorted = []
    dlinessorted = [ t[1] for t in dlinesdecorated ]
    return dlinessorted

if __name__ == "__main__":
    arguments = getoptions()
    rules = getrules(arguments.globalrules, arguments.localrules)
    filesanddestinations = getmappings(arguments.files2dirs, '- specifies names of files and destination directories')
    sedtxtmappings = getmappings(arguments.sedtxt, '- specifies stream edits before urlification')
    sedhtmlmappings = getmappings(arguments.sedhtml, '- specifies stream edits after urlification')
    optionalcloudfile = arguments.cloud
    sizebefore = totalsize()
    datafilesbefore = datals()
    databackup(datafilesbefore)
    datalines = slurpdata(datafilesbefore)
    shuffle(rules, datalines)
    sizeafter = totalsize()
    movefiles(filesanddestinations)
    datafilesaftermove = datals()
    urlify(datafilesaftermove, sedtxtmappings, sedhtmlmappings, '.html', optionalcloudfile)
    comparesize(sizebefore, sizeafter)

