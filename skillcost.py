#!/usr/bin/env python3
######################################################
#
#    skillcost.py
#
#  <description>
#
#  Usage: skillcost.py <args>
#
######################################################

from __future__ import print_function

import sys
import argparse

current_max_level = 280

def calc_cost(level):
    # 54 is an 810 cost jump over 53 (which is 20660).
    # After 54, cost increases linearly by 800 per level
    if level >= 54:
        cost = 21470 + 800 * (level - 54)
    # 12-15 is just flat 360
    # 16-31 increases by 100 each level
    # 32-37 increases by 300/level
    # 38-44 increases by 1000/level
    # 45-53 increases by 1100/level
    elif level > 11:
        cost = 360
        if level > 15:
            cost += 100 * (level - 15)
        if level > 31:
            cost += 200 * (level - 31)
        if level > 37:
            cost += 700 * (level - 37)
        if level > 44:
            cost += 100 * (level - 44)
    # Level 1 costs 0 by definition
    elif level == 1:
        cost = 0
    # Anything else <= 11 is just 240
    else:
        cost = 240
    
    return cost

def calc_xp_cost(level):
    # Level 1 costs 0 by definition
    if level == 1:
        cost = 0
    # Level 2 is 24
    # 3-6 is 48
    # 7-15 is 72
    elif level == 2:
        cost = 24
    elif level <= 6:
        cost = 48
    else:
        cost = 72
        # 16-22 increases by 20/level
        # 23-26 increases by 2/level
        # 27-30 increases by 3/level
        # 31-37 increases by 10/level
        # 38-42 increases by 50/level
        # 43-48 increases by 200/level
        # 49-53 increases by 400/level
        # 54-63 increases by 500/level
        if level > 15:
            cost += min(20 * (level - 15), 140)
        if level > 22:
            cost += 2 * (level - 22)
        if level > 26:
            cost += 1 * (level - 26)
        if level > 30:
            cost += 7 * (level - 30)
        if level > 37:
            cost += 40 * (level - 37)
        if level > 42:
            cost += 150 * (level - 42)
        if level > 48:
            cost += 200 * (level - 48)
        if level > 53:
            cost += 100 * (level - 53)
        # After 63, cost increases linearly by 600 per level
        if level > 63:
            cost += 100 * (level - 63)
    
    return cost

def main(argv=None):
    parser = argparse.ArgumentParser(description="template")
    parser.add_argument("arg", type=int, help="help message")
    parser.add_argument("--xp", action="store_true", help="help message")
    
    args = parser.parse_args()
    
    cb = calc_xp_cost if args.xp else calc_cost
    
    if args.arg == 0:
        # If argument is 0, generate table
        total = 0
        for i in range(2, current_max_level + 1):
            cost = cb(i)
            total += cost
            print(f"{i}|{cost}|{total}")
    else:
        print(cb(int(args.arg)))
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

