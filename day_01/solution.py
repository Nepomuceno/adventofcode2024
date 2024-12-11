import math

def solve(input: str, second: bool):
    if second:
        return solve_second(input)

    list_a = [int(line.split("   ")[0]) for line in input.splitlines()]
    list_b = [int(line.split("   ")[1]) for line in input.splitlines()]
    list_a.sort()
    list_b.sort()
    total = 0
    for a,b in zip(list_a,list_b):
        total += abs(a-b)
    return total


def solve_second(input: str):
    list_a = [int(line.split("   ")[0]) for line in input.splitlines()]
    list_b = [int(line.split("   ")[1]) for line in input.splitlines()]
    set_b = {}
    for n in list_b:
        if n in set_b:
            set_b[n] += 1
        else:
            set_b[n] = 1
    total = 0
    for n in list_a:
        if n in set_b:
            total += n * set_b[n]
    return total
