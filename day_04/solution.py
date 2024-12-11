import math
import re


def solve(input: str, second: bool):
    if second:
        return solve_second(input)
    result = 0
    grid = [[a for a in line] for line in input.splitlines()]
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == "X":
                result += number_of_words(grid, i, j)
    return result


def number_of_words(grid, s_i, s_j):
    result = 0
    word = "XMAS"
    max_i = len(grid)
    max_j = len(grid[0])
    directions = {
        "S": (1, 0),
        "N": (-1, 0),
        "E": (0, 1),
        "W": (0, -1),
        "SW": (1, -1),
        "SE": (1, 1),
        "NW": (-1, 1),
        "NE": (-1, -1),
    }
    for d in directions.values():
        l = (d[0] * 3, d[1] * 3)
        if s_i + l[0] < 0 or s_i + l[0] >= max_i:
            continue
        if s_j + l[1] < 0 or s_j + l[1] >= max_j:
            continue
        valid = True
        for i in range(1, 4):
            valid = valid and grid[s_i + (d[0] * i)][s_j + (d[1] * i)] == word[i]
        result += 1 if valid else 0
    return result


def number_of_x_mas(grid, i, j):
    max_i = len(grid)
    max_j = len(grid[0])
    if not (i > 0 and j > 0 and i < (max_i - 1) and j < (max_j - 1)):
        return 0
    if (
        grid[i - 1][j - 1] == grid[i + 1][i + 1]
        or grid[i - 1][i + 1] == grid[i + 1][i - 1]
    ):
        return 0
    positions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    words = [
        "MMSS",
        "SMMS",
        "SSMM",
        "MSSM",
    ]
    for word in words:
        valid = True
        for i in range(len(positions)):
            valid = valid and grid[i + positions[i][0]][j + positions[i][1]] == word[i]
        if valid:
            return 1
    return 0


def solve_second(input: str):
    count = 0
    grid = [[a for a in line] for line in input.splitlines()]
    valid_words = ["MMSS", "SMSM", "SSMM", "MSMS"]
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[0]) - 1):
            if grid[i][j] != "A":
                continue
            d = [(1, -1), (1, 1), (-1, -1), (-1, 1)]
            word = ""
            for a, b in d:
                word += grid[i + a][j + b]

            # print the word
            print(f"Is {word} a valid word?")
            print(word[0], " ", word[1])
            print(" ", "A", " ")
            print(word[2], " ", word[3])
            
            if word in valid_words:
                count += 1
    return count
