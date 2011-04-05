Shawkle: Gettings Things Done with rule-based processing of plain-text lists

Updated: 2011-04-04

This Python script is designed to process plain-text files,
composed of "lines" of screen width (e.g., 120 columns)
or Tweet width (140 columns), by automatically relocating
individual lines into various files based on pattern matching.
The patterns to be matched, along with the source and target
files to which the patterns refer, are expressed in a set of
"rules" that are processed in order.  This Python script
replaces earlier incarnations of the script in Korn shell
that I have been continuously using to manage my to-do lists,
activity logs, and browser favorites for the past sixteen
years.

This project represents a refactoring and rewrite in Python
of a script originally written in 1993 using DOS 3.3 and the
MKS Toolkit (hence Korn shell). The original script, "shuffle",
was published in December 1994 in UnixWorld [1]. After using
awk in a rewrite of the script, I published the rewritten
script in December 2006 in lifehacker.com under the name
"shawkle" [2], with a narrative about the rationale for its
design.

This rewrite in Python was motivated primarily by a desire to
make shawkle more portable between platforms.  The shell script
version requires installation of a Korn shell and calls many
standard Unix utilities.  Moreover after using the program
for so many years, I had evolved a specific manner of using
the program and felt the algorithm could be simplified by
hard-coding some simple defaults.  The Python rewrite runs
roughly ten times faster than the older Korn shell script.

Although this Python rewrite does not use awk, I am retaining
the name "shawkle" in order to avoid possible confusion with
other programs called "shuffle" which have in the meantime
appeared.  I also see that "shawkle" means "shake" in Yiddish
(as in "Gib a shawkle!" or "Shake a leg!").  As the program
involves ingesting alot of text lines and "shaking them up",
albeit in a rule-driven manner, the familiar name still
seems apt.

The source code for this Python version of shawkle is available
under a BSD open-source license from a Google Code page [3] and
can be downloaded by checking out [4] with Subversion.

The source checkout includes not only the script itself,
shawkle.py, but two directories of example data that can be
used to test the program and play around with the rule-based
approach:

--   testadata directory
     testdata/a/*.txt           - example data
     testdata/a/.globalrules    - configuration file: first rules file
     testdata/a/.rules          - configuration file: second rules file
     testdata/a/.filemappings   - configuration file: maps filenames to target directories
     testagendab/.rules         - configuration file: first rules file

To see the program in action, follow the instructions in
testdata/a/demo-howto.txt (or, if the file is installed 
in ~/shawkle: ~/shawkle/testdata/a/demo-howto.txt).

The script is designed to operate on text files in the
working directory.  Beware that within the working directory,
the script creates subdirectories and creates, deletes, and
overwrites and text files it finds.  I am not aware of any
conditions under which the script could cause harm to files
outside of the working directory, but testers should please
exercise due caution.

The demo is designed to illustrate an additional feature not
supported in the published Korn shell script: an additional set
of rules for automatically moving certain files to specified
subdirectories as a final step.  For example, I might have
separate directories for "work-related" and "personal" lists,
and list files will move between those directories, whenever
shawkle.py is run, on the basis of simple mappings.

When run, the program creates backup directories for the text
files -- four levels deep -- so that users can fall back on
earlier snapshots of the files if something unexpected occurs.
These directories are, from most recent to oldest:

    .backup
    .backupi
    .backupii
    .backupiii

As of March 2011, the most important issue remaining to be
addressed is that of changing the algorithm in databackup()
to _copy_ data between the .backup* directories instead of
_moving_ the directories.  Moving a directory under Subversion
control creates problems with the Subversion project as
a whole.  This will be addressed soon, as the scenario of
using shawkle in data directories under Subversion control
is quite likely.

I consider this script robust enough to begin publicizing it
more widely and would welcome any feedback or bug reports
from users.  The script tries hard to keep the user from
unintentionally damaging data by exiting with an error message,
before any data is processed, for example if any non-text
files, swap files (with extension .swp), emacs backup files
(ending in a tilde), or files with blank lines are encountered.
Shawkle also exits if it detects bad regular expressions in the
configuration files.  Aside from creating and refreshing the
backup directories, the script leaves directories untouched.

Tom Baker <tbaker@tbaker.de>

[1] http://web.bilkent.edu.tr/Online/uworld/archives/94/grabbag/06.txt.html
[2] http://lifehacker.com/217063/getting-things-done-with-rule+based-list-processing 
[3] http://code.google.com/p/shawkle/
[4] http://shawkle.googlecode.com/svn/trunk

