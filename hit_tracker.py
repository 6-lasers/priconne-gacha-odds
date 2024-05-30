#!/usr/bin/env python
######################################################
#
#    hit_tracker.py
#
#  <description>
#
#  Usage: hit_tracker.py <args>
#
######################################################

from __future__ import print_function

import sys
import argparse
import time
import json

def dump_message(f, mydict, ot_dict, day):
    idx_strs = [
        "3 hits left:",
        "2 hits left:",
        "1 hit left:",
        "0 hits left:"
    ]
    f.write(f"# Day {day} logs:\n\n")
    for i in range(3, -1, -1):
        if len(mydict[i]):
            f.write(f"{idx_strs[i]}\n")
            for idx,name in enumerate(mydict[i]):
                ot_str = f" ({ot_dict[name]} OT left)" if ot_dict[name] > 0 else ""
                f.write(f"{idx+1}. {name} {ot_str}\n")
            f.write("\n")
    if len(mydict['excused']):
        f.write("Excused:\n")
        for idx,name in enumerate(mydict['excused']):
            f.write(f"{idx+1}. {name}\n")
    f.write(f"Last updated: <t:{int(time.time())}:R>\n")

def print_csv(timedict):
    for name in timedict:
        if timedict[name]:
            print(f"{name},{','.join(timedict[name])}")

def main(argv=None):
    parser = argparse.ArgumentParser(description="template")
    parser.add_argument("arg", help="help message")
    parser.add_argument("-c", "--config", default="clan_config.json", help="help message")
    parser.add_argument("-f", "--file", help="help message")
    parser.add_argument("-d", "--day", type=int, help="help message")
    parser.add_argument("-t", "--timedump", action="store_true", help="help message")
    
    args = parser.parse_args()
    
    with open(args.config, "r", encoding="utf-8") as f:
        clanconfig = json.load(f)
        mapping = clanconfig['mapping']
        player_list = clanconfig['player_list']

    #print args.arg
    #if args.name:
    #    print args.name
    with open(args.arg, "r") as f:
        lines = f.readlines()

    tmpdict = dict.fromkeys(player_list, 0)
    ot_dict = dict.fromkeys(player_list, 0)
    timedict = {name: [] for name in player_list}

    mydict = {
        0: [],
        1: [],
        2: [],
        3: [],
        'excused': []
    }
    for line in lines:
        if line.startswith("excused"):
            splitline = line.split()
            player = splitline[1]
            reason = splitline[2]
            tmpdict[mapping[player] if player in mapping else player.capitalize()] = "excused"
        elif line.startswith("mia"):
            splitline = line.split()
            player = splitline[1]
            del tmpdict[mapping[player] if player in mapping else player.capitalize()]
        else:
            line_s = line.split()
            name = mapping[line_s[0]] if line_s[0] in mapping else line_s[0].capitalize()
            tmpdict[name] += 1
            if len(line_s) > 1:
                # timestamp
                timedict[name].append(line_s[-1])
            if len(line_s) == 3:
                if line_s[1] == "b":
                    ot_dict[name] += 1
                else:
                    ot_dict[name] -= 1
                
    for item in tmpdict:
        if isinstance(tmpdict[item], int) and tmpdict[item] > 3:
            print(f"ERROR: {item} = {tmpdict[item]}")
        else:
            mydict[tmpdict[item]].append(item)
        """
        splitline = line.split()
        #if splitline[0] not in mydict:
        #    mydict[splitline[0]] = 0
        idx = len(splitline[1]) if len(splitline) > 1 else 0
        mydict[idx].append(splitline[0])
        """

    if args.file:
        f = open(args.file, "w", encoding="utf-8")
    else:
        f = sys.stdout
    dump_message(f, mydict, ot_dict, args.day)

    if args.timedump:
        print_csv(timedict)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

