from numpy import vectorize
import itertools

weapons = []
armor = []
rings = []

with open('stole.input.txt' , "r") as f:
        lines =  f.read().strip().split('\n')


c = 0
for i in lines:
    if i == '':
        c += 1
        continue
    p = i.split()
    p = p[-3:] # had a bug here, the line was p = p[1:]
    p = vectorize(int)(p)
    if c == 0:
        weapons.append(p)
    if c == 1:
        armor.append(p)
    if c == 2:
        rings.append(p)

armor.append([0, 0, 0]) # making not wearing armor possible
rings.append([0, 0, 0]) # same for rings
rings.append([0, 0, 0])




bhp = 100
bdmg = 8
barmr = 2

def simulate(php, pdmg, parmr):
    b = bhp
    while True:
        b -= max(1, pdmg - barmr)
        if b <= 0:
            return True
        php -= max(1, bdmg - parmr)
        if php <= 0:
            return False

m = 1e100
for i0 in weapons:
    for i1 in armor:
        for i2, i3 in itertools.combinations(rings, 2):
            php = 100
            cost = i0[0] + i1[0] + i2[0] + i3[0]
            pdmg = i0[1] + i1[1] + i2[1] + i3[1]
            parmr = i0[2] + i1[2] + i2[2] + i3[2]
            if simulate(php, pdmg, parmr):
                m = min(m, cost)
print(m)

m = -1e100
for i0 in weapons:
    for i1 in armor:
        for i2, i3 in itertools.combinations(rings, 2):
            php = 100
            cost = i0[0] + i1[0] + i2[0] + i3[0]
            pdmg = i0[1] + i1[1] + i2[1] + i3[1]
            parmr = i0[2] + i1[2] + i2[2] + i3[2]
            if not simulate(php, pdmg, parmr):
                m = max(m, cost)
print(m)