"""
Advent Of Code 2021 day 16

"""
# import system modules
import time
import math
# import my modules
import aoc # pylint: disable=import-error

func_map = {
    # Packets with type ID 0 are sum packets - their value is the sum of the values of their
    # sub-packets. If they only have a single sub-packet, their value is the value of the
    # sub-packet.
    0: lambda packets: sum((execute_packet(sub_packet) for sub_packet in packets)),
    # Packets with type ID 1 are product packets - their value is the result of multiplying
    # together the values of their sub-packets. If they only have a single sub-packet, their
    # value is the value of the sub-packet.
    1: lambda packets: math.prod((execute_packet(sub_packet) for sub_packet in packets)),
    # Packets with type ID 2 are minimum packets - their value is the minimum of the values
    # of their sub-packets.
    2: lambda packets: min((execute_packet(sub_packet) for sub_packet in packets)),
    # Packets with type ID 3 are maximum packets - their value is the maximum of the values
    # of their sub-packets.
    3: lambda packets: max((execute_packet(sub_packet) for sub_packet in packets)),
    # Packets with type ID 5 are greater than packets - their value is 1 if the value
    # of the first sub-packet is greater than the value of the second sub-packet; otherwise,
    # their value is 0. These packets always have exactly two sub-packets.
    5: lambda packets: 1 if execute_packet(packets[0]) > execute_packet(packets[1]) else 0,
    # Packets with type ID 6 are less than packets - their value is 1 if the value of the
    # first sub-packet is less than the value of the second sub-packet; otherwise, their
    # value is 0. These packets always have exactly two sub-packets.
    6: lambda packets: 1 if execute_packet(packets[0]) < execute_packet(packets[1]) else 0,
    # Packets with type ID 7 are equal to packets - their value is 1 if the value of the
    # first sub-packet is equal to the value of the second sub-packet; otherwise, their
    # value is 0. These packets always have exactly two sub-packets.
    7: lambda packets: 1 if execute_packet(packets[0]) == execute_packet(packets[1]) else 0
}

def execute_packet(packet):
    """Function to execute packets recursively"""
    if packet['packet_type'] in func_map:
        return func_map[packet['packet_type']](packet['packets'])
    # Packets with type ID 4 are Literal values - represent a single number as described above
    if packet['packet_type'] == 4:
        return packet['value']
    return -1

def hex_to_binary(hex_string):
    """Function to convert hex string to binary atring"""
    # Convert hex string to integer
    integer_value = int(hex_string, 16)
    length = len(hex_string) * 4
    # Convert integer to binary string with specified length
    return f'{integer_value:0{length}b}'

def binary_to_int(binary_string):
    """Function to convert binary string to int"""
    return int(binary_string, 2)

def get_packet_version(binary_string):
    """Function to extract packet version"""
    return binary_to_int(binary_string[0:3])

def get_packet_type(binary_string):
    """Function to extract packet type"""
    return binary_to_int(binary_string[3:6])

def get_literal_value(binary_string):
    """Function to get literal value of a packet"""
    # To do this, the binary number is padded with leading zeroes
    # until its length is a multiple of four bits, and then it is broken into groups of
    # four bits. Each group is prefixed by a 1 bit except the last group, which is prefixed
    # by a 0 bit. These groups of five bits immediately follow the packet header. For example,
    # the hexadecimal string D2FE28 becomes:
    # 110100101111111000101000
    # VVVTTTAAAAABBBBBCCCCC
    value_string = ''
    ptr = 6
    stop_bit = '1'
    while stop_bit == '1':
        stop_bit = binary_string[ptr]
        value_string += binary_string[ptr+1:ptr+5]
        ptr += 5
    remainder_string = binary_string[ptr:]
    return int(value_string,2), remainder_string

def parse_packet(hex_string):
    """Function to parse packets recursively"""
    binary_string = hex_string
    if any((char in '23456789abcef' for char in hex_string)):
        binary_string = hex_to_binary(hex_string)
    packet_version = get_packet_version(binary_string)
    packet_type = get_packet_type(binary_string)
    if packet_type == 4:
        # Packets with type ID 4 represent a literal value. Literal value packets encode a
        # single binary number.
        value, remainder_string = get_literal_value(binary_string)
        return {
            'packet_version': packet_version,
            'packet_type': packet_type,
            'value': value }, remainder_string
    length_type = binary_string[6]
    if length_type == '0':
        # If the length type ID is 0, then the next 15 bits are a number that represents the total
        # length in bits of the sub-packets contained by this packet.
        length = 15
        payload_length = binary_to_int(binary_string[7:7+length])
        payload_start = 7 + length
        payload = binary_string[payload_start:payload_start + payload_length]
        remainder_string = binary_string[(payload_start + payload_length):]
        working_string = payload
        packets = []
        while '1' in working_string:
            packet, working_string = parse_packet(working_string)
            packets.append(packet)
        return {
            'packet_version': packet_version,
            'packet_type': packet_type,
            'length_type': length_type,
            'payload_length': payload_length,
            'payload': payload,
            'packets': packets}, remainder_string
    # If the length type ID is 1, then the next 11 bits are a number that represents
    # the number of sub-packets immediately contained by this packet.
    length = 11
    sub_packets = binary_to_int(binary_string[7:7+length])
    remainder_string = binary_string[7 + length:]
    packets = []
    for _ in range(sub_packets):
        packet, remainder_string = parse_packet(remainder_string)
        packets.append(packet)
    return {
        'packet_version': packet_version,
        'packet_type': packet_type,
        'length_type': length_type,
        'packets': packets}, remainder_string

def get_packet_versions(packet_list):
    """Function to get packet version"""
    versions = []

    for packet in packet_list:
        # Add the packet_version of the current packet
        versions.append(packet['packet_version'])
        # Recursively process the nested packets
        if 'packets' in packet and packet['packets']:
            versions.extend(get_packet_versions(packet['packets']))
    return versions

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    packets = []
    remainder_string = input_value
    while '1' in remainder_string:
        packet, remainder_string = parse_packet(remainder_string)
        packets.append(packet)
    if part == 2:
        return execute_packet(packet)
    return sum(get_packet_versions(packets))

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2021,16)
    input_data = my_aoc.load_text()
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
        1: 917,
        2: 2536453523344
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
        answer[my_part] = funcs[my_part](input_data, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
