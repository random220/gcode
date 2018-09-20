#!/usr/bin/python

import subprocess
import os
os.environ['PATH'] = '/usr/local/bin:/bin:/sbin:/usr/bin:/usr/sbin'

def main():
    print_anaya_processes()
    if is_now_a_forbidden_time():
        change_password_to_secret()
        kill_anaya_processes()
    else:
        change_password_to_known()


def print_anaya_processes():
    cmdout = subprocess.check_output(['ps', 'aux'])
    # omandal  console  Sep 12 17:19 
    # omandal  ttys000  Sep 20 12:07 

    lines = cmdout.splitlines()
    for line in lines:
        words = line.split()
        if words[0] == 'omandal':
            print words[0]+' '+words[1]+' '+words[10]

main()
