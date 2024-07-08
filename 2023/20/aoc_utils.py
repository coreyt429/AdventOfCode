# https://adventofcode.com/2023/day/20
from __future__ import annotations
from typing import Iterable, Any, Final, NamedTuple, Callable
import itertools_recipes as ir
from dataclasses import dataclass, field
from collections import deque
from pprint import pprint


test_input = """
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""

test_input_2 = """
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""

HIGH_PULSE: Final = True
LOW_PULSE: Final = False


class Signal(NamedTuple):
    sender: str
    receptor: str
    pulse: bool


@dataclass
class Module:
    name: str
    connected: list[Any]


@dataclass
class Broadcaster(Module):

    def __call__(self, pulse: bool = LOW_PULSE):
        return [Signal(self.name, m, pulse) for m in self.connected]


@dataclass
class FlipFlop(Module):
    state: bool = False

    def __call__(self, data: Signal) -> list[Signal]:
        assert data.receptor == self.name
        if data.pulse:
            return []
        old_state = self.state
        self.state = not old_state
        to_send = LOW_PULSE if old_state else HIGH_PULSE
        return [Signal(self.name, m, to_send) for m in self.connected]


@dataclass
class Conjunction(Module):
    memory: dict[str, bool] = field(default_factory=dict)

    def __call__(self, data: Signal) -> list[Signal]:
        assert data.receptor == self.name
        self.memory[data.sender] = data.pulse
        to_send = LOW_PULSE if all(self.memory.values()) else HIGH_PULSE
        return [Signal(self.name, m, to_send) for m in self.connected]


@dataclass
class MODError:

    def __call__(self, data: Signal) -> list[Signal]:
        return []


class PulsePropagation:

    def __init__(self, instructions: Iterable[list[str]]):
        modules = {}
        for ins in instructions:
            name: str
            name, *con = ins
            if name.startswith("%"):
                name = name[1:]
                modules[name] = FlipFlop(name, con)
            elif name.startswith("&"):
                name = name[1:]
                modules[name] = Conjunction(name, con)
            elif name == "broadcaster":
                modules[name] = Broadcaster(name, con)
            else:
                raise ValueError(f"invalid instruction {ins!r}")
        # update memories
        for mod in modules.values():
            for c in mod.connected:
                if isinstance(con := modules.get(c), Conjunction):
                    con.memory[mod.name] = False
        self.modules = modules

    def __call__(self, pulse: bool = LOW_PULSE, show: bool = False, output: Callable[[Signal], list[Signal]] = None, callback: Callable[[Signal], None] = None) -> tuple[int, int]:
        stack = deque(self.modules["broadcaster"](pulse))
        low = pulse == LOW_PULSE
        high = pulse == HIGH_PULSE
        output = output if output else MODError()
        if show:
            print("initial state")
            pprint(self.modules)
        while stack:
            s = stack.popleft()
            if callback:
                callback(s)
            if s.pulse:
                high += 1
            else:
                low += 1
            stack.extend(self.modules.get(s.receptor, output)(s))
        if show:
            print("final state")
            pprint(self.modules)
            print(f"result: {high=} {low=}")
        return high, low


def process_data(data: str) -> PulsePropagation:
    """transform the raw data into a processable form"""
    return PulsePropagation(line.replace("->", " ").replace(",", " ").split() for line in ir.interesting_lines(data))


def get_raw_data(path: str = "./input.txt") -> str:
    with open(path) as file:
        return file.read()