import codecs
import json
import matplotlib.pyplot as plt
import numpy as np
import glob
import pandas as pd

from dateutil import parser, tz

"""
    reads the json output of the other python file and prints a table with the time currently online and viewer count.
"""
games = []
times = []
data = {}

# get all the games listed ...
l = sorted(glob.glob('ou2/games_stats_*.json'))
for file_name in l:
    file = codecs.open(file_name, "r", "utf-8")
    file2date = (file_name[file_name.index('games_stats_')+len('games_stats_'):-1].split('.')[0] + 'Z').replace(' ', 'T')
    date_poll = parser.parse(file2date)
    times.append(date_poll)
    j_data = json.load(file)
    for d in j_data:
        if d['game']['name'] not in games:
            games.append(d['game']['name'])

for g in games:
    data[g] = []
for file_name in l:
    games_visited = []
    file = codecs.open(file_name, "r", "utf-8")
    file2date = (file_name[file_name.index('games_stats_')+len('games_stats_'):-1].split('.')[0] + 'Z').replace(' ', 'T')
    date_poll = parser.parse(file2date)
    j_data = json.load(file)
    for d in j_data:
        data[d['game']['name']].append(d['viewers'])
        games_visited.append(d['game']['name'])
    for g in games:
        if g not in games_visited:
            data[g].append(0)
#        if "Fortnite" in d['game']['name']:
#            print("{}\t{}\t{}".format(d['viewers'], d['game']['name'], date_poll))


df = pd.DataFrame(data, index=["{:02d}".format(t.month) + "-{:02d}".format(t.day) + "-" + "{:02d}".format(t.hour)+":"+"{:02d}".format(t.minute) for t in times])
df['hour'] = [x[:x.index(':')] for x in df.index]  # per hour
# df['day'] = index=["{:02d}-{:02d}".format(t.month, t.day) for t in times]
# df_hour = df.groupby(['day']).max()  # per hour
df_hour = df.groupby(['hour']).mean()  # per hour
# df = pd.DataFrame(data, index=times)
f = plt.figure(figsize=(16,9))
for i in range(16):
    # if games[i] not in "FreezeME":
    plt.plot(df_hour[games[i]], label=games[i])
plt.xlabel('Hour in UTC (month-day-hour)')
plt.ylabel('Number of viewers')
plt.title("Development of viewers per game in 15 minute steps (avg over full hours)")
plt.xticks(df_hour.index, rotation='vertical')
plt.legend()
plt.show()
f.savefig("foo.pdf", bbox_inches='tight')

# get data for JavaScript chart.js ...
out = "var chartData = ["
for i in range(11):
    if games[i] not in "FreezeME":
        # print(games[i])
        data_ = """label: '{}',fill: false,backgroundColor: colors[currentColor],borderColor: colors[currentColor++],data: {},"""
        d_ = "["
        for v in df[games[i]].values:
            d_ += str(v) + ", "
        d_ = d_[:-2]+"]"
        out += " {" + data_.format(games[i].replace('\'', '\\\''), d_) + "}, "
print(out + "]")
print("var labels = " + str([str(x[3:]) for x in df.index]) + "\n")