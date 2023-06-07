#!/usr/bin/env python3
import re
import sys
import json

rec  = {'dn':'NONE', 'sm': 'NONE', 'mdn': 'NONE', 'msm': 'NONE'}
recs = {}
recs['dn'] = {}
recs['sm'] = {}
recs['dn']['NONE'] = {'dn':'NONE', 'sm': 'NONE', 'mdn': 'NONE', 'msm': 'NONE'}
recs['sm']['NONE'] = {'dn':'NONE', 'sm': 'NONE', 'mdn': 'NONE', 'msm': 'NONE'}

def record():
    recs['dn'][rec['dn']] = rec
    recs['sm'][rec['sm']] = rec
    
with open('allusers.txt', 'rt') as f:
    for line in f:
        line = line.strip()
        m = re.search(r'^([^\s\:]+)\s*\:\s*(.*)', line)
        if m:
            key, value = m.group(1), m.group(2)
            if key == 'dn':
                record()
                rec = {'dn':value, 'sm': 'NONE', 'mdn': 'NONE', 'msm': 'NONE'}
            elif key == 'manager':
                rec['mdn'] = value
            elif key == 'sAMAccountName':
                rec['sm'] = value
record()

for sm in recs['sm']:
    mdn = recs['sm'][sm]['mdn']
    msm = recs['dn'][mdn]['sm']
    recs['sm'][sm]['msm'] = msm
    recs['sm'][sm]['emps'] = {}

recs['dn'] = {}

for sm in recs['sm']:
    msm = recs['sm'][sm]['msm']
    recs['sm'][msm]['emps'][sm] = True

def parents_path(sm):
    epath = sm
    while True:
        msm = recs['sm'][sm]['msm']
        if msm != 'NONE' and msm != sm:
            epath = msm + '/' + epath 
            sm = msm
        else:
            break
    return epath

def children(sm):
    todo = {sm}    # set
    found = set()  # empty set
    while len(todo) != 0:
        for sm in list(todo):
            found.add(sm)
            todo.remove(sm)
            for i in recs['sm'][sm]['emps']:
                todo.add(i)
    return found


arg = None
if len(sys.argv) != 1:
    arg = sys.argv[1]

if arg is None:
    lines = []
    for sm in recs['sm']:
        lines.append(parents_path(sm))

    lines.sort()
    for line in lines:
        print(line)
else:
    lines = []
    for sm in children(arg):
        lines.append(parents_path(sm))
    lines.sort()
    for line in lines:
        print(line)
        

