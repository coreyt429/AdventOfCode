import sys
import math

# FAIL.  study stole, there is lots to learn there.

def parse_input(data):
    # Split the data into lines
    modules = {'button':{'type':'button', 'targets': ['broadcaster'] }}
    lines = data.strip().split('\n')
    for line in lines:
        module,targets = line.split(' -> ')
        moduleType=''
        if module[0] in ['%','&']:
            moduleType=module[0]
            module=module[1:]
        elif module == 'broadcaster':
            moduleType = 'broadcaster'
        modules[module] = {'type': moduleType, 'targets': targets.split(', ')}
        if modules[module]['type'] == '%':
            modules[module]['state'] = 'off'
        elif modules[module]['type'] == '&':
            modules[module]['inputs'] = {}
        if len(modules['button']['targets']) == 0:
            modules['button']['targets'].append(module)
    untyped_modules = []
    for module in modules.keys():
        for dst in modules[module]['targets']:
            if not dst in modules: # add untyped targets
                untyped_modules.append(dst)
            elif modules[dst]['type'] == '&': # they initially default to remembering a low pulse for each input.
                modules[dst]['inputs'][module] = 'low'
    for module in untyped_modules:
        #print(f'Untyped: {untyped_modules}')
        modules[module] = {'type':'untyped', 'targets': [] }

    return modules

"""
Flip-flop modules (prefix %) are either on or off; they are initially off. 
  If a flip-flop module receives a high pulse, it is ignored and nothing happens. 
  However, if a flip-flop module receives a low pulse, it flips between on and off. 
  
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""

counters = {'low': 0, 'high': 0}
press_counter=0
rx_low_press=0

def press_button(modules):
    global counters
    global press_counter
    press_counter+=1

    stack=[]
    for target in modules['button']['targets']:
        stack.append(['button',target,'low'])

    #print(stack)
    while stack:
        #print(stack)
        src,dst,sig = stack.pop(0)
        #print(f'{src} -{sig}-> {dst}')
        if dst == 'rx' and sig == 'low': # low signal to rx
            if rx_low_press == 0:
                rx_low_press == press_counter
        counters[sig]+=1
        if modules[dst]['type']=='broadcaster':
            for newdst in modules[dst]['targets']:
                stack.append([dst,newdst,sig])
        elif modules[dst]['type']=='%':
            #print(dst,modules[dst])
            if sig == 'low': # If a flip-flop module receives a high pulse, it is ignored and nothing happens. 
                if modules[dst]['state'] == 'off': #If it was off, it turns on and sends a high pulse.
                    modules[dst]['state'] = 'on'
                    for newdst in modules[dst]['targets']:
                        stack.append([dst,newdst,'high'])
                else: # If it was off, it turns on and sends a high pulse. If it was on, it turns off and sends a low pulse.
                    modules[dst]['state'] = 'off'
                    for newdst in modules[dst]['targets']:
                        stack.append([dst,newdst,'low'])
        elif modules[dst]['type']=='&':
            """
            Conjunction modules (prefix &) remember the type of the most recent pulse received from each of their connected input modules; 
            they initially default to remembering a low pulse for each input. 
            hen a pulse is received, the conjunction module first updates its memory for that input. 
            Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.
            """
            #print(f'Conjunction modules {dst}: {modules[dst]}')
            modules[dst]['inputs'][src] = sig
            newsig = 'low'
            #print(f'Inputs: {modules[dst]["inputs"]}')
            if 'low' in modules[dst]['inputs'].values():
                newsig = 'high'
            #print(f'New Signal: {newsig}')
            #print(f'Targets: {modules[dst]["targets"]}')
            for newdst in modules[dst]['targets']:
                #print(dst,newdst,newsig)
                stack.append([dst,newdst,newsig])
    if 'high' in modules['xm']['inputs'].values():
        print(f'xm recieved high {press_counter}: {modules["xm"]}')
    print(f'Press: {press_counter}, xm: {modules["xm"]}')
  
seen = set()
def path_to_rx(modules,currMod='rx'):
    global seen
    for module in modules:
        if currMod in modules[module]['targets']:
            print(f'{module} -> {currMod}')
            if module not in seen:
                seen.add(module)
                path_to_rx(modules,module)



def part1(parsed_data):
    retval = 0;
    global counters
    presses = 1000
    if len(sys.argv) == 3:
        presses = int(sys.argv[2])
    for idx in range(presses):
        #print(f'Button Press: {idx}')
        press_button(parsed_data)
        #print()
    #print(counters)
    retval = math.prod(counters.values())
    return retval

def part2(parsed_data):
    # Brute foce may take a while, looking at other options
    global rx_low_press
    while rx_low_press == 0: # keep pressing button
        press_button(parsed_data)
    retval = rx_low_press;
    #path_to_rx(parsed_data)
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
    