import math
import re

def solve(input: str, second: bool):
    if second:
        return solve_second(input)
    result = 0
    lines = input.splitlines()
    not_before = {}
    invalid = 0
    while True:
        line = lines.pop(0)
        if line == "":
            break
        rule = line.split("|")
        if rule[0] in not_before:
            not_before[rule[0]].add(rule[1])
        else:
            not_before[rule[0]] = {rule[1]}
    updates = []
    while len(lines) > 0:
        line = lines.pop(0)
        updates.append(line.split(","))
    for update in updates:
        prev = set()
        for u in update:
            prev.add(u)
            if u in not_before:
                # check for the intersection of not before and prev
                if len(not_before[u] & prev) > 0:
                    invalid += 1
                    break
        else :
            result += int(update[(len(update)//2)])
            print(f"Valid update: {update}")
    return result



def solve_second(input: str):
    result = 0
    lines = input.splitlines()
    not_before = {}
    source = []
    destination = []
    while True:
        line = lines.pop(0)
        if line == "":
            break
        rule = line.split("|")
        source.append(rule[0])
        destination.append(rule[1])
        if rule[0] in not_before:
            not_before[rule[0]].add(rule[1])
        else:
            not_before[rule[0]] = {rule[1]}
    # find the intersection of all that are in detination but not in surce 
    intersection = set(destination) - set(source)
    print(f"Intersection: {intersection}")
    not_before_test = {k: v.copy() for k, v in not_before.items()}
    updates = []
    while len(lines) > 0:
        line = lines.pop(0)
        updates.append(line.split(","))
    for update in updates.copy():
        prev = set()
        valid = True
        for u in update:
            prev.add(u)
            if u in not_before_test:
                # check for the intersection of not before and prev
                if len(not_before_test[u] & prev) > 0:
                    valid = False
                    break 
        if not valid:
            updates_set = set(update)
            local_set = {}
            for u in updates_set:
                if u in not_before_test:
                    local_set[u] = not_before_test[u].copy()
                    
            number_map = number_map_creation(local_set)
            update.sort(key=lambda x: number_map[x] if x in number_map else 0)
            result += int(update[(len(update)//2)])
    return result

def number_map_creation(not_before):
    number_map = {}
    max_number = 100_000_000
    while len(not_before) > 0:
        for key in not_before.copy().keys():
            for value in not_before[key].copy():
                if not value in not_before:
                    number_map[value] = max_number
                    max_number -= 1
                    for k in not_before.keys():
                        not_before[k].discard(value)
            if len(not_before[key]) == 0:
                number_map[key] = max_number
                max_number -= 1
                del not_before[key]
    return number_map
