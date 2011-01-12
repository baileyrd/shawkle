Shawkle: Gettings Things Done with rule-based processing of plain-text lists

This Python script is designed to process plain-text files,
composed of "lines" of screen width (e.g., 120 columns), by
automatically moving the lines between different files based
on pattern matching.  The patterns to be matched, along with
the source and target files to which the patterns refer, are
expressed in a set of "rules" that are processed in order.
I have been using an earlier incarnation of this script, in
Korn shell, to manage my to-do lists and browser favorites
for the past sixteen years.

This project represents a refactoring and rewrite in Python
of a script originally written in 1993 using DOS 3.3 and the
Korn shell of MKS Toolkit. The original script, "shuffle",
was published in December 1994 in UnixWorld [1]. After using
awk in a rewrite of the script, I published the rewritten
script in December 2006 in lifehacker.com under the name
"shawkle" [2], with a narrative about the rationale for its
design.

This rewrite in Python was motivated primarily by a desire
to make shawkle more portable between platforms.  The shell
script version requires installation of a Korn shell and calls
many standard Unix utilities.  After using the program for so
long, I had evolved a specific manner of using the program
and felt the algorithm could be simplified by hard-coding
some simple defaults.

The new Python version runs much faster than the older Korn
shell script.  Here are some comparative timings from running
the two versions on a typical subdirectory of text lists:

    #!/bin/pdksh (2007)       #!/usr/bin/env python (2010)
    real    0m9.324s          real    0m1.150s
    user    0m10.933s         user    0m0.436s
    sys     0m6.143s          sys     0m0.624s

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

--   testagenda directory
     testagenda/.arules         - configuration file: first rules file
     testagenda/.rules          - configuration file: second rules file
     testagenda/.filemappings   - configuration file: maps filenames to target directories
     testagenda/*.txt           - example data

--   testagendab directory
     testagendab/.arules        - configuration file: first rules file
     testagendab/.rules         - configuration file: second rules file
     testagendab/.filemappings  - configuration file: maps filenames to target directories
     testagendab/*.txt          - example data

In order to run the demo, cd to the directory 'testagenda'
and run: '../shawkle.py'.

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

As of January 2011, I consider this script robust enough
to publicize more widely and would welcome any feedback or
bug reports from users.  The script tries hard to keep the
user from unintentionally damaging data by exiting with an
error message, before any data is processed, for example
if any non-text files, swap files (with extension .swp), or
files with blank lines are encountered.  Aside from creating
and refreshing the backup directories, the script leaves
directories untouched.  I am aware of some conditions that
can cause the program to exit with an uncaught exception
- for example, if a rule uses a regular expression not
supported by the Python functions - and I will be most
grateful for suggestions on making the script more robust.
I am an occasional programmer and have never used a Google
Code page to manage a project so would welcome any advice,
or initiatives, on using the wiki and issue tracker.

My wish list for further development of this script includes
a function for making plain-text links in TXT files into
clickable URLs in HTML files.  For this, I currently use an
old PERL script which works reasonably well but would like to
integrate this process into the main shawkle.py script, so that

    agendatest/now.txt

could be "URLified" as

    agendatest/.html/now.txt.html

to make it usable in my Web browser.



Tom Baker <tbaker@tbaker.de>, 12 January 2011

[1] http://web.bilkent.edu.tr/Online/uworld/archives/94/grabbag/06.txt.html
[2] http://lifehacker.com/217063/getting-things-done-with-rule+based-list-processing 
[3] http://code.google.com/p/shawkle/
[4] http://shawkle.googlecode.com/svn/trunk
