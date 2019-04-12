#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import print_function

import sys
import subprocess


def log(*args, **kwargs):
    print(*args, **kwargs)


def call(command):
    """
    :type command: str
    """
    r = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = r.communicate()
    if len(error) == 0:
        o = output.decode().rstrip()
        log('<{}> output: <{}>'.format(command, o))
    else:
        e = error.decode().rstrip()
        log('<{}> error: <{}>'.format(command, e))


def main():
    arguments = sys.argv[1:]
    call('pwd')


if __name__ == '__main__':
    main()
