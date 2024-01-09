#!/usr/bin/env python3

import os, sys
import random
import time

X = 1728
Y = 1117

if os.path.isfile('/tmp/.die.alive'):
    os.unlink('/tmp/.die.alive')

while True:
    if os.path.isfile('/tmp/.die.alive'):
        sys.exit(0)
    x = random.randint(0, X)
    y = random.randint(0, Y)
    os.system(f'cliclick m:{x},{y}')
    time.sleep(15)
