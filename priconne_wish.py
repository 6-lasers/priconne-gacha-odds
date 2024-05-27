#!/usr/bin/env python3
######################################################
#
#    priconne_wish.py
#
#  Simulator for pulls in Priconne
#
#  Usage: priconne_wish.py [-h] [-c <number>] [-d] [-nc] <banner name>
#
######################################################

from __future__ import print_function

import sys
import argparse
import random
import json

# Loading raw banner and pool data from JSON
with open("event_banners.json", "r") as f:
    event_wish_list = json.load(f)
with open("std_pools.json", "r") as f:
    pools = json.load(f)
    std_1_star_pool = pools['1_star_pool']
    std_2_star_pool = pools['2_star_pool']
    std_3_star_pool = pools['std_3_star_pool']

# Official odds published in-game

base_odds = {
    'standard': {
        '1': 0.795,
        '2': 0.18,
        '3': 0.025
    },
    # Featured rates
    'featured': {
        '1': 0.0,
        '2': 0.03,
        '3': 0.007
    }
}

# Pick pools in order of priority
def pick_pool(banner_type, _10pull_guarantee, debug=False):
    # TODO
    game_type = "standard"
    
    random_val = random.random()
    
    if debug:
        print("Pulling {0}".format(banner_type))
    # Test 3*
    odds = base_odds[game_type]['3']
    if random_val < odds:
        # 3* selected, check for featured items
        if banner_type == "event" and random_val < base_odds['featured']['3']:
            return '3feat'
        else:
            return '3'
    
    # Test 2*, also check for guarantee if 10-pulling.
    # Yes, this does mean that the featured 2* odds do
    # not change on the 10th pull
    random_val -= odds
    odds = base_odds[game_type]['2']
    if random_val < odds or _10pull_guarantee:
        if banner_type == "event" and random_val < base_odds['featured']['2']:
            return '2feat'
        else:
            return '2'
    
    return '1'

class bannerState:
    pull_type = ""
    banner = {}
    do_pull = None
    debug = False
    _10pull_count = 0
    
    # Standard pull with no featured items
    def do_standard_pull(self):
        # If pull_type is True then we're pulling singles
        # and _10pull_count stays at 0
        if not self.pull_type:
            if self._10pull_count == 10:
                self._10pull_count = 1
            else:
                self._10pull_count += 1
        pool = pick_pool("standard", self._10pull_count == 10, self.debug)
        item = random.choice(self.banner['drops'][pool])
        
        return pool,item
    
    # Event pulls with featured items
    def do_event_pull(self):
        # If pull_type is True then we're pulling singles
        # and _10pull_count stays at 0
        if not self.pull_type:
            if self._10pull_count == 10:
                self._10pull_count = 1
            else:
                self._10pull_count += 1
        pool = pick_pool("event", self._10pull_count == 10, self.debug)
        
        featured = False
        if pool[1:5] == "feat":
            featured = True
            pool = pool[0] 
        
        if featured and 'featured' in self.banner['drops'][pool]:
            item = random.choice(self.banner['drops'][pool]['featured'])
        else:
            item = random.choice(self.banner['drops'][pool]['other'])
        
        return pool,item
    
    def __init__(self, banner, pull_type, game_type, debug=False):
        self.pull_type = pull_type
        self.debug = debug
        
        # Initialize banner type
        if banner == "standard":
            self.banner = banners[banner]
            self.do_pull = self.do_standard_pull
        else:
            self.do_pull = self.do_event_pull
            
            self.banner = banners['event']
            # Distinguish featured items
            for pool in ['1', '2', '3']:
                if pool in event_wish_list[banner]:
                    self.banner['drops'][pool]['featured'] = event_wish_list[banner][pool]
                    # Remove featured items from 'other' category
                    self.banner['drops'][pool]['other'] = [item for item in self.banner['drops'][pool]['other'] if item not in event_wish_list[banner][pool]]
            
            if self.debug:
                print("Banner: " + banner)
                print(json.dumps(self.banner, sys.stdout, indent=4))


# Base loadouts for banner types.
# Not JSON so we can use higher level logic
banners = {
    'standard': {
        'drops':
        {
            '1': std_1_star_pool,
            '2': std_2_star_pool,
            '3': std_3_star_pool
        }
    },
    'event': {
        'drops':
        {
            '1': {
                'other': std_1_star_pool
            },
            '2': {
                'other': std_2_star_pool
            },
            '3': {
                'other': std_3_star_pool
            }
        }
    }
}

# No color for 1*
# ASCII yellow for 2*
# ASCII magenta for 3*
pool_color = {
    '1': "",
    '2': '\033[33m',
    '3': '\033[35m'
}

def main(argv=None):
    parser = argparse.ArgumentParser(description="Simulator for pulls in Princess Connect Re:Dive")
    parser.add_argument("banner", metavar="<banner name>", help="Name of the banner to simulate. Use \"list\" to list banner names.")
    parser.add_argument("-c", "--count", metavar="<number>", type=int, default=1, help="Number of pulls to simulate")
    parser.add_argument("-s", "--single", action="store_true", help="Pull singles instead of 10-pulls")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable verbose output")
    parser.add_argument("-nc", "--nocolor", action="store_true", help="Remove ASCII color codes from output")
    
    args = parser.parse_args()
    
    if args.banner == "list":
        print("\n".join(["standard"] + event_wish_list.keys()))
        return 0
    
    tracking = {
        '1': 0,
        '2': 0,
        '3': 0
    }
    _3star_list = []
    
    myBanner = bannerState(args.banner, args.single, args.ba, args.debug)
    for i in range(args.count):
        result = myBanner.do_pull()
        
        # Accounting
        tracking[result[0]] += 1
        if result[0] == '3':
            _3star_list.append(result[1])
        
        if args.nocolor:
            print(result[1])
        else:
            print(pool_color[result[0]] + result[1] + "\033[0m")
    
    for i in range(1,4):
        print(f"{i}*: {tracking[str(i)]}")
    
    da_total = tracking['1'] + 10 * tracking['2'] + 50 * tracking ['3']
    print(f"DA total: {da_total}")
    
    if _3star_list:
        print(f"3* character list:")
        print("  " + "\n  ".join(_3star_list))
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

