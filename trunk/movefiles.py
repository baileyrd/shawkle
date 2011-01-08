#!/usr/bin/env python

from __future__ import division
import os
import re
import shutil
import string
import sys

#    datalines = ['2010-02 To be archived...\n',
#     '=2010-02-15 Tue 1400 TELECON\n',
#     '=2010-02-15 Tue 1900 RDF2 http://decentralyze.com/2009/10/30/rdf-2-wishlist/\n',
#     '=2010-02-17 Wed 0800 TELECON\n',
#     '=2010-08-24 Tue 0800 TELECON\n',
#     'A LATER Belongs in agendaa\n',
#     'LATER Haircut\n',
#     'LATER http://www.asis.org/\n',
#     'NOW Buy milk\n',
#     'NOW Shovel snow\n']
#    listofdatafiles = ['huh.txt', 'malendar.txt']
#    rules = [[1, '2010-', 'lines', 'agendaz', ''],
#     [0, '^A ', 'lines', 'agendaa', ''],
#     [0, '.', 'lines', 'HUH.txt', ''],
#     [0, '.', 'agendaa', 'HUH.txt', ''],
#     [1, '=2', 'HUH.txt', 'calendar.txt', ''],
#     [1, 'LATER', 'HUH.txt', 'LATER.txt', ''],
#     [1, 'NOW', 'HUH.txt', 'NOW.txt', '']]
today=$(date +%Y-%m-%d.%H%M)

function move_file { 
    # Arguments: $1 = filename; $2 = preferred directory
    M=/home/tbaker/u/folders/+FTMP; mkdir -p $M
    [ -f $1 ] && (
        # If preferred directory exists, then move the file there.
        [ -d $2 ] && ( print -u2 Moving $1 to $2/$today.$1; mv -i $1 $2/$today.$1 )
        # If preferred directory does not exist, then move the file to default directory $M
        [ ! -d $2 ] && ( print -u2 Moving $1 to $M/$today.$1; mv -i $1 $M/$today.$1 )
        )
    }

move_file agenda  /home/tbaker/u/agenda
#move_file agendaa /home/tbaker/u/agendaa
move_file agendab /home/tbaker/u/agendab
move_file agendap /home/tbaker/u/folders/PYTH/agendap
move_file agendax /home/tbaker/acct/agendax
move_file agenday /home/tbaker/health/agenday
move_file agendaz /home/tbaker/person/agendaz
