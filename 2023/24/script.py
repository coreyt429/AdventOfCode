import sys
from sympy import Symbol
from sympy import solve_poly_system
from z3 import Solver, Real, Reals, sat
import time
start_time = time.time()


"""
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""

def time_stamp(label):
    global start_time
    current_time = time.time()
    runtime_seconds = current_time - start_time
    print(f"{label}: {runtime_seconds} seconds")

def parse_input(data):
    # Split the data into lines
    lines = data.strip().split('\n')
    hail=[]
    for line in lines:
        strPos,strVel = line.split(' @ ')
        pos = [int(x) for x in strPos.split(', ')]
        vel = [int(x) for x in strVel.split(', ')]
        hail.append({"pos":pos, "vel":vel})
    return hail


def find_intersection_and_check_time(pointa, pointb):
    posA_x, posA_y = pointa['pos'][0], pointa['pos'][1]
    velA_x, velA_y = pointa['vel'][0], pointa['vel'][1]

    posB_x, posB_y = pointb['pos'][0], pointb['pos'][1]
    velB_x, velB_y = pointb['vel'][0], pointb['vel'][1]

    a, b, c, d = velA_x, -velB_x, velA_y, -velB_y
    e, f = posB_x - posA_x, posB_y - posA_y
    denominator = a * d - b * c

    if denominator == 0:
        return None, False, False  # Lines are parallel or coincident

    t = (e * d - b * f) / denominator
    s = (a * f - e * c) / denominator

    intersection_x = posA_x + velA_x * t
    intersection_y = posA_y + velA_y * t

    intersection_point = (intersection_x, intersection_y)
    past_for_pointa = t < 0
    past_for_pointb = s < 0
    return intersection_point, past_for_pointa, past_for_pointb


def part1(parsed_data,target):
    # for idx in hail
    # calculate times both x and y are within target[0] and target[1] inclusive
    retval=0
    for i in range(len(parsed_data)):
        pointa = parsed_data[i]
        for j in range(i+1,len(parsed_data)):
            pointb = parsed_data[j]
            if pointa == pointb:
                continue
            intersection, past_for_pointa, past_for_pointb = find_intersection_and_check_time(pointa, pointb)
            #print(f'Hailstone A: {pointa["pos"][0]}, {pointa["pos"][1]}, {pointa["pos"][2]} @ {pointa["vel"][0]}, {pointa["vel"][1]}, {pointa["vel"][2]}')
            #print(f'Hailstone B: {pointb["pos"][0]}, {pointb["pos"][1]}, {pointb["pos"][2]} @ {pointb["vel"][0]}, {pointb["vel"][1]}, {pointb["vel"][2]}')
            if intersection:
                if past_for_pointa and past_for_pointb:
                    #print(f"Hailstones' paths crossed in the past for both hailstones.")
                    past=True
                elif past_for_pointa:
                    #print(f"Hailstones' paths crossed in the past for hailstone A.")
                    past=True
                elif past_for_pointb:
                    #print(f"Hailstones' paths crossed in the past for hailstone B.")
                    past=True
                else:
                    x,y = intersection
                    location='outside'
                    if target[0] <= x <= target[1] and  target[0] <= y <= target[1]:
                        retval+=1
                        location = 'inside'
                    #formatted_x = f"{x:.3f}".rstrip('0').rstrip('.')
                    #formatted_y = f"{y:.3f}".rstrip('0').rstrip('.')
                    #print(f"Hailstones' paths will cross {location} the test area (at x={formatted_x}, y={formatted_y}).")
            #else:
                #print("Hailstones' paths are parallel; they never intersect.")
            #print()
    return retval


def part2(line_data): # sympy solution works for 3 or more lines, but is slow for the entire list
    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')
    vx = Symbol('vx')
    vy = Symbol('vy')
    vz = Symbol('vz')
    equations = []
    t_syms = []
    for idx,line in enumerate(line_data[:3]):
        x0,y0,z0 = line['pos']
        xv,yv,zv = line['vel']
        #print(x0,y0,z0,xv,yv,zv)
        t = Symbol('t'+str(idx))
        eqx = x + vx*t - x0 - xv*t
        eqy = y + vy*t - y0 - yv*t
        eqz = z + vz*t - z0 - zv*t

        equations.append(eqx)
        equations.append(eqy)
        equations.append(eqz)
        t_syms.append(t)
    result = solve_poly_system(equations,*([x,y,z,vx,vy,vz]+t_syms))
    #print(result)
    return(result[0][0]+result[0][1]+result[0][2])

def part2_z3(line_data): # z3 solves for the whole list
    x, y, z = Reals('x y z')
    vx, vy, vz = Reals('vx vy vz')
    solver = Solver()

    for idx, line in enumerate(line_data[:3]):
        x0, y0, z0 = line['pos']
        xv, yv, zv = line['vel']

        t = Real('t' + str(idx))

        solver.add(x + vx * t == x0 + xv * t)
        solver.add(y + vy * t == y0 + yv * t)
        solver.add(z + vz * t == z0 + zv * t)

    if solver.check() == sat:
        model = solver.model()
        #print(model)
        # Extracting the solution
        return int(model[x].as_decimal(10))+int(model[y].as_decimal(10))+int(model[z].as_decimal(10))
    else:
        return "No solution"

if __name__ == "__main__":
    with open(sys.argv[1] , "r") as f:
        parsed_data = parse_input(f.read())
    #print(parsed_data)
    target = (int(sys.argv[2]),int(sys.argv[3]))

    #print("Part 1")
    #time_stamp('p1')
    answer1 = part1(parsed_data,target)
    
    #print("Part 2")
    #time_stamp('p2')
    #answer2 = part2(parsed_data)
    #time_stamp('p2z3')
    answer2z3 = part2_z3(parsed_data)

    print(f"Part1:    {answer1}")
    #print(f"Part2:    {answer2}")
    print(f"Part2 z3: {answer2z3}")
