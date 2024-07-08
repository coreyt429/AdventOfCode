import sys
import re
import math
from copy import deepcopy


def parse_input(data):
    # Split the data into lines
    rule_block,part_block = data.strip().split('\n\n')

    rules={}
    parts=[]
    """
    'px{a<2006:qkq,m>2090:A,rfg}'split('{|}')
    {x=2127,m=1623,a=2188,s=1013}
    """
    for rule in rule_block.split('\n'):
        split_characters = r'\{|\}'  # Escaping '{' and '}' and using '|' for 'or'
        # Splitting the string
        rule_name, rule_tests, dummy  = re.split(split_characters, rule)
        rule_list = rule_tests.split(',')
        rules[rule_name] = tuple(rule_list)
        
    pattern='{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}'
    parts = [match.groups() for match in re.finditer(pattern, part_block) if match]
    #for part in part_block.split('\n'):
    #    match = re.match(pattern,part)
    #    parts.append([match.group(1),match.group(2),match.group(3),match.group(4)])

    # Split each line by whitespace and remove the first element (the label)
    return rules,parts

def accepted_part(part,rules,current='in'):
    if current == 'A':
        return True
    elif current == 'R':
        return False   
    rule = rules[current]
    for test in rule:
        matches = re.match(r'^([a-zA-Z]+)$',test)
        if matches:
            label=matches.group(1)
            return accepted_part(part,rules,label) 
        else:
            comparison,label = test.split(':')
            matches = re.match(r'([xmas])([<>])(\d+)',comparison)
            mykey = {'x':0,'m':1,'a':2,'s':3}
            if matches:
                prop=matches.group(1)
                oper=matches.group(2)
                value=int(matches.group(3))
                if oper == '<':
                    if int(part[mykey[prop]]) < value:
                        return accepted_part(part,rules,label)
                elif oper ==  '>':
                    if int(part[mykey[prop]]) > value:
                        return accepted_part(part,rules,label)
                else:
                    print(f'unkown operator in comparison: {comparison}')


def part_value(parts):
    pattern = r'(\d+)'
    total_sum = 0
    for part in parts:
        total_sum += sum(int(match.group()) for match in re.finditer(pattern, part))
    return total_sum

def find_workflows(rules,path=tuple(['in']),current='in'):
    workflows = []
    if current == 'A':
        print(f'Accepted: {path}')
        workflows.append(path)
        return workflows
    elif current == 'R':
        #print(f'Rejected: {path}')
        workflows.append(path)
        return []   
    rule = rules[current]
    for test in rule:
        matches = re.match(r'^([a-zA-Z]+)$',test)
        if matches:
            label=matches.group(1)
            newpath = list(path)
            newpath.append(label)
            newworkflows = find_workflows(rules,tuple(newpath),label)
            for workflow in newworkflows:
                workflows.append(workflow)

        else:
            comparison,label = test.split(':')
            matches = re.match(r'([xmas])([<>])(\d+)',comparison)
            mykey = {'x':0,'m':1,'a':2,'s':3}
            if matches:
                prop=matches.group(1)
                oper=matches.group(2)
                value=int(matches.group(3))
                if oper in ['<','>']:
                    newpath = list(path)
                    newpath.append(label)
                    newworkflows = find_workflows(rules,tuple(newpath),label)
                    for workflow in newworkflows:
                        workflows.append(workflow)
                else:
                    print(f'unkown operator in comparison: {comparison}')
    return workflows
