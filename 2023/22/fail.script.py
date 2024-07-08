import sys

"""
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""

def parse_input(data):
    # Split the data into lines
    lines = data.strip().split('\n')
    bricks = []
    idx=0
    for line in lines:
        a,b = line.split('~')
        a = [int(x) for x in a.split(',')]
        b = [int(x) for x in b.split(',')]
        bricks.append([tuple(a), tuple(b), *cubes([tuple(a), tuple(b)])])
        idx+=1
    return sorted(bricks, key=lambda brick: brick[0][2])

def cubes(brick):
    myCubes = set()
    canSupport = set()
    needSupport = set()
    #print(f'cubes({brick})')
    for x in range(brick[0][0],brick[1][0]+1):
        for y in range(brick[0][1],brick[1][1]+1):
            for z in range(brick[0][2],brick[1][2]+1):
                myCubes.add(tuple([x,y,z]))
                canSupport.add(tuple([x,y,z+1]))
                if z > 1:
                    needSupport.add(tuple([x,y,z-1]))
    return myCubes, canSupport, needSupport

def is_cube_supported(cube,mybrick,bricks):
    retval = False
    #print(f'is_cube_supported({cube},{mybrick},bricks)')
    x,y,z = cube
    drop = z
    cube_support = (x,y,z-1)
    if z == 1: # cube is on the ground
        #print(f'is_cube_supported({cube}) - ground level')
        #print('Ground floor')
        cube_support = (x,y,0)
        drop=0
        retval = True
    elif cube_support  in mybrick[2]:
        #print(f'is_cube_supported({cube}) - vertically supported in self {mybrick[2]}')
        retval = False # False because any True makes True, so True here will leave a vertical block hanging in the air
    else:
        needs = mybrick[4]
        for brick in bricks:
            if brick == mybrick:
                continue
            for cube2 in brick[2]:
                if cube2 == cube_support:
                    drop=0
                    retval = True
                elif cube2[:-1] == (x,y):
                    if cube2[2] < z:
                        diff = z-cube2[2]
                        #print(cube,cube2)
                        #print(f'cube diff: {diff} < {drop}')
                        if diff < drop:
                            drop = diff
                            if drop > max(brick[0][2],brick[1][2]):
                                drop=max(brick[0][2],brick[1][2])
                            else:
                                drop-=1

    #print(f'is_cube_supported returning: {cube} {retval},{drop},{cube_support}')
    if not retval:
        cube_support = None
    if z - drop < 1:
        drop=z-1
    return retval, drop, cube_support

def is_brick_supported(mybrick,bricks):
    retval=False
    drop = 10**9
    cube_supports = set()
    needs = mybrick[4] # needed supports
    for brick in bricks:
        if brick == mybrick:
            continue
        provides = brick[2] # actual cubes
        #print(f'Needs: {needs} Provides: {provides}')
        common_exists = any(element in needs for element in provides)
        if common_exists:
            #print('A')
            common_elements = needs & provides
            for em in common_elements:
                cube_supports.add(em)
            retval = True
    # use old method to calculate drop
    if not retval:
        #print('B')
        for cube in mybrick[2]:
            support, diff, cube_support = is_cube_supported(cube,mybrick,bricks)
            if cube_support and cube_support not in brick[2]:
                cube_supports.add(cube_support)
            if support:
                retval=True
            else:
                #print(f'brick diff: {diff} < {drop}')
                if diff < drop:
                    drop = diff
                    #print(f'return {retval}, {drop}')
                    if drop > max(mybrick[0][2],mybrick[1][2]):
                            print('Bailing')
                            print(f'is_brick_supported({mybrick}) - {drop}')
                            exit()
    #print(f'returning {retval}, {drop}, {cube_supports}')
    return retval, drop, cube_supports

def is_brick_supported_orig(brick,bricks):
    retval=False
    drop = 10**9
    cube_supports = []
    for cube in brick[2]:
        support, diff, cube_support = is_cube_supported(cube,brick,bricks)
        if cube_support and cube_support not in brick[2]:
            cube_supports.append(cube_support)
        if support:
            retval=True
        else:
            #print(f'brick diff: {diff} < {drop}')
            if diff < drop:
                drop = diff
                #print(f'return {retval}, {drop}')
                if drop > max(brick[0][2],brick[1][2]):
                        print('Bailing')
                        print(f'is_brick_supported({brick}) - {drop}')
                        exit()
    print(f'returning {retval}, {drop}, {cube_supports}')
    return retval, drop, cube_supports

def still_supported(brick,bricks,removed):
    #print(f'  still_supported({brick},bricks,{removed})')
    supported, drop, supports =  is_brick_supported(brick,bricks)
    #print(f'    {supported}, {drop}, {supports}')
    retval = False
    support_count = len(supports)
    #print(f'    Starting with {support_count} supports: {supports}')
    missing = []
    remaining = []
    for cube in supports:
        found = False
        #print(f'Removed: {removed}')
        for brick2 in removed:
            #print(f'{cube} in {brick2[2]} == {cube in brick2[2]}')
            if cube in brick2[2]:
                support_count-=1
                #print(f'Found ')
                found = True        
        if found:
            missing.append(cube)
        else:
            remaining.append(cube)
    if  remaining:
        #print(f'Remaining: {remaining}')
        retval = True
    #print(f'    Ending with {len(remaining)} supports: {remaining}')
    #print(f'    still_supported == {retval} {support_count} {missing} {remaining}')
    return retval

def still_stable(bricks,removed):
    #print(f'still_stable(bricks,{removed})')
    retval = True
    for brick in bricks:
        if brick in removed: # skip removed bricks
            #print(f'Skipping self: {brick}')
            continue
        else:
            #print(f'  Checking {brick}')
            supported = still_supported(brick,bricks,removed)
            #print(f'  Checking {brick} - {supported}')
            if not supported:               
                retval = False
    print(f'still_stable() {retval}')
    return retval

def lower_brick(brick,drop):
    #print(f'In: lower_brick({brick[:-1]},{drop})')
    for end in [0,1]:
        x,y,z = brick[end]
        z-=drop
        if z < 1:
            print('Bailing')
            print(f'lower_brick({brick[:-1]},{drop})')
            print(f'new z: {z}')
            exit()
        brick[end] = (x,y,z)
    brick[2], brick[3], brick[4]  = cubes(brick[:-1])
    #print(f'Out: lower_brick({brick[:-1]},{drop})')
    

def settle_bricks(bricks):
    movement = True
    idx=0
    while movement:
        idx+=1
        print(f'Settle Pass: {idx}')
        movement = False
        idx2 = 0
        for brick in bricks:
            idx2+=1
            print(f'Pass: {idx}  Brick: {idx2} {brick}')
            supported, drop, supports = is_brick_supported(brick,bricks)
            #print(f'{supported}, {drop}, {supports}')
            #print(f'settling: {brick}, {drop}')
            while not supported:
                movement = True
                lower_brick(brick,drop)
                supported, drop, supports = is_brick_supported(brick,bricks)
                #print(f'{supported}, {drop}')

def part1(bricks):
    retval=0
    settle_bricks(bricks)
    #for brick in bricks:
    #    print(brick[2])
    idx=0
    stable = []
    for brick in bricks:
        idx+=1
        print(f'Removing {idx}: {brick}')
        if still_stable(bricks,[brick]):
            stable.append(True)
            retval+=1
        else:
            stable.append(False)
    
    #for brick in bricks:
    #    print(brick[3],brick[2])
    #print(stable)
    return retval


def part2(parsed_data):
    retval = 0;
    return retval

if __name__ == "__main__":
    with open(sys.argv[1] , "r") as f:
        parsed_data = parse_input(f.read())
    #print(parsed_data)

    #print("Part 1")
    answer1 = part1(parsed_data)
    
    #print("Part 2")
    answer2 = part2(parsed_data)

    print(f"Part1: {answer1}")
    print(f"Part2: {answer2}")
    