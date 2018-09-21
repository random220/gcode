#!/usr/bin/python

import subprocess
import os
import sys
from subprocess import PIPE, Popen

os.environ['PATH'] = '/usr/local/bin:/bin:/sbin:/usr/bin:/usr/sbin'
passfile = '/etc/anayapass'
if not os.path.isfile(passfile):
    sys.exit(0)

myos = os.uname()
mac = False
if myos[0] == 'Darwin':
    mac = True

def main():
    #change_password('known')
    change_password('secret')
    kill_anaya_processes()

def main2():
    print_anaya_processes()
    if is_now_a_forbidden_time():
        change_password('secret')
        kill_anaya_processes()
    else:
        change_password('known')

def kill_anaya_processes():
    # Same commands on mac or linux
    subprocess.call('pkill -u anaya'.split())
    subprocess.call('pkill -9 -u anaya'.split())

def is_now_a_forbidden_time():
    return False

def change_password_to_known():
    return

def change_password(what):
    password = getpass(what)
    if password == None:
        print 'Doing nothing'
        return

    command = ['echo']
    if mac:
        command = 'dscl . -passwd /Users/anaya'.split()
        command.append(password)
    else:
        p = Popen(['chpasswd'], stdin=PIPE, stdout=None, stderr=None, shell=False)
        p.communicate(input='anaya:'+password+'\n')

    cmdout = subprocess.check_output(command)
    print cmdout

def getpass(what):
    if os.path.isfile(passfile):
        F = open(passfile, 'r')
        content = F.read()
        lines = content.splitlines()
        for line in lines:
            words = line.split()
            if words[0] == what:
                return words[1]
    else:
        return False

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


