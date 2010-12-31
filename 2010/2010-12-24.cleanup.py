#!/usr/bin/env python

import os

def datacleanup():
    listofpathnames = os.listdir(os.getcwd())
    for file in listofpathnames:
        if os.path.isfile(file):
            if os.path.getsize(file) == 0:
                print 'Removing zero-length file:', file
                os.remove(file)

if __name__ == "__main__":
    datacleanup()

