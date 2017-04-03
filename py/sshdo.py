#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pexpect
import sys

def usage():
    sys.stderr.write('''Usage: {} <username> <password> <hosts-file> <cmd>
    <hosts-file>    hosts list, one host per line
'''.format(sys.argv[0]))
    sys.exit(-1)

def do(user, passwd, hosts_file, cmd):
    hosts = []
    with open(hosts_file, 'r') as fp:
        hosts = fp.read().strip().split('\n')

    for host in hosts:
        try:
            print('>> Execute "{}" on {}'.format(cmd, host))
            child = pexpect.spawn("ssh {}@{} '{}'".format(user, host, cmd))
            #child.logfile = sys.stderr

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
        except:
            print('>> Failed on {}'.format(host))

if '__main__' == __name__:
    if 5 != len(sys.argv):
        usage()

    do(
        sys.argv[1],
        sys.argv[2],
        sys.argv[3],
        sys.argv[4]
    )
