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
import numpy


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
    
def polynomial(x, coefs):
    sum = 0
    
    # Reverse coefs so that the index of each coefficient in the polynomial
    # matches its index in the list (e.g., the constant is in position 0)
    coefs.reverse()
    
    for i in range(0, len(coefs)):
        sum += math.pow(x, i)*coefs[i]
        
    return sum


# Return a dictionary of x, y values
# TODO: Only handles integer domains for now, extend to float
def evaluate(start, end, tick, coefs):
    func = {}
    for x in range(start, end, tick):
        func[x] = polynomial(x, coefs)
        
    return func
    
# Return a JSON string representation of the data domain and
# range.
def get_JSON(start, end, tick, mean, stdev, coefs):
    vals = evaluate(start, end, tick, coefs)
    
    # Generate noise to add to signal
    noise = numpy.random.normal(mean, stdev, len(vals))
    
    json_preamble= '"data": [\n\t{\n\t\t"name": "table",\n\t\t"values": [\n\t\t\t'
    json_postamble = '\n\n\t\t]\n\t}\n]'
    
    json_vals_list = []
    noise_idx = 0
    for key in range(start, end, tick):
        bit = '{"x":' + str(key) + ', "y":' + str(vals[key]+noise[noise_idx]) + '}'
        json_vals_list.append(bit)
        noise_idx = noise_idx+1
        
    json_full = json_preamble + ", ".join(json_vals_list) + json_postamble
    return json_full
    
def get_Vega_spec(start, end, tick, mean, stdev, coefs):
    vega_preamble = """
{
    "width": 800,
    "height": 600,
    "padding": {"top": 10, "left": 30, "bottom": 20, "right": 10},
    """
    
    vega_postamble = """,
    "scales": [
        {"name":"x", "type":"ordinal", "range":"width", "domain":{"data":"table", "field":"data.x"}},
        {"name":"y", "range":"height", "nice":true, "domain":{"data":"table", "field":"data.y"}}
    ],
    "axes": [
        {"type":"x", "scale":"x"},
        {"type":"y", "scale":"y"}
    ],
    "marks": [
        {
            "type": "rect",
            "from": {"data":"table"},
            "properties": {
                "enter": {
                    "x": {"scale":"x", "field":"data.x"},
                    "width": {"scale":"x", "band":true, "offset":-1},
                    "y": {"scale":"y", "field":"data.y"},
                    "y2": {"scale":"y", "value":0}
                },
                "update": { "fill": {"value":"steelblue"} },
                "hover": { "fill": {"value":"red"} }
            }
        }
    ]
}
    """
    
    vega_full = vega_preamble + get_JSON(start, end, tick, mean, stdev, coefs) + vega_postamble
    return vega_full
    
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
        
    startX = -50
    endX = 50
    tickX = 5
    noise_mean = 0
    noise_stdev = 5000
    poly = [2, 4, 8, 3]
    
    print get_Vega_spec(startX, endX, tickX, noise_mean, noise_stdev, poly)

if __name__ == "__main__":
    sys.exit(main())
