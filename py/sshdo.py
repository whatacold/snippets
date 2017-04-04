#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Execute specified command on every hosts, which are specified in a file.
'''

import pexpect
import sys, os, getopt

def usage():
    sys.stderr.write('''Usage: {} [-u <username>] [-p <password>] <hosts-file> <cmd>

    <hosts-file>    hosts list, one host per line\n'''.format(sys.argv[0]))
    sys.exit(1)

def do(hosts_file, cmd, user=None, passwd=None):
    hosts = []
    with open(hosts_file, 'r') as fp:
        hosts = fp.read().strip().split('\n')

    for host in hosts:
        try:
            print('>> Execute "{}" on {}'.format(cmd, host))
            if user:
                child = pexpect.spawn("ssh {}@{} '{}'".format(user, host, cmd))
            else:
                child = pexpect.spawn("ssh {} '{}'".format(host, cmd))  # e.g. using private key
            #child.logfile = sys.stderr

            passwd_sent = False
            while not passwd_sent:
                i = child.expect(['password:', 'yes/no'], timeout=3)
                if 0 == i:
                    if not passwd:
                        sys.stderr.write('Password required but not supplied!\n')
                        usage()
                    child.sendline(passwd)
                    passwd_sent = True
                elif 1 == i:
                    child.sendline('yes')

            child.interact()
        except Exception as e:
            print('>> Failed on {}: {}'.format(host, e))

if '__main__' == __name__:
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'u:p:')
    except getopt.GetoptError as err:
        print(err)
        usage()

    user = None
    passwd = None
    for o, a in opts:
        if '-u' == o:
            user = a
        elif '-p' == o:
            passwd = a
        else:
            usage()

    if 2 != len(args):
        usage()

    hosts_file = args[0]
    cmd = args[1]
    if not os.path.isfile(hosts_file):
        sys.stderr.write('No such file: {}\n'.format(hosts_file))
        usage()

    do(
        hosts_file,
        cmd,
        user,
        passwd
    )
