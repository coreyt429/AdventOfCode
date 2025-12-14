"""
AdventOfCode 2016 4

Each room consists of an encrypted name (lowercase letters separated by dashes)
followed by a dash, a sector ID, and a checksum in square brackets.

A room is real (not a decoy) if the checksum is the five most common letters
in the encrypted name, in order, with ties broken by alphabetization. For example:

aaaaa-bbb-z-y-x-123[abxyz] is a real room because the most common letters are
                            a (5), b (3), and then a tie between x, y,
                            and z, which are listed alphabetically.
a-b-c-d-e-f-g-h-987[abcde] is a real room because although the letters are all
                            tied (1 of each), the first five are listed alphabetically.
not-a-real-room-404[oarel] is a real room.
totally-real-room-200[decoy] is not.
Of the real rooms from the list above, the sum of their sector IDs is 1514.
What is the sum of the sector IDs of the real rooms?

I was getting really modern here, just had to refactor to current format, and
streamline a bit.
"""

# import system modules
import logging
import argparse
import re
from heapq import heappush, heappop

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_input(input_text):
    """
    Parses input data
    """
    input_pattern = re.compile(r"(.*)-(\d+)\[(\w*)\]")
    data = []
    for line in input_text.strip().splitlines():
        if not line:
            continue
        matches = input_pattern.match(line)
        data.append(
            {
                "letters": matches.group(1),
                "sectorId": int(matches.group(2)),
                "checksum": matches.group(3),
            }
        )
    return data


def build_checksum(letters):
    """
    Function to build checksum
    """
    heap = []
    for letter in set(letters):
        score = -1 * letters.count(letter)
        heappush(heap, (score, letter))
    checksum = ""
    for _ in range(5):
        score, letter = heappop(heap)
        checksum += letter
    return checksum


def check_checksum(letters, checksum):
    """
    Function to compare checksums
    """
    return build_checksum(letters.replace("-", "")) == checksum


def decrypt(message, cipher_key):
    """
    Function to decrypt codes
    To decrypt a room name, rotate each letter forward through the alphabet a
    number of times equal to the room's sector ID. A becomes B, B becomes C, Z
    becomes A, and so on. Dashes become spaces.
    For example, the real name for qzmt-zixmtkozy-ivhz-343 is very encrypted name.
    """
    offset = cipher_key % 26
    message.replace("-", " ")
    decrypted_message = ""
    for char in message:
        if char == "-":
            char = " "
        else:
            char_num = ord(char)
            char_num += offset
            if char_num > 122:
                char_num -= 26
            char = chr(char_num)
        decrypted_message += char
    return decrypted_message


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    codes = parse_input(input_value)
    if part == 1:
        total = 0
        for code in codes:
            if check_checksum(code["letters"], code["checksum"]):
                total += code["sectorId"]
        return total
    # part 2
    for code in codes:
        decrypted = decrypt(code["letters"], code["sectorId"])
        if "north" in decrypted:
            return code["sectorId"]
    return part


YEAR = 2016
DAY = 4
input_format = {
    1: "text",
    2: "text",
}

funcs = {
    1: solve,
    2: solve,
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    aoc = AdventOfCode(
        year=YEAR,
        day=DAY,
        input_formats=input_format,
        funcs=funcs,
        test_mode=args.test,
    )
    aoc.run(submit=args.submit)
