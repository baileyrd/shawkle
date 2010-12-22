#!/usr/bin/env python

import os
import sys

def datals():
    """Returns list of files in current directory, excluding dot files and subdirectories.
        Ends program with error message on encountering a file ending in .swp or .lock."""
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

if __name__ == "__main__":
    os.chdir('/home/tbaker/u/scripts/PYFFLE/shawkle/testdata')
    listofdatafiles = datals()
    os.chdir('/home/tbaker/u/scripts/PYFFLE/shawkle')

