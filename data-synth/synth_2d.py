#!/usr/bin/env python
# encoding: utf-8
"""
synth_2d.py

Created by Steven Gomez on 2013-08-06.
Copyright (c) 2013 steveg. All rights reserved.
"""

import sys
import getopt
import math


help_message = '''
The help message goes here.
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def flat(x, coef0):
    return (coef0)

def linear(x, coef1, coef0):
    return (coef1*x + coef0)
    
def quadratic(x, coef2, coef1, coef0):
    return (coef2*(x*x) + linear(x, coef1, coef0))
    
def cubic(x, coef3, coef2, coef1, coef0):
    return (coef3*(x*x*x) + quadratic(x, coef2, coef1, coef0))
    
def polynomial(x, *coefs):
    sum = 0
    
    coefs = list(coefs)
    print coefs
    
    # Reverse coefs so that the index of each coefficient in the polynomial
    # matches its index in the list (e.g., the constant is in position 0)
    coefs.reverse()
    
    for i in range(0, len(coefs)):
        sum += math.pow(x, i)*coefs[i]
        
    return sum


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ho:v", ["help", "output="])
        except getopt.error, msg:
            raise Usage(msg)
    
        # option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-o", "--output"):
                output = value
    
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2
        
    x = 2
    print polynomial(x, 2, 4)


if __name__ == "__main__":
    sys.exit(main())
