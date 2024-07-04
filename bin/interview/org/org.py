
"""
Input
    prashant:om
    gary:prashant
    om:srini
    aaron:peter
    om:felix
    prashant:devon
    devon:aaron

Output:
    /gary/prashant
    /gary/prashant/devon
    /gary/prashant/devon/aaron
    /gary/prashant/devon/aaron/peter
    /gary/prashant/om
    /gary/prashant/om/felix
    /gary/prashant/om/srini
"""

inp = [
"prashant:om",
"gary:prashant",
"om:srini",
"aaron:peter",
"om:felix",
"prashant:devon",
"devon:aaron",
]

e2m = {}
for line in inp:
    m, e = line.split(':')
    e2m[e] = m

orgs = []
for e in e2m:
    org = '/'+e
    while e in e2m:
        m = e2m[e]
        org = '/'+m+org
        e = m
    orgs.append(org)

for org in sorted(orgs):
    print(org)



