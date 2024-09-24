"""
Advent Of Code 2019 day 13

This one was pretty fun. I'm really starting to like my Grid() class.
It didn't require any tweaks this time, and is really fast now that
I've learned not to use update() frequently.

IntCodeComputer() also didn't require any changes this time.  Though,
I was tempted to add a next_op method to check for input ops, but opted
to just do that in the part_2 instead since it was just two lines of
code (which really could have been one, but I'll leave it two for readability):
    instruction_text = str(self.icc.program[self.icc.ptr])
    op_code = int(instruction_text[-2:]) 
    # alternate form
    op_code = int(str(self.icc.program[self.icc.ptr])[-2:]) 

I started overthinking the game logic, but kept my self disciplined to
trying the simplest case first, and that worked.

My game play logic, was pretty much just have the paddle follow the ball.
Actually, now that I think about it, that is probably all I really had to do
was move the paddle to the ball, but my calculations work, so I'll leave it alone.

I was initially concerned that there may be a case for more than one ball, or
paddle.  Then on rereading, the instructions referred to them as "the ball" and
"the paddle" so I didn't start down that path.

I also wondered if I needed to be concerned about trajectory changes from hitting
blocks and walls.  But following the line out to calculate what the ball might hit
would have been more resource intensive, so luckily that was not needed.

This did give me an opportunity to revisit slope and intercept formulas. So there
was a math lesson as well. 

"""
# import system modules
import time

# import my modules
from intcode import IntCodeComputer # pylint: disable=import-error
import aoc # pylint: disable=import-error
from grid import Grid # pylint: disable=import-error

class ArcadeCabinet(Grid):
    """
    Class to represent arcade cabinet
    
    This class extends Grid() and adds an IntCodeComputer() for processing
    """

    def __init__(self, program):
        """
        Init Method
        """
        # init super() to configure grid
        # Since we have a fixed size, and cartesion will flip the game upside down
        # I went ahead and filled the screen as 24x45 0's and used screen coordinates
        super().__init__(['0'*45]*24, coordinate_system='screen', use_overrides=False)
        # init computer
        self.icc = IntCodeComputer(program)
        # set default_value ob_default_value to empty.
        self.cfg['default_value'] = '0'
        self.cfg['ob_default_value'] = '0'
        # redefine self.icc.output.  It is None by default
        self.icc.output = []
        # init square_count
        self.square_count = 1
        # init ball and paddle positions to None
        self.last_ball = None
        self.ball = None
        self.paddle = None
        # init score
        self.score = 0

    def process_square(self):
        """
        Method to process a square the robot enters
        """
        # every three output instructions specify the x position (distance from the left),
        #  y position (distance from the top), and tile id
        while len(self.icc.output) < 3:
            # break when ptr is outside program
            if not 0 <= self.icc.ptr < len(self.icc.program):
                # print(f"ptr: {self.icc.ptr} is OOB")
                break
            # get current intstruction string
            instruction_text = str(self.icc.program[self.icc.ptr])
            # print(f"instruction_text: {instruction_text}")
            # the opcode is the rightmost two digits of the first value in an instruction.
            op_code = int(instruction_text[-2:])
            # does the next step require input?
            if op_code == 3:
                # get target position for paddle to intercept ball
                target = self.paddle_target()
                # If the joystick is in the neutral position, provide 0.
                # If the joystick is tilted to the left, provide -1.
                # If the joystick is tilted to the right, provide 1.
                # how far should we move?
                delta_x = target[0] -  self.paddle[0]
                # init joystick to neutral 0
                joystick = 0
                # if target is to the right, move joystick right
                if delta_x > 0:
                    joystick = 1
                # if target is to the left, move joystick left
                elif delta_x < 0:
                    joystick = -1
                # add joystick to input queue
                self.icc.inputs.append(joystick)
            # take next step
            self.icc.step()
        # process outputs
        if self.icc.output:
            # x value
            x_val = self.icc.output.pop(0)
            # y value
            y_val = self.icc.output.pop(0)
            # type
            square_type = self.icc.output.pop(0)
            # When three output instructions specify X=-1, Y=0,
            # the third output instruction is not a tile
            if (x_val, y_val) == (-1, 0):
                self.score = square_type
                # print(f"new score: {self.score}")
            else:
                # set point in grid
                self.set_point((x_val, y_val), str(square_type))
                # 4 is a ball tile. The ball moves diagonally and bounces off objects
                if square_type == 4:
                    # track ball position
                    self.last_ball = self.ball
                    self.ball = (x_val, y_val)
                    # init last_ball if still None
                    if self.last_ball is None:
                        self.last_ball = self.ball
                # 3 is a horizontal paddle tile. The paddle is indestructible
                if square_type == 3:
                    # track paddle position
                    self.paddle = (x_val, y_val)

    def paddle_target(self):
        """
        Method to calculate where the paddle should move
        based on ball trajectory
        """
        # going up
        if self.ball[1] > self.last_ball[1]:
            # just track the ball if it is going up.
            return (self.ball[0], self.paddle[1])
        # going down
        # try to guess where it will hit row 22
        # get change in x and y values from last two positions
        delta_y = self.ball[1] - self.last_ball[1]
        delta_x = self.ball[0] - self.last_ball[0]
        # ball didn't move, (init case, since we set last_ball to ball at the first position)
        # set slope to 1
        if delta_x == delta_y:
            slope = 1
        else:
            # otherwise, calculate slope
            slope = delta_y / delta_x
        # calculate new x value
        new_x = self.ball[0] + (self.ball[1] - self.paddle[1]) / slope
        # return target position for paddle
        return (new_x, self.paddle[1])

def part_1(input_value):
    """
    Function to run part 1
    """
    # init game
    game = ArcadeCabinet(input_value)
    # loop until game is complete
    while 0 <= game.icc.ptr < len(game.icc.program):
        # process square
        game.process_square()
    # update map
    game.update()
    # print(len(game.map))
    # return count of 2's
    return str(game).count('2')

def part_2(input_value):
    """
    function to run part 2
    """
    # init game
    game = ArcadeCabinet(input_value)
    # insert two quarters:
    game.icc.program[0] = 2
    # loop until game is complete
    while 0 <= game.icc.ptr < len(game.icc.program):
        # process square
        game.process_square()
        # from part 1, we know the screen size is 1080 char
        # update is expensive, so lets just run it once
        # when we reach 1080
        if game.square_count < 1080:
            # update square_count
            game.square_count = len(game.map)
            # if we reached 1080, update
            if game.square_count > 1079:
                game.update()
        # ball and paddle tracking debug statements
        # else:
        #     print(f"ball: {game.ball}")
        #     print(f"paddle: {game.paddle}")
    # return last game score
    return game.score

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 1:
        return part_1(input_value)
    return part_2(input_value)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2019,13)
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
        1: 296,
        2: 13824
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
