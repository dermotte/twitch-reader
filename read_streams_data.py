import codecs
import json

from dateutil import parser, tz

"""
    reads the json output of the other python file and prints a table with the time currently online and viewer count.
"""

utc = tz.gettz('UTC')
file_name = "streams_2018-06-22 11:00:08.691693.json"
# open the file with the json result data ..
file = codecs.open(file_name, "r", "utf-8")
# date when the poll happened is encoded in the file name
file2date = file_name[8:-1].split('.')[0]+'Z'
date_poll = parser.parse(file2date.replace(' ', 'T'))
j_data = json.load(file)
cnt = 0
cnt_0 =0
for d in j_data:
    date_tmp = parser.parse(d["started_at"])
    td = date_poll - date_tmp
    print("{},{},{},{}".format(d["viewer_count"], d["language"], d["started_at"], td.total_seconds()))
    if int(d["viewer_count"])<1: cnt_0 +=1
    cnt = cnt+1
    # print(date_tmp, datetime.datetime.now(utc) - date_tmp)
print(cnt)
print(cnt_0)
# print(j_data)
