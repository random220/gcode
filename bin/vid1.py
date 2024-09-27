#!/bin/bash

p=''
if [[ $p == '' ]]; then
    type python3 >/dev/null 2>&1
    if [[ $? == 0 ]]; then
        p=python3
    fi
fi
if [[ $p == '' ]]; then
    type python >/dev/null 2>&1
    if [[ $? == 0 ]]; then
        p=python
    fi
fi
if [[ $p == '' ]]; then
    echo Python not found
    exit 1
fi

rm -rf ~/.vid
mkdir ~/.vid

export f0=~/.vid/f0
export f1=~/.vid/f1
export f2=~/.vid/f2
export mvsh=~/.vid/mv.sh
vidpy=~/.vid/vid.py

ls -1a > $f0

cat <<"EOF" >$vidpy
import os
import sys
import re

f0 = os.environ['f0']
f1 = os.environ['f1']
f2 = os.environ['f2']
mvsh = os.environ['mvsh']


f0_handle = open(f0, 'rt')
f1_handle = open(f1, 'wt')
f2_handle = open(f2, 'wt')

n = 0
for line in f0_handle:
    line = line.strip()
    if line == '.':
        continue
    if line == '..':
        continue
    n += 1
    f1_handle.write('{n} {line}\n'.format(n=n, line=line))
    f2_handle.write('{n} {line}\n'.format(n=n, line=line))

f0_handle.close()
f1_handle.close()
f2_handle.close()

os.system('vi {f2}'.format(f2=f2))

def read_dirlist(fn):
    x = {}
    with open(fn, 'rt') as f:
        for line in f:
            line = line.strip()
            m = re.search(r'^(\d+)\s+(.+)$', line)
            if m:
                x[m.group(1)] = m.group(2)
    return x

one = read_dirlist(f1)
two = read_dirlist(f2)

def quotify(x):
    x = x.replace('\\', '\\\\')
    x = x.replace("'", "\\'")
    x = "$'{x}'".format(x=x)
    return x

indexes = set(list(one.keys()) + list(two.keys()))
dirs = {}

with open(mvsh, 'wt') as mvsh_handle:
    for i in indexes:
        f=''
        g=''
        if i in one:
            f = one[i]
        if i in two:
            g = two[i]
            m = re.search(r'^(.+)/', g)
            if m:
                d = m.group(1)
                if d not in dirs:
                    dirs[d] = True
                    mvsh_handle.write("mkdir -p {d}\n".format(d=quotify(d)))

        if i in one and i not in two:
            mvsh_handle.write("rm -rf {f}\n".format(f=quotify(f)))
            continue
        if one[i] != two[i]:
            mvsh_handle.write("mv {f} {g}\n".format(f=quotify(f), g=quotify(g)))

EOF

eval "$p $vidpy"

echo '# --------------------------------------------------------'
cat $mvsh
echo '# --------------------------------------------------------'
echo "bash $mvsh"
echo 'rm -rf ~/.vid'
