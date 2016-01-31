#!/usr/bin/python

import re, os
from classes.player import Player

# reading player file
f = open("eden.html", "r")
big_data = f.read()
f.close()

# creating regex for finding required table with stats
regex = r"<table class=('|\")player-stats('|\")>\s*<tbody>(.|\n)*?</tbody>"
regex = re.compile(regex)
regex = regex.search(big_data)
data = regex.group()


# we also strip away the part with player overall and add it into our data
regex = r"\s*(<h1 class=(\"|')top-header(\"|')><span class=(\"|')ovr [a-zA-Z]*(\"|')>([0-9]*)</span>)\s*"
data += re.search(regex, big_data).group(1)


# stats that are needed
stats = [
    "Attacking Prowess", "Dribbling", "Low Pass", "Lofted Pass", "Finishing", "Place Kicking", "Header", 
    "Defensive Prowess", "Ball Winning", "Kicking Power", "Speed", "Explosive Power", "Body Balance", "Jump"
]

def generate_regex_for_stats(stat_name):
    regex = r"<tr>\s*"
    regex += r"<td><span class=\"[A-Za-z ]*?\">([0-9]*)</span></td></td>\s*"    ## backreference to stat value
    regex += r"<td>(" + stat_name + r")\s*</tr>"                                   ## backreference to stat name 
    return regex

def generate_regex_for_overall():
    regex = r"\s*<h1 class=(\"|')top-header(\"|')><span class=(\"|')ovr [a-zA-Z]*(\"|')>([0-9]*)</span>\s*" 
    return regex

def get_player_object(data, stats):
    dragon_stats = {}
    for stat in stats:
        print stat
        dragon_stats[stat] = re.search(generate_regex_for_stats(stat), data).group(1) 
    overall = re.search(generate_regex_for_overall(), data).group(5)
    return Player("Eden", "Hazard", dragon_stats, overall)

print str(get_player_object(data, stats))
