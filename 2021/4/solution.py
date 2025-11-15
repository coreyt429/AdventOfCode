"""
Advent Of Code 2021 day 4

I read this one last night, and didn't start coding it until this morning.
My initial thought last night was to make this one object oriented, and that strategy
paid off.

The only thing that tripped me up on this one was a poorly placed "break" that was
causing an incorrect answer in part 2

"""

# import system modules
import time
from colorama import Fore

# import my modules
import aoc  # pylint: disable=import-error


class Bingo:
    """Class to represent Bingo game"""

    def __init__(self, game_data):
        """Init Method"""
        number_text, *cards_text_list = game_data.split("\n\n")
        self.numbers = [int(num) for num in number_text.split(",")]
        self.cards = self.build_cards(cards_text_list)

    def build_cards(self, cards_text_list):
        """Method to load cards from input data"""
        cards = []
        for card_text in cards_text_list:
            cards.append(BingoCard(card_text))
        return cards

    def play(self, mode=1):
        """Method to play the game"""
        for number in self.numbers:
            for _, card in enumerate(self.cards):
                card.mark(number)
                if card.winner:
                    if mode == 1:
                        return card.score
        last_score = 0
        for number in self.numbers[::-1]:
            for card in self.cards:
                if card.last_called == number:
                    last_score = card.score
                    break
            if last_score > 0:
                break
        return last_score


class BingoCard:
    """Class to represent a bingo card"""

    def __init__(self, numbers):
        """Init Method"""
        self.numbers = self.parse_numbers(numbers)
        self.marked = set()
        self.winner = False
        self.last_called = None
        self.score = 0

    def parse_numbers(self, text):
        """Method to parse text input"""
        numbers = []
        for line in text.splitlines():
            numbers.append([int(num) for num in line.split(" ") if num.isdigit()])
        return numbers

    def check(self):
        """Method to check a card for wins"""
        for row in self.numbers:
            win = True
            for number in row:
                if number not in self.marked:
                    win = False
            if win:
                if not self.winner:
                    self.calc_score()
                self.winner = True
        for col, _ in enumerate(self.numbers[0]):
            win = True
            for row, _ in enumerate(self.numbers):
                if self.numbers[row][col] not in self.marked:
                    win = False
            if win:
                if not self.winner:
                    self.calc_score()
                self.winner = True

    def mark(self, number):
        """Method to mark a number"""
        # stop marking if we already won
        if self.winner:
            return
        self.last_called = number
        for row in self.numbers:
            for num in row:
                if num == number:
                    self.marked.add(number)
        self.check()
        return

    def calc_score(self):
        """Method to calculate card score"""
        # The score of the winning board can now be calculated.
        # Start by finding the sum of all unmarked numbers on that board;
        # in this case, the sum is 188.
        total = 0
        for row in self.numbers:
            for num in row:
                if num not in self.marked:
                    total += num
        # Then, multiply that sum by the number that was just called when the board won
        # 24, to get the final score, 188 * 24 = 4512
        self.score = total * self.last_called

    def __str__(self):
        """String Method for debugging"""
        my_str = ""
        for row in self.numbers:
            for num in row:
                if num in self.marked:
                    my_str += f"{Fore.GREEN}{num:2}{Fore.RESET} "
                else:
                    my_str += f"{num:2} "
            my_str.rstrip()
            my_str += "\n"
        if self.winner:
            my_str += f"\nWinner! {self.score} {self.last_called}\n"
        my_str += "\n"
        return my_str


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    game = Bingo(input_value)
    return game.play(mode=part)


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2021, 4)
    input_data = my_aoc.load_text()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 44088, 2: 23670}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_data, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
