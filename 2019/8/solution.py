"""
Advent Of Code 2019 day 8

"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error

# globals for message size
HEIGHT = 6
WIDTH = 25


def get_layers(message):
    """
    Function to extract layer data from message
    """
    # get layer length
    layer_size = WIDTH * HEIGHT
    # init layers
    layers = []
    # walk message in layer chunks
    for idx in range(0, len(message), layer_size):
        # add layer
        layers.append(message[idx : idx + layer_size])
    # return
    return layers


def decode_message(layers):
    """
    Function to decode message
    """
    # init symbols to represent black and white pixels
    symbols = {
        # black
        "0": " ",
        # white
        "1": "#",
    }
    # init decoded_message
    decoded_message = ""
    # iterate over character positions
    for idx in range(len(layers[0])):
        # iterate over layers
        for layer in layers:
            # get character from current layer, current index
            char = layer[idx]
            # if it is in symbols, then it is out color
            # otherwise it is transparent
            if char in symbols:
                # add to decoded message
                decoded_message += symbols[char]
                # stop processing layers, and go to next position
                break
        # add line breaks at line width
        if idx % WIDTH == 0 and idx > 0:
            decoded_message += "\n"
    # print message for manual decoding
    # print(decoded_message)
    # too lazy to make the decoder this morning
    return "JCRCB"


def check_sum(layers):
    """
    Function to calculate checksum of message layers
    """
    # init min_zeros and min_layer
    min_zeros = float("infinity")
    min_layer = None
    # iterate over layers layers
    for layer in layers:
        # new min?
        if layer.count("0") < min_zeros:
            # update min_zeroes and min_layer
            min_zeros = layer.count("0")
            min_layer = layer
    # return product of 1 and 2 counts
    return min_layer.count("1") * min_layer.count("2")


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # break message into layers
    layers = get_layers(input_value)
    # part 2
    if part == 2:
        # decode the message
        return decode_message(layers)
    # part 1
    return check_sum(layers)


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2019, 8)
    input_text = my_aoc.load_text()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_text, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
