#!/usr/bin/env python3

import os, sys
import random
import time
import subprocess as sp

X = 1728
Y = 1117

if os.path.isfile('/tmp/.die.alive'):
    os.unlink('/tmp/.die.alive')

p0 = sp.getoutput('cliclick p:.')

while True:
    if os.path.isfile('/tmp/.die.alive'):
        os.unlink('/tmp/.die.alive')
        sys.exit(0)
    p1 = sp.getoutput('cliclick p:.')
    if p1 == p0:
        x = random.randint(0, X)
        y = random.randint(0, Y)
        sp.run(f'cliclick -r -e 50 m:{x},{y}', shell=True)
    p0 = sp.getoutput('cliclick p:.')
    time.sleep(60)
