#!/bin/bash

# Check for Python3 or Python2 and assign to variable `p`
p=''
if command -v python3 &>/dev/null; then
    p=python3
elif command -v python &>/dev/null; then
    p=python
else
    echo "Python not found"
    exit 1
fi

# Setup temporary directory
VID_DIR="$HOME/.vid"
mkdir -p "$VID_DIR"

export F0="$VID_DIR/f0"
export F1="$VID_DIR/f1"
export F2="$VID_DIR/f2"
export MVSH="$VID_DIR/mv.sh"
VIDPY="$VID_DIR/vid.py"

# List files and directories in the current directory
ls -1a > "$F0"

# Generate Python script
cat <<'EOF' >"$VIDPY"
import os
import re

f0 = os.environ['F0']
f1 = os.environ['F1']
f2 = os.environ['F2']
mvsh = os.environ['MVSH']

with open(f0, 'rt') as f0_handle, open(f1, 'wt') as f1_handle, open(f2, 'wt') as f2_handle:
    n = 0
    for line in f0_handle:
        line = line.strip()
        if line in ('.', '..'):
            continue
        n += 1
        f1_handle.write('{} {}\n'.format(n, line))
        f2_handle.write('{} {}\n'.format(n, line))

os.system('vi {}'.format(f2))

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
    return "$'{}'".format(x)

indexes = set(one.keys()).union(set(two.keys()))
dirs = {}

with open(mvsh, 'wt') as mvsh_handle:
    for i in indexes:
        f = one.get(i, '')
        g = two.get(i, '')
        if i in one and i not in two:
            mvsh_handle.write("rm -rf {}\n".format(quotify(f)))
        elif one.get(i) != two.get(i):
            if g:
                dir_name = os.path.dirname(g)
                if dir_name and dir_name not in dirs:
                    dirs[dir_name] = True
                    mvsh_handle.write("mkdir -p {}\n".format(quotify(dir_name)))
                mvsh_handle.write("mv {} {}\n".format(quotify(f), quotify(g)))
EOF

# Run the Python script
"$p" "$VIDPY"

# Display and suggest executing the move script
echo '# --------------------------------------------------------'
cat "$MVSH"
echo '# --------------------------------------------------------'
echo "bash $MVSH"
echo "rm -rf $VID_DIR"
