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

recs['dn'] = {}

lines = []
for sm in recs['sm']:
    epath = sm
    while True:
        msm = recs['sm'][sm]['msm']
        if msm != 'NONE' and msm != sm:
            epath = msm + '/' + epath 
            sm = msm
        else:
            break
    lines.append(epath)

lines.sort()
for line in lines:
    print(line)




