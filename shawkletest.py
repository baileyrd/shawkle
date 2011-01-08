#!/usr/bin/env python

from __future__ import division
from __future__ import with_statement
from IPython import genutils
import os
import re
import shutil
import string
import sys

def datacleanup():
    listofpathnames = os.listdir(os.getcwd())
    for file in listofpathnames:
        if os.path.isfile(file):
            if os.path.getsize(file) == 0:
                print 'Removing zero-length file:', file
                os.remove(file)

if __name__ == "__main__":
    datalines = ['2010-02 To be archived...\n',
     '=2010-02-15\n',
     '=2010-02-15 Tue 1400 TELECON\n',
     '=2010-02-15 Tue 1900 RDF2 http://decentralyze.com/2009/10/30/rdf-2-wishlist/\n',
     '=2010-02-17 Wed 0800 TELECON\n',
     '=2010-08-24 Tue 0800 TELECON\n',
     'A LATER Belongs in agendaa\n',
     'LATER Haircut\n',
     'LATER http://www.asis.org/\n',
     'NOW Buy milk\n',
     'NOW Shovel snow\n']
    #listofdatafiles = ['huh.txt', 'malendar.txt']
    rules = [[0, '^2010-', 'aaa.txt', '2010.txt', ''],
     [0, '^A ', 'aaa.txt', 'agendaa.txt', ''],
     [0, '.', 'aaa.txt', 'HUH.txt', ''],
     [2, '=2', 'HUH.txt', 'calendar.txt', ''],
     [1, 'LATER', 'HUH.txt', 'LATER.txt', ''],
     [1, 'NOW', 'HUH.txt', 'NOW.txt', '']]
    rulenumber = 0
    for rule in rules:
        rulenumber += 1
        field = rule[0]
        searchkey = rule[1]
        source = rule[2]
        target = rule[3]
        print '%s [%s] "%s" to "%s"' % (field, searchkey, source, target)
        if rulenumber == 1:
            data = datalines
        else:
            readonlysource = open(source, 'r')
            data = readonlysource.readlines()
            readonlysource.close()
        sfile = open(source, 'w')
        tfile = open(target, 'a')
        if field == 0:
            print 'field is zero'
            if searchkey == ".":
                tfile.writelines(data)
            else:
                sfile.writelines([ line for line in data if re.search(searchkey, line) ])
                tfile.writelines([ line for line in data if not re.search(searchkey, line) ])
        else:
            data = datalines
            print 'field is not zero'
            ethfield = field - 1
            for line in data:
                if field > len(line.split()):
                    tfile.writelines(data)
                else:
                    sfile.writelines([ line for line in data if re.search(searchkey, line.split()[ethfield]) ])
                    tfile.writelines([ line for line in data if not re.search(searchkey, line.split()[ethfield]) ])
        sfile.close()
        tfile.close()
    datacleanup()






# Notes:
# 2010-12-25
#    sourcefile.writelines([ dataline for dataline in data if re.match(searchkey, dataline) ])
#    sourcefile.writelines([ dataline for dataline in data if re.search(searchkey, dataline) ])
#    - "search" matches anywhere, "match" matches at start of string
#    - typically, want to assume start of string
#    - but what about if "^AGENDA" is supposed to come after "^A "...?
#
#    Next: maybe need to test for list?
#        def mustbelist(argument):
#            if type(argument) != list:
#                print 'Argument be a list, if only a list of one.  Exiting...'
#                sys.exit()
#    [4, 'TELECON', 'aaa.txt', 'telecon.txt', ''],
#            sourcefile.writelines([ line for line in data if searchkey in line.split()[ethsearchfield] ])
#            targetfile.writelines([ line for line in data if not searchkey in line.split()[ethsearchfield] ])
#        sourcefile.close()

#        if rulenumber == 1:
#            # When first rule is processed, no files -- source or target -- have yet been created,
#            # so data is taken directly from variable "datalines", a list that has already been created in memory.
#            # Note: the following assignment might be redundant...
#            data = datalines
#        else:
#            # After the first rule is processed, data is read from the source file into a list 
#            # in memory and assigned to the variable "data"
#            readonlysource = open(source, 'r')
#            data = readonlysource.readlines()
#            readonlysource.close()
