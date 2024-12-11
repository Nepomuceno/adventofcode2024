import math
import re

def solve(input: str, second: bool):
    if second:
        return solve_second(input)
    result = 0
    matches = re.findall(r"mul\([0-9]+,[0-9]+\)", input)
    for m in matches:
        a = int(m[4:-1].split(',')[0])
        b = int(m[4:-1].split(',')[1])
        result += a*b
    return result


def solve_second(input: str):
    result = 0
    matches = re.findall(r"(mul\([0-9]+,[0-9]+\)|do\(\)|don't\(\))", input)
    enabled = True
    for m in matches:
        if m == "do()":
            enabled = True
            continue
        if m == "don't()":
            enabled = False
            continue
        if not enabled:
            continue
        a = int(m[4:-1].split(',')[0])
        b = int(m[4:-1].split(',')[1])
        result += a*b
    return result
