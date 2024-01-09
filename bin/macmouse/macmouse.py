import math
import os
X = 1728
Y = 1117

cx = X/2
cy = Y/2

r = 1150 - cx

for a in range(0,360):
    theta = a * math.pi / 180
    x = int(cx + r * math.cos(theta))
    y = int(cy + r * math.sin(theta))
    os.system(f'cliclick m:{x},{y}')
