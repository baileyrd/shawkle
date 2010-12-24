#!/usr/bin/env python

import os
import sys
import shutil

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

def databackup(filelist):
    """Backs up list of files in $PWD to ".backup", bumping previous to ".backupi", ".backupii", ".backupiii"."""
    backupdirs = ['.backup', '.backupi', '.backupii', '.backupiii']
    for dir in backupdirs:
        if not os.path.isdir(dir):
            os.mkdir(dir)
    shutil.rmtree(backupdirs[3])
    print 'Bumping off', backupdirs[3]
    shutil.move(backupdirs[2], backupdirs[3])
    print 'Moving contents of', backupdirs[2], "to", backupdirs[3]
    shutil.move(backupdirs[1], backupdirs[2])
    print 'Moving contents of', backupdirs[1], "to", backupdirs[2]
    shutil.move(backupdirs[0], backupdirs[1])
    os.mkdir(backupdirs[0])
    for file in filelist:
        print 'Moving to', backupdirs[0], ":", file
        shutil.move(file, backupdirs[0])

if __name__ == "__main__":
    os.chdir('/home/tbaker/u/scripts/PYFFLE/shawkle/testdata')
    listofdatafiles = datals()
    databackup(listofdatafiles)
    os.chdir('/home/tbaker/u/scripts/PYFFLE/shawkle')


