"""Day 19: Aplenty"""
from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Self


class PartCategory(Enum):
    """Part Category Enum"""

    EXTREMELY = "x"
    MUSICAL = "m"
    AERODYNAMIC = "a"
    SHINY = "s"


class Flow(Enum):
    """Flow Enum"""

    ACCEPTED = "A"
    REJECTED = "R"


NextWorkflow = str | Flow


@dataclass
class Rule:
    """Rule Class"""

    category: PartCategory
    greater_than: bool
    value: int
    next_workflow: NextWorkflow
    special: bool = False

    def match(self, value: int) -> bool:
        """Matches a certain value to a rule"""
        if self.greater_than:
            return value > self.value
        return value < self.value

    @classmethod
    def from_str(cls, string: str) -> Self:
        """Parse string as Rule"""
        category = PartCategory(string[0])
        greater_than = string[1] == ">"
        value, next_workflow = string[2:].split(":")
        value = int(value)
        next_workflow = (
            Flow(next_workflow) if len(next_workflow) == 1 else next_workflow
        )
        return cls(category, greater_than, value, next_workflow)


@dataclass
class PartRange:
    """Part Range Class"""

    x: range
    m: range
    a: range
    s: range

    def get_range(self, category: PartCategory):
        """Takes a category and returns the corresponding range"""
        match category:
            case PartCategory.EXTREMELY:
                return self.x
            case PartCategory.MUSICAL:
                return self.m
            case PartCategory.AERODYNAMIC:
                return self.a
            case PartCategory.SHINY:
                return self.s

    def replace(self, category: PartCategory, r: range) -> None:
        """Takes a category and a range and replaces the corresponding range"""
        match category:
            case PartCategory.EXTREMELY:
                self.x = r
            case PartCategory.MUSICAL:
                self.m = r
            case PartCategory.AERODYNAMIC:
                self.a = r
            case PartCategory.SHINY:
                self.s = r

    def permutations(self) -> int:
        """Total number of permutations"""
        return len(self.x) * len(self.m) * len(self.a) * len(self.s)


@dataclass
class Worflow:
    """Workflow Class"""

    name: str
    rules: list[Rule]
    next_workflow: NextWorkflow

    @classmethod
    def from_str(cls, string: str) -> Self:
        """Parse string as Workflow"""
        name, rules = string.split("{")
        rules = rules[:-1].split(",")
        last_rule = rules[-1]
        rules = list(map(Rule.from_str, rules[:-1]))
        next_workflow = Flow(last_rule) if len(last_rule) == 1 else last_rule
        return cls(name, rules, next_workflow)

    def analyze_part_range(self, pr: PartRange) -> list[tuple[NextWorkflow, PartRange]]:
        """Analyze a workflow for a given part range"""
        splits: list[tuple[NextWorkflow, PartRange]] = []
        for rule in self.rules:
            cat_range = pr.get_range(rule.category)
            if rule.greater_than:
                if len(range(rule.value, cat_range.stop)) == 0:
                    continue
                new_range = PartRange(pr.x, pr.m, pr.a, pr.s)
                new_range.replace(rule.category, range(rule.value + 1, cat_range.stop))
                splits.append((rule.next_workflow, new_range))
                pr.replace(rule.category, range(cat_range.start, rule.value + 1))
            else:
                if len(range(cat_range.start, rule.value)) == 0:  # If an overlap exists
                    continue
                new_range = PartRange(pr.x, pr.m, pr.a, pr.s)
                new_range.replace(rule.category, range(cat_range.start, rule.value))
                splits.append((rule.next_workflow, new_range))
                pr.replace(rule.category, range(rule.value, cat_range.stop))
        splits.append((self.next_workflow, pr))
        return splits


def parse_workflows(workflows: list[str]) -> dict[str, Worflow]:
    """Parse workflows"""
    workflow_dict: dict[str, Worflow] = {}
    for workflow in workflows:
        workflow = Worflow.from_str(workflow)
        workflow_dict[workflow.name] = workflow
    return workflow_dict


Rating = dict[PartCategory, int]


def parse_ratings(ratings: list[str]) -> list[Rating]:
    """Parse ratings"""

    def parse_rating(string: str) -> Rating:
        parts = string[1:-1].split(",")
        parts = [part.split("=") for part in parts]
        return {PartCategory(k): int(v) for (k, v) in parts}

    return list(map(parse_rating, ratings))


def part1(workflows: dict[str, Worflow], rating: Rating) -> int:
    """Part 1"""
    curr_wf_name = "in"
    while True:
        curr_wf = workflows[curr_wf_name]
        for rule in curr_wf.rules:
            part = rating[rule.category]
            if not rule.match(part):
                continue
            match rule.next_workflow:
                case Flow.ACCEPTED:
                    return sum(rating.values())
                case Flow.REJECTED:
                    return 0
                case next_wf_name:
                    curr_wf_name = next_wf_name
                    break
        else:
            match curr_wf.next_workflow:
                case Flow.ACCEPTED:
                    return sum(rating.values())
                case Flow.REJECTED:
                    return 0
                case next_wf_name:
                    curr_wf_name = next_wf_name


def part2(workflows: dict[str, Worflow]) -> int:
    """Part 2"""
    accepted_ranges: list[PartRange] = []
    start_range = PartRange(
        range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001)
    )
    # Queue will keep track of PartRanges we need to send through more workflows
    range_queue: deque[tuple[str, PartRange]] = deque([("in", start_range)])
    while range_queue:
        test_wf_name, test_range = range_queue.pop()
        range_splits = workflows[test_wf_name].analyze_part_range(test_range)
        for next_wf, pr in range_splits:
            match next_wf:
                case Flow.ACCEPTED:
                    accepted_ranges.append(pr)
                case Flow.REJECTED:
                    continue
                case _:
                    range_queue.append((next_wf, pr))
    total_possibilities = sum(map(PartRange.permutations, accepted_ranges))
    return total_possibilities


def main() -> None:
    """Main function"""
    with open("input.txt", "r", encoding="utf-8") as file:
        workflows, ratings = file.read().split("\n\n")

    workflows = parse_workflows(workflows.splitlines())
    ratings = parse_ratings(ratings.splitlines())

    part1_sum = sum(part1(workflows, rating) for rating in ratings)
    print(f"Part 1: {part1_sum}")

    part2_sum = part2(workflows)
    print(f"Part 2: {part2_sum}")


if __name__ == "__main__":
    main()
