import math
import re
import time
import copy

def pritn_map(guard_map, guard, loops = []):
    for y in range(len(guard_map)):
        for x in range(len(guard_map[0])):
            if guard and guard[0] == x and guard[1] == y:
                print("\033[91m" + guard[2] + "\033[0m", end="")
                continue
            if [x, y] in loops:
                print("\033[95mO\033[0m", end="")
                continue
            if guard_map[y][x]['obstacle']:
                print("\033[97m#\033[0m", end="")  # White color for obstacles
                continue
            if guard_map[y][x]['visited_positions']:
                print("\033[92m*\033[0m", end="")
                continue
            print("\033[90m.\033[0m", end="")  # Light grey color for non-obstacles
        print()



def solve(input: str, second: bool):
    if second:
        return solve_second(input)
    result = 0
    positions = ">v<^"
    guard_map = []
    guard = None
    for y, line in enumerate(input.splitlines()):
        row = []
        for x, char in enumerate(line):
            cell = {
                'obstacle': char == '#',
                'visited_positions': {},
            }
            if char in positions:
                guard = [x, y, char]
            row.append(cell)
        guard_map.append(row)
    pritn_map(guard_map, guard)
    time.sleep(0.01)
    is_done = False
    count = 0
    while not is_done:
        count += 1
        [is_done, _] = tick(guard_map, guard)
        # clear the screen
        print("\033[H\033[J")
        if count % 20 == 0:
            pritn_map(guard_map, guard)
            time.sleep(0.1)
    # count the visited positions
    pritn_map(guard_map, guard)
    for y in guard_map:
        for x in y:
            if x['visited_positions']:
                result += 1
    return result

def tick(guard_map, guard):
    if guard is None:
        return True, False
    
    # check if the guard is in a visited position
    if guard_map[guard[1]][guard[0]]['visited_positions'].get(guard[2], False):
        return True, True

    # add the current guard position to visited positions
    guard_map[guard[1]][guard[0]]['visited_positions'][guard[2]] = True
    
    # check if the guard moving forward will leave the map if does stop and return
    match guard[2]:
        case '>':
            if guard[0] + 1 >= len(guard_map[0]):
                return True, False
        case '<':
            if guard[0] - 1 < 0:
                return True, False
        case '^':
            if guard[1] - 1 < 0:
                return True, False
        case 'v':
            if guard[1] + 1 >= len(guard_map):
                return True, False
            
    # check if the guard moving forward will hit an obstacle if does turn 90 degrees to the right and continue
    match guard[2]:
        case '>':
            if guard_map[guard[1]][guard[0] + 1]['obstacle']:
                guard[2] = 'v'
                return False, False
        case '<':
            if guard_map[guard[1]][guard[0] - 1]['obstacle']:
                guard[2] = '^'
                return False, False
        case '^':
            if guard_map[guard[1] - 1][guard[0]]['obstacle']:
                guard[2] = '>'
                return False, False
        case 'v':
            if guard_map[guard[1] + 1][guard[0]]['obstacle']:
                guard[2] = '<'
                return False, False
    # if none of that is true move the guard forward
    match guard[2]:
        case '>':
            guard[0] += 1
        case '<':
            guard[0] -= 1
        case '^':
            guard[1] -= 1
        case 'v':
            guard[1] += 1
    return False, False

def solve_second(input: str):
    positions = ">v<^"
    guard_map = []
    guard = None
    loops = []
    result = 0
    for y, line in enumerate(input.splitlines()):
        row = []
        for x, char in enumerate(line):
            cell = {
                'obstacle': char == '#',
                'visited_positions': {},
            }
            if char in positions:
                guard = [x, y, char]
            row.append(cell)
        guard_map.append(row)
    # trying to add a obstacle in every position to check which one does cause a cycle
    new_map = copy.deepcopy(guard_map)
    if guard is None:
        return 0
    initail_guard = guard.copy()
    is_done = False
    while not is_done:
        [is_done, _] = tick(new_map, initail_guard)
    initial_visited = []
    for y in range(len(new_map)):
        for x in range(len(new_map[0])):
            if new_map[y][x]['visited_positions']:
                initial_visited.append([x, y])
    start = time.time()
    initail_guard = guard.copy()
    for y in range(len(guard_map)):
        for x in range(len(guard_map[0])):
            is_done = False
            is_loop = False
            if guard_map[y][x]['obstacle']:
                continue
            if not [x, y] in initial_visited:
                continue
            new_map = copy.deepcopy(guard_map)
            new_map[y][x]['obstacle'] = True
            guard = initail_guard.copy()
            [is_done, is_loop] = tick(new_map, guard)
            count = 0
            while not is_done:
                count += 1
                [is_done, is_loop] = tick(new_map, guard)
                if count > len(new_map) * len(new_map[0]):
                    raise Exception("Infinite loop not detected")
            if ((len(guard_map[0]) * y)+ x) % 100 == 0:
                progress = (len(guard_map[0]) * y) + x
                total = len(guard_map) * len(guard_map[0])
                elapsed_time = time.time() - start
                estimated_total_time = (elapsed_time / progress) * total if progress > 0 else 0
                estimated_remaining_time = estimated_total_time - elapsed_time
                estimated_completion_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + estimated_remaining_time))
                print(f"[{progress}/{total}] Loops: {len(loops)}, Elapsed: {elapsed_time:.2f}s, Est. Total: {estimated_total_time:.2f}s, Est. Completion: {estimated_completion_time}")
            if is_loop:
                # print("--------------------")
                # pritn_map(new_map, guard, loops)
                # print()
                result += 1
                loops.append([x, y])
    guard = initail_guard
    print(f"Result: {result}")
    print(f"Loops: {loops}")
    print(f"Guard: {guard}")
    pritn_map(guard_map, guard, loops)
    print(f"Map size: {len(guard_map)}x{len(guard_map[0])} total: {len(guard_map) * len(guard_map[0])}")
    return result
