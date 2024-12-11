import math

def solve(input: str, second: bool):
    if second:
        return solve_second(input)
    result = 0
    reports = [[int(x) for x in line.split(" ")] for line in input.splitlines()]
    for report in reports:
        valid = True
        valid = is_safe_report(report)
        result += 1 if valid else 0
    return result

def is_safe_report(report):
    valid = True
    ascending_status = 'U'
    for i in range(len(report)-1):
        change = report[i] - report[i+1]
        if abs(change) > 3 or abs(change) == 0:
            valid = False
            break
        if ascending_status == 'P' and change < 0:
            valid = False
            break
        elif ascending_status == 'N' and change > 0:
            valid = False
            break
        elif change > 0:
            ascending_status = 'P'
        else :
            ascending_status = 'N'
    if valid:
        print(report)
    return valid

def solve_second(input: str):
    reports = [[int(x) for x in line.split(" ")] for line in input.splitlines()]
    result = 0
    for report in reports:
        valid = is_safe_report(report)
        if not valid:
            for i in range(len(report)):
                temp_rep = report[0:i] + report [i+1:]
                valid = is_safe_report(temp_rep)
                if valid:
                    break
        result += 1 if valid else 0
    return result
