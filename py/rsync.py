#!/usr/bin/env python
# -*- coding: utf8 -*-

import pexpect
import sys

def usage():
    sys.stderr.write('''Usage: {} <password> <localpath> <remote>
'''.format(sys.argv[0]))
    sys.exit(-1)

def rsync(passwd, localpath, remote):
    '''Use pexpect to automatically rsync files'''
    # ignore svn meta files
    cmd = 'rsync -avz --exclude=.svn* -e "ssh -p 22" {} {}'\
        .format(localpath, remote)
    child = pexpect.spawn(cmd)
    #child.logfile = sys.stdout

    passwd_sent = False
    i = child.expect(['password:', 'yes/no'], timeout=3)
    if 0 == i:
        child.sendline(passwd)
        passwd_sent = True
    elif 1 == i:
        child.sendline('yes')

    if not passwd_sent:
        child.expect('password:', timeout=3)
        child.sendline(passwd)

    child.interact()

if '__main__' == __name__:
    if 4 != len(sys.argv):
        usage()

    rsync(sys.argv[1], sys.argv[2], sys.argv[3])