"""
('px', 'qkq', 'A')
xmas = [4000,4000,4000,4000] 256,000,000,000,000
in{s<1351:px,qqz}
xmas = [4000,4000,4000,1350] 86,400,000,000,000
px{a<2006:qkq,m>2090:A,rfg}
xmas = [4000,4000,2005,1350] 29,160,000,000,000
qkq{x<1416:A,crn}
xmas = [1415,4000,2005,1350] 10,315,350,000,000
"""
def calculate_workflow(workflow,rules,current='in',ranges=tuple([tuple([1,4000]),tuple([1,4000]),tuple([1,4000]),tuple([1,4000])])):
    print(f'calculate_workflow({workflow},{current},{ranges})')
    retval=0
    counts={}
    for prop in 'xmas':
        counts[prop] = 4000
    idx=0
    rule=workflow[idx]
    #print(rule,counts,ranges)
    if rule == 'A':
        #print(f'Found A {ranges}')
        retval = math.prod((end - start + 1) for start, end in ranges)
        print(f'Returning {retval}')
    else:
        #print(f'No A: {rule}')
        buckets={}
        buckets['x']=list(ranges[0])
        buckets['m']=list(ranges[1])
        buckets['a']=list(ranges[2])
        buckets['s']=list(ranges[3])
        #print(f'Buckets: {buckets}')
        target=workflow[idx+1]
        #print(rules[rule],target)
        newworkflow=list(workflow)
        #print(rules[rule])
        #print(newworkflow)
        newworkflow.pop(0)
        #print(newworkflow)
        for test in rules[rule]:
            if test == target:
                newranges=tuple([tuple(buckets['x']),tuple(buckets['m']),tuple(buckets['a']),tuple(buckets['s'])])
                #print(f'GoTo {test} Matches {target}')
                #print("Recursion1")
                retval += calculate_workflow(newworkflow,rules,target,newranges)
            elif ':' not in test: # could the data set have a catcharll rule before  rule that matches?
                break
            elif f':{target}' in test:
                myBuckets = deepcopy(buckets)
                #Comparison x<1416:A Matches A
                comparison,label = test.split(':')
                #print(f'Comparison: {comparison}')
                matches = re.match(r'([xmas])([<>])(\d+)',comparison)
                if matches:
                    prop=matches.group(1)
                    oper=matches.group(2)
                    value=int(matches.group(3))
                    if oper == '<':
                        myBuckets[prop][1]=value-1
                        buckets[prop][0]=value
                    elif oper ==  '>':
                        myBuckets[prop][0]=value+1
                        buckets[prop][1]=value
                    #print("Recursion2")
                    newranges=tuple([tuple(myBuckets['x']),tuple(myBuckets['m']),tuple(myBuckets['a']),tuple(myBuckets['s'])])
                    retval += calculate_workflow(newworkflow,rules,target,newranges)
            elif ':' in test: # next target doesn't match, but lets adjust bucket to filter out what did
                #print(f'New check: {test}: {rules[rule]}')
                comparison,label = test.split(':')
                matches = re.match(r'([xmas])([<>])(\d+)',comparison)
                if matches:
                    prop=matches.group(1)
                    oper=matches.group(2)
                    value=int(matches.group(3))
                    # x<1500 then x:1500-4000
                    if oper == '<':
                        buckets[prop][0]=value
                    elif oper ==  '>':
                        buckets[prop][1]=value
    #print(f'Returning {retval}')
    return retval
    


def part1(parts,rules):
    retval = 0;
    for part in parts:
        if accepted_part(part,rules):
            value=part_value(part)
            retval+=value
    return retval

def part2(rules):
    retval = 0;
    workflows = set(find_workflows(rules))
    if len(sys.argv) > 2:
        workflows = [workflows[int(sys.argv[2])]]
    for workflow in workflows:
        print(workflow)
        retval+=calculate_workflow(workflow,rules)
        #print(retval)
        #exit()
    return retval

def both(ch, gt, val, ranges):
   ch = 'xmas'.index(ch)
   ranges2 = []
   for rng in ranges:
      rng = list(rng)
      lo, hi = rng[ch]
      if gt:
         lo = max(lo, val + 1)
      else:
         hi = min(hi, val - 1)
      if lo > hi:
         continue
      rng[ch] = (lo, hi)
      ranges2.append(tuple(rng))
   return ranges2

def acceptance_ranges_outer(work,rules):
    print(f'acceptance_ranges_outer: {work} {rules[work]}')
    return acceptance_ranges_inner(rules[work],rules)

def acceptance_ranges_inner(w,rules):
    print(f'acceptance_ranges_outer({w})')
    #acceptance_ranges_outer(('s<1351:px', 'qqz'))
    it = w[0]
    print(f'it: {it}')
    if it == "R":
        return []
    if it == "A":
        return [((1, 4000), (1, 4000), (1, 4000), (1, 4000))]
    if ":" not in it:
        return acceptance_ranges_outer(it,rules)
    cond = it.split(":")[0]
    print(f'cond: {cond}')
    gt = ">" in cond
    print(f'gt: {gt}')
    ch = cond[0]
    print(f'ch: {ch}')
    val = int(cond[2:])
    print(f'val: {val}')
    val_inverted = val + 1 if gt else val - 1
    print(f'val_inverted: {val_inverted}')
    if_cond_is_true = both(ch, gt, val, acceptance_ranges_inner([it.split(":")[1]],rules))
    if_cond_is_false = both(ch, not gt, val_inverted, acceptance_ranges_inner(w[1:],rules))
    return if_cond_is_true + if_cond_is_false


def part2b(rules):
    retval = 0;
    for rng in acceptance_ranges_outer('in',rules):
        print(f'Range: {rng}')
        v = 1
        for lo, hi in rng:
            print(f'{hi} - {lo}')
            v *= hi - lo + 1
            print(f'{v} *= {hi} - {lo} + 1')
        retval += v
    return retval

if __name__ == "__main__":
    with open(sys.argv[1] , "r") as f:
        rules,parts = parse_input(f.read())
    #print(f'Rules: {rules}')
    #print(f'Parts: {parts}')

    #print("Part 1")
    answer1 = part1(parts,rules)
    
    #print("Part 2")
    answer2 = part2(rules)
    answer2b = part2b(rules)

    print(f"Part1:  {answer1}")
    print(f"Part2:  {answer2}")
    print(f"Part2b: {answer2b}")
    