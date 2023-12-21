"""Day 20: Pulse Propagation"""
from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
import math
from typing import Iterator, override


class Pulse(Enum):
    """Pulse Enum"""

    LOW = 0
    HIGH = 1


@dataclass
class BaseModule(ABC):
    """Base Module"""

    name: str
    destinations: list[str] = field(default_factory=list)

    @abstractmethod
    def process_pulse(self, input_name: str, pulse: Pulse) -> Pulse | None:
        """Process an input pulse"""

    def reset(self):
        """Resets the fields"""


@dataclass
class FlipFlop(BaseModule):
    """Flip Flop Module"""

    state: bool = False

    @override
    def process_pulse(self, input_name: str, pulse: Pulse) -> Pulse | None:
        if pulse == Pulse.HIGH:
            return None
        self.state = not self.state
        return Pulse.HIGH if self.state else Pulse.LOW

    @override
    def reset(self):
        self.state = False


@dataclass
class Conjunction(BaseModule):
    """Conjunction Module"""

    last_inputs: dict[str, Pulse] = field(default_factory=dict)

    def add_input(self, input_name: str) -> None:
        """Adds an input module with a default low pulse"""
        self.last_inputs[input_name] = Pulse.LOW

    @override
    def process_pulse(self, input_name: str, pulse: Pulse) -> Pulse | None:
        self.last_inputs[input_name] = pulse
        if all(last_pulse == Pulse.HIGH for last_pulse in self.last_inputs.values()):
            return Pulse.LOW
        return Pulse.HIGH

    @override
    def reset(self):
        for input_name in self.last_inputs:
            self.last_inputs[input_name] = Pulse.LOW


class Broadcast(BaseModule):
    """Broadcast Module"""
    @override
    def process_pulse(self, input_name: str, pulse: Pulse) -> Pulse | None:
        return pulse


def get_modules(lines: list[str]) -> dict[str, BaseModule]:
    """Parses the input and returns a dictionary of modules"""
    modules: dict[str, BaseModule] = {}
    for line in lines:
        name, output = line.split(" -> ")
        output_modules = output.split(", ")
        match name[0]:
            case "%":
                module = FlipFlop(name[1:], output_modules)
            case "&":
                module = Conjunction(name[1:], output_modules)
            case _:
                module = Broadcast(name, output_modules)
        modules[module.name] = module

    # Set default input pulses as LOW for conjunctions
    for module_name, module in modules.items():
        for output in module.destinations:
            module = modules.get(output)
            if isinstance(module, Conjunction):
                module.add_input(module_name)
    return modules


def count_pulses(modules: dict[str, BaseModule]) -> dict[Pulse, int]:
    """Returns the pulse count, given the current modules' state"""
    counter = {Pulse.LOW: 0, Pulse.HIGH: 0}
    queue: deque[tuple[str, str, Pulse]] = deque([("button", "broadcaster", Pulse.LOW)])
    while queue:
        input_name, module_name, pulse = queue.pop()
        counter[pulse] += 1
        if module_name in modules:
            new_pulse = modules[module_name].process_pulse(input_name, pulse)
            if new_pulse is not None:
                for output in modules[module_name].destinations:
                    queue.appendleft((module_name, output, new_pulse))
    return counter


def get_counter_ranges(modules: dict[str, BaseModule]) -> Iterator[int]:
    """Part 2"""
    for broadcaster_output in modules["broadcaster"].destinations:
        bits = ""
        flip_flop = modules[broadcaster_output]
        while True:
            if any(
                isinstance(modules[output], Conjunction)
                for output in flip_flop.destinations
            ):
                bits = "1" + bits
            else:
                bits = "0" + bits
            for output in flip_flop.destinations:
                if isinstance(modules[output], FlipFlop):
                    flip_flop = modules[output]
                    break
            else:
                break
        yield int(bits, 2)


def main() -> None:
    """Main Function"""
    with open("input.txt", "r", encoding="utf-8") as f:
        text = f.read()

    lines = text.splitlines()
    modules = get_modules(lines)
    counters = [count_pulses(modules) for _ in range(1000)]

    print(
        "Part 1:",
        sum(counter[Pulse.LOW] for counter in counters)
        * sum(counter[Pulse.HIGH] for counter in counters),
    )
    print("Part 2:", math.lcm(*get_counter_ranges(modules)))


if __name__ == "__main__":
    main()
