#!/usr/bin/env python

import os, re, shutil, string, sys, datetime, optparse, shawkle

def movefiles(sourcedirectory, targetdirectory):
    pwd = os.getcwd()
    abssourcedir = pwd + '/' + sourcedirectory
    abstargetdir = pwd + '/' + targetdirectory
    if os.path.isdir(abssourcedir):
        if os.path.isdir(abstargetdir):
            os.chdir(abssourcedir)
            files = shawkle.datals()
            if files:
                print 'Moving files in', repr(abssourcedir), "to", repr(abstargetdir)
                for file in files:
                    shutil.copy2(file, abstargetdir)
                    os.remove(file)
            os.chdir(pwd)
        else:
            print 'Directory', repr(abstargetdir), 'does not exist - exiting...'
            sys.exit()
    else:
        print 'Directory', repr(abssourcedir), 'does not exist - exiting...'
        sys.exit()

if __name__ == "__main__":
    movefiles('a', 'b')
    movefiles('b', 'a')
    movefiles('c', 'a')
    
