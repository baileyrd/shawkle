#!/usr/bin/env python

import os

def totalsize():
    totalsize = 0
    listoffiles = os.listdir(os.getcwd())
    for file in listoffiles:
        if os.path.isfile(file):
            filesize = os.path.getsize(file)
            if filesize == 0:
                print 'Removing zero-length file:', file
                os.remove(file)
            else:
                if file[0] != ".":
                    totalsize = totalsize + filesize
    return totalsize

if __name__ == "__main__":
    print totalsize()

