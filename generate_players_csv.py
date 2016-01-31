#!/usr/bin/python

import re, os, sys, csv
from classes.player import Player

# takes the huge html file of players and strips away unneeded thingies
def compress_data(big_data):
    # creating regex for finding required table with stats
    regex = r"<table class=('|\")player-stats('|\")>\s*<tbody>(.|\n)*?</tbody>"
    regex = re.compile(regex)
    regex = regex.search(big_data)
    data = regex.group()

    # we also strip away the part with player overall and add it into our data
    regex = r"\s*(<h1 class=(\"|')top-header(\"|')><span class=(\"|')ovr [a-zA-Z]*(\"|')>([0-9]*)</span>)\s*"
    data += re.search(regex, big_data).group(1)
    return data

# big_data = compress_data(big_data)


# stats we have for our players
stats = [
    "Attacking Prowess", "Dribbling", "Low Pass", "Lofted Pass", "Finishing", "Place Kicking", "Header", 
    "Defensive Prowess", "Ball Winning", "Kicking Power", "Speed", "Explosive Power", "Body Balance", "Jump"
]

# Returns v1 for player_stat regex
# @return str
def generate_regex_for_stats1(stat_name):
    regex = r"<tr>\s*"
    regex += r"<td><span class=\"[A-Za-z ]*?\">([0-9]*)</span></td></td>\s*"            ## backreference to stat value
    regex += r"<td>(" + stat_name + r")\s*</tr>"                                        ## backreference to stat name 
    return regex

# Returns v2 for player_stat regex
# @return str
def generate_regex_for_stats2(stat_name):
    regex = r"<tr>\s*"
    regex += r"<td><span class=\"[A-Za-z ]*?\">([0-9]*)</span></td>\s*"                 ## backreference to stat value
    regex += r"<td>(" + stat_name + r")\s*</td></tr>"                                   ## backreference to stat name 
    return regex

# @return str
def generate_regex_for_overall():
    regex = r"\s*<h1 class=(\"|')top-header(\"|')><span class=(\"|')ovr [a-zA-Z]*(\"|')>([0-9]*)</span>\s*" 
    return regex

# @returns Player
def get_player_object(data, stats, name, surname):
    dragon_stats = {}
    for stat in stats:
        res = re.search(generate_regex_for_stats1(stat), data) 
        if res == None:
            res = re.search(generate_regex_for_stats2(stat), data)
        print "Working with: " + str(stat)
        dragon_stats[stat] = res.group(1)
    overall = re.search(generate_regex_for_overall(), data).group(5)
    return Player(name, surname, dragon_stats, overall)

# Returns [name, surname]
def get_player_name_from_file_name(path): 
    player_file_name = os.path.basename(player_file)                # gets only the name of opened .html file
    player_file_name = os.path.splitext(player_file_name)[0]        # gets us only the name and surname of player, separated by <SPACE>
    player_file_name = str(player_file_name).split(' ')
    return player_file_name

path = "teams"

# Creating output csv file for all present players
try:
    output_stats = open("players_stats.csv", "wt")
    output_general = open("players.csv", "wt")
except IOError:
    print "Failed creating csv files at current dir."
    sys.exit()

header = list(stats)
header.insert(0, 'player_id')
header.append('overall')

# Creating header 
writer_stats = csv.writer(output_stats)
writer_general = csv.writer(output_general)
writer_general.writerow(('team_id', 'player_id', 'name', 'surname', 'position', 'date_of_birth'))
writer_stats.writerow(tuple(header))

i = 1                           # used for player id
j = 1                           # used for team id
for currDir, dirs, files in os.walk(path):
    for f in files:
        player_file_name = ""
        if f.endswith(".html"):
            player_file = os.path.realpath(os.path.join(currDir,f))
            try:
                print "working with:\n" + player_file
                player_file_name = get_player_name_from_file_name(player_file)
                name = player_file_name[0]
                surname = player_file_name[1]
                player_file = open(player_file, "r")
            except IOError:
                print "Failed opening file: " + player_file
                sys.exit()

            # extracting compressed data for players
            data = compress_data(player_file.read())
            player_file.close()

            # extracting information for player in file
            player = get_player_object(data, stats, "JOHN", "DOE")
            player_stats_helper_list = [str(i)]
            for stat in stats:
                player_stats_helper_list.append(player.stats[stat])
            player_stats_helper_list.append(player.overall)
            writer_stats.writerow(tuple(player_stats_helper_list))
            writer_general.writerow((str(j), str(i), name, surname, 'cb', '2016-01-03'))
            if i % 11 == 0:
                j += 1
            i += 1



output_stats.close()
output_general.close()
