import numpy as np
from sympy import Symbol
from sympy import solve_poly_system

handle = open("input.txt","r")

shards = []
for line in handle:
  pos, vel = line.strip().split(" @ ")
  px,py,pz = pos.split(", ")
  vx,vy,vz = vel.split(", ")
  shards.append((int(px),int(py),int(pz),int(vx),int(vy),int(vz)))

count = 0
#go through the pairs of lines, convert them to y=mx+b
#(I think you could also do it directly in parametric form, but I knew how to do it with y=mx+b form)
#Given y = ma*x + ba and y = mb*x + bb, set them equal and solve for x
#then plug back in to solve for y.
#find the times by dividing the x distance by the x velocity
#check if times are positive and the intersection is within the target box
for adx in range(len(shards)-1):
  shard_a = shards[adx]
  ma = shard_a[4]/shard_a[3]
  ba = shard_a[1] - ma * shard_a[0]
  for bdx in range(adx+1,len(shards)):
    shard_b = shards[bdx]
    mb = shard_b[4]/shard_b[3]
    bb = shard_b[1] -mb * shard_b[0]
    if ma == mb: #parallel lines, would create divide-by-zero on the next step, and won't intersection
      if ba == bb: #this is a sanity check
        print(shard_a,shard_b,"ARE THE SAME LINE") #just make sure something tricky isn't happening
        exit()
      continue
    ix = (bb - ba)/(ma - mb)
    iy = ma*ix + ba

    ta = (ix - shard_a[0])/shard_a[3]
    tb = (ix - shard_b[0])/shard_b[3]

    if ta >= 0 and tb >= 0 and ix >= 200000000000000 and ix <= 400000000000000 and iy >= 200000000000000 and iy <= 400000000000000:
      count+=1

print(count) #part 1 answer

#Part 2 uses SymPy. We set up a system of equations that describes the intersections, and solve it.
x = Symbol('x')
y = Symbol('y')
z = Symbol('z')
vx = Symbol('vx')
vy = Symbol('vy')
vz = Symbol('vz')

equations = []
t_syms = []
#the secret sauce is that once you have three shards to intersect, there's only one valid line
#so we don't have to set up a huge system of equations that would take forever to solve. Just pick the first three.
for idx,shard in enumerate(shards[:3]):
  #vx is the velocity of our throw, xv is the velocity of the shard we're trying to hit. Yes, this is a confusing naming convention.
  x0,y0,z0,xv,yv,zv = shard
  t = Symbol('t'+str(idx)) #remember that each intersection will have a different time, so it needs its own variable

  #(x + vx*t) is the x-coordinate of our throw, (x0 + xv*t) is the x-coordinate of the shard we're trying to hit.
  #set these equal, and subtract to get x + vx*t - x0 - xv*t = 0
  #similarly for y and z
  eqx = x + vx*t - x0 - xv*t
  eqy = y + vy*t - y0 - yv*t
  eqz = z + vz*t - z0 - zv*t

  equations.append(eqx)
  equations.append(eqy)
  equations.append(eqz)
  t_syms.append(t)

#To my great shame, I don't really know how this works under the hood.
result = solve_poly_system(equations,*([x,y,z,vx,vy,vz]+t_syms))
print(result[0][0]+result[0][1]+result[0][2]) #part 2 answer
