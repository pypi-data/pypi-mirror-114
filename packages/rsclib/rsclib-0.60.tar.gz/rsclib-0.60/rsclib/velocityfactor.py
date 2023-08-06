#!/usr/bin/python3

from math import pi, sqrt

# from Self-Resonance-in-Coils, Payne

def vf (a, p, f) :
    """ f in MHz p: winding pitch im m
        dc: coil diameter in m
    """
    x = 2 * pi * a / p
    k = (sqrt (20) / pi) * ((dc ** 2 * f / (300 * p)) ** .25)
    vw = sqrt ((1 + x**2) / (1 + (k * x) ** 2))
    return vw
# end def vf


