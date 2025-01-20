#!/usr/bin/env python3
"""
The formula for calculating guitar fret spacing is to divide the scale length
of the guitar by 17.817154 to find the location of the first fret. To find the
location of each subsequent fret, divide the remaining scale length by the same
factor. For example, to find the distance from the nut to the second fret, you
can:
Subtract the distance from the nut to the first fret from the scale length
Divide that number by 17.817
Add the result to the distance from the nut to the first fret


Logic:
    In 12 equal steps the frequency doubles
    Each step multiplies the frequecyc by 2^(1/12) = 1.059...
    That means each step reduces the vibrating length by that factor 1/(2^(1/12))
    So, leftover is 1 - 1/(2^(1/12))
    Which means division by 1 / ( 1 - 1/(2^(1/12)) ) = 17.817153745105742

"""

s_lespaul = 24.75
s_fender = 25.5

s = s_fender
print(f'Scale : {s}')
n = 17.817153745105742

import sys

if len(sys.argv) == 2:
    s = float(sys.argv[1])

x = 0
for i in range(1,25):
    y = (s - x) / n
    x = x + y
    print(f'{i}\t{y}\t{x}\t')
