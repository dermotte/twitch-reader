import codecs
import json
import matplotlib.pyplot as plt
import numpy as np

from dateutil import parser, tz

"""
    reads the json output of the other python file and prints a table with the time currently online and viewer count.
"""


def get_data(file_name = "streams_2018-06-22 11:00:08.691693.json", ):
    # open the file with the json result data ..
    file = codecs.open(file_name, "r", "utf-8")
    # date when the poll happened is encoded in the file name
    file2date = file_name[8:-1].split('.')[0] + 'Z'
    date_poll = parser.parse(file2date.replace(' ', 'T'))
    j_data = json.load(file)
    cnt = 0
    cnt_0 = 0
    x = []  # rank
    y = []  # viewer count
    s = []  # seconds running
    game_id = "0"  # which game was it
    for d in j_data:
        date_tmp = parser.parse(d["started_at"])
        td = date_poll - date_tmp
        print("{},{},{},{}".format(d["viewer_count"], d["language"], d["started_at"], td.total_seconds()))
        if int(d["viewer_count"]) < 1: cnt_0 += 1
        cnt = cnt + 1
        game_id = d["game_id"]
        x.append(cnt)
        y.append(int(d["viewer_count"]))
        s.append(td.total_seconds())
        # print(date_tmp, datetime.datetime.now(utc) - date_tmp)
    print(cnt)
    print(cnt_0)
    return (x,y, s, game_id)


x1,y1, s1, g1 = get_data("streams_2018-06-22 11:00:08.691693.json")
x2,y2, s2, g2 = get_data("streams_2018-06-22 13:03:23.134448.json")
x3,y3, s3, g3 = get_data("streams_2018-06-22 13:05:20.724386.json")
x4,y4, s4, g4 = get_data("streams_2018-06-22 13:20:39.873882.json")

#plt.plot(x1, s1, label=str(g1))
plt.plot(x1, y1, label=str(g1)+ " Heroes of the Storm")
plt.plot(x3, y3, label=str(g3)+ " World of Warcraft")
plt.plot(x4, y4, label=str(g4)+ " Warframe")
plt.xlabel('rank')
plt.ylabel('viewers')
plt.title("Rank 2 ViewerCount on Twitch TV - 2018-06-22 lunch time")
plt.legend()
plt.show()
#fig = plt.figure()
#fig.suptitle("")
#ax = fig.add_subplot(111)
#ax.plot(np.array(x), np.array(y))
plt.show()

# print(j_data)
