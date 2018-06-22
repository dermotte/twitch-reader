import codecs
import datetime
import json
import time

import requests

from twitchreader.credentials import client_id

print(client_id)

"""
    Calls twitch for getting the streams list of a particular game. 
    Sorted by view count. Result are stored as a list in a JSON file.
"""
current_dt = datetime.datetime.utcnow()
# preparing the file for output ...
with codecs.open("games_"+str(current_dt)+".json", "w", "utf-8") as file:

    # client id needed to get access to Twitch
    # client_id = ... # see twitchreader.credentials.py
    # endpoint for getting current streams
    endpoint = "https://api.twitch.tv/helix/games/top?first=100"

    all_data = []

    headers = {'Client-ID': client_id}
    result = requests.get(endpoint, headers=headers)
    json_data = result.json()
    # just add the data, leave aside the pagination cursor.
    all_data.extend(json_data["data"])
    # get out the viewer count ...
    for d in json_data["data"]:
        print(u'{}\t{}'.format(d["id"], d["name"]))

    cursor = (json_data["pagination"]["cursor"]) # cursor for the next page ...

    # fetch the next x pages ...
    for i in range(99):
        result = requests.get(endpoint + "&after=" + cursor, headers=headers)
        json_data = result.json()
        # get out the viewer count ...
        for d in json_data["data"]:
            print(u'{}\t{}'.format(d["id"], d["name"]))
        all_data.extend(json_data["data"])
        if "cursor" in json_data["pagination"] :
            cursor = (json_data["pagination"]["cursor"]) # cursor for the next page ...
        else:
            break
        time.sleep(3) # should be 3 according to the Twitch regulations!
    # closing file
    json.dump(all_data, file)
    file.close()