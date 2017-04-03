#!/usr/bin/env python

import sys
import binascii

def bin2hex(bin):
    return binascii.hexlify(bin)

def usage():
    sys.stderr.write("""Usage: hexdump.py [FILE]

Convert bytes from FILE, to hex string in one by one byte order.
If FILE is omitted, read bytes from standard input.
""")
    sys.exit(-1)

if '__main__' == __name__:
    if len(sys.argv) == 1:
        bin = sys.stdin.read()
    else:
        try:
            fp = open(sys.argv[1], 'rb')
            bin = fp.read() # read all
            fp.close()
        except IOError:
            usage()

    sys.stdout.write(bin2hex(bin))
