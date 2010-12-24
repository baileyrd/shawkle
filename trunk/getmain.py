#!/usr/bin/env python

import os
import re

if __name__ == "__main__":
    os.chdir('/home/tbaker/u/scripts/PYFFLE/shawkle/testdata')
    data = ['=2010-02-15 Tue 1400 TELECON\n', '=2010-08-24 Tue 0800 TELECON\n', 'A LATER Belongs in agendaa\n']
    rules = [[0, '2010', 'lines', 'agenday', ''], [2, 'LATER', 'lines', 'LATER.txt', '']]
    for rule in rules:
        searchfield = rule[0]
        searchkey = rule[1]
        source = rule[2]
        target = rule[3]
        #with open(source, 'r') as datatoread:
        #    data = datatoread.readlines()
        sourcefile = open(source, 'w')
        targetfile = open(target, 'a')
        print "%-10s %-10s %-10s %-10s" % (searchfield, searchkey, source, target)
        if searchfield == 0:
            sourcefile.writelines([ dataline for dataline in data if re.search(searchkey, dataline) ])
            sourcefile.writelines([ dataline for dataline in data if not re.search(searchkey, dataline) ])
            #lineswith = [ dataline for dataline in data if re.search(searchkey, dataline) ]
            #print 'lineswith is', lineswith
            #sourcefile.writelines(lineswith)
            #lineswithout = [ dataline for dataline in data if not re.search(searchkey, dataline) ]
            #print 'lineswithout is', lineswithout
            #targetfile.writelines(lineswithout)
        else:
            searchfield = searchfield - 1
            print searchfield
            sourcefile.writelines([ dataline for dataline in data if searchkey in dataline.split()[searchfield] ])
            targetfile.writelines([ dataline for dataline in data if not searchkey in dataline.split()[searchfield] ])
        sourcefile.close()
        targetfile.close()
    os.chdir('/home/tbaker/u/scripts/PYFFLE/shawkle')

