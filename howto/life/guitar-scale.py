"""
The formula for calculating guitar fret spacing is to divide the scale length
of the guitar by 17.817154 to find the location of the first fret. To find the
location of each subsequent fret, divide the remaining scale length by the same
factor. For example, to find the distance from the nut to the second fret, you
can:
Subtract the distance from the nut to the first fret from the scale length
Divide that number by 17.817
Add the result to the distance from the nut to the first fret
"""

s_lespaul = 24.75
s_fender = 25.5

s = s_lespaul
n = 17.817154

x = 0
for i in range(1,25):
    y = (s - x) / n
    x = x + y
    print(f'{i}\t{y}\t{x}\t')
