"""
Advent Of Code 2019 day 25

I'm sure I should have setup a shortest path algorithm and taught the
droid to explore the map.  It was just more fun to play the game on this
one.  So I mapped out the rooms and items, identified the useful/dangerous
items.  Instructed the droid to pickup all the useful items and take them to the
security checkpoint.  From there, just drop them all, and try the combinations
of items until one works.

If I take all the items to the security check point, it takes about 12 seconds
to solve.  The current iteration is optimized for the known solution only
picking up the needed items and iterating over their combinations so it runs
it a little over 1 second.

                                             Corridor*
                                               |
                           Kitchen --------- Hallway!
                             |                 |
                             |               Observatory*
                             |
                    Hot Chocolate Fountain* - Passages!
                              | 
                           crew quarters* --- Stables
                              |                 |
                              |              Arcade* ----- Science Lab!
                              |                 |
                              |              Engineering - Navigation*
                              |         
                              |
                           storage ------------------------ hull breach
                              |                                  |
                              |      Gift Wrapping Center* - sick bay! - Warp Drive Maintenance*
Security Checkpoint     -  Holodeck   
      |
 pressure plate


Items
jam - Crew Quarters
astronaut ice cream - Hot Chocolate Fountain
molten lava - Hallway - ends program
photons - Sick Bay - ends program
space heater - Warp Drive Maintenance
shell - Gift Wrapping Center
asterisk - Arcade
giant electromagnet - Science Lab - picking up seems bad
spool of cat6 - Navigation
escape pod - Passages - ends program
infinite loop - Corridor - starts infinite loop
space law space brochure - Observatory


"Alert! Droids on this ship are lighter than the detected value!"
   - all
      - spool of cat6
      - space law space brochure
      - asterisk
      - jam
      - shell
      - astronaut ice cream
      - space heater
      - klein bottle
   - pairs
     - a
       - jam
       - astronaut ice cream
     - b
       - shell
       - astronaut ice cream
      

"Alert! Droids on this ship are heavier than the detected value!"
  - none
  - jam
    - jam

"""
# import system modules
import time
from itertools import combinations
import re

# import my modules
from intcode import IntCodeComputer # pylint: disable=import-error
import aoc # pylint: disable=import-error

def get_item_commands():
    """
    Function to generate commands for possible combinations
    of items
    """
    commands = []
    # winning combination
    # - asterisk
    # - astronaut ice cream
    # - space heater
    # - klein bottle
    # unnecessary items commented out
    items = [
        # 'spool of cat6',
        # 'space law space brochure',
        'asterisk',
        # 'jam',
        # 'shell',
        'astronaut ice cream',
        'space heater',
        'klein bottle']
    # drop all items at the security checkpoint
    for item in items:
        commands.append(f"drop {item}")
    # try possible combinations
    for size in range(1, len(items) + 1):
        for combo in combinations(items, size):
            for item in combo:
                commands.append(f"take {item}")
            # commands.append("inv")
            commands.append("south")
            for item in combo:
                commands.append(f"drop {item}")
    return commands

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        return "Align the warp drive"
    icc = IntCodeComputer(input_value)
    icc.output = []
    # initial commands to walk around, pickup all items, and go to the security checkpoint
    # commands commented out to optimize route and not pickup unnecessary items
    commands = [
        "south",
        #"west",
        #"take shell",
        #"east",
        "east",
        "take space heater",
        "west",
        "north",
        "inv",
        "west",
        "north",
        #"take jam",
        "east",
        "south",
        "take asterisk",
        "south",
        "take klein bottle",
        #"east",
        #"take spool of cat6",
        #"west",
        "north",
        "north",
        "west",
        "north",
        "take astronaut ice cream",
        #"north",
        #"east",
        #"south",
        #"take space law space brochure",
        #"north",
        #"west",
        #"south",
        "south",
        "south",
        "south",
        "west",
    ]
    # add commands to try item combinations
    commands.extend(get_item_commands())
    # uncomment for manual exploration
    # commands = []
    while True:
        # if icc.next_op_code() is None:
        #     print("program ended")
        #     break
        while icc.next_op_code() != 3:
            if icc.next_op_code() is None:
                break
            icc.step()
        output_string = ''
        while icc.output:
            output_string += chr(icc.output.pop(0))
        # uncomment when playing manually
        # print(output_string)
        # A loud, robotic voice says "Analysis complete! You may proceed."
        # and you enter the cockpit. Santa notices your small droid, looks puzzled
        # for a moment, realizes what has happened, and radios your ship directly.
        if 'keypad' in output_string:
            break
        if commands:
            input_string = commands.pop(0)
        else:
            input_string = input("Enter a command: ").strip()
        # print(f"you entered: {input_string}")
        for char in input_string:
            icc.inputs.append(ord(char))
        icc.inputs.append(10)
        while icc.inputs:
            icc.step()
    # "Oh, hello! You should be able to get in by typing 2105377 on the keypad
    # at the main airlock."
    return int(re.findall(r'\d+', output_string)[0])

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2019,25)
    input_text = my_aoc.load_text()
    # parts dict to loop
    parts = {
        1: 1,
        2: 2
    }
    # dict to store answers
    answer = {
        1: None,
        2: None
    }
    # correct answers once solved, to validate changes
    correct = {
        1: 2105377,
        2: "Align the warp drive"
    }
    # dict to map functions
    funcs = {
        1: solve,
        2: solve
    }
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_text, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
