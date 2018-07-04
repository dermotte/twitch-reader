import codecs
import datetime
import json
import time

import requests

from twitchreader.credentials import client_id

"""
    Calls twitch for getting the viewer count and 
    channel count on games on Twitch.
    
    Uses the Twitch v5 API, might be deprecated at some point in time
    New API doesn't give viewer count in response.
"""
current_dt = datetime.datetime.utcnow()
# preparing the file for output ...
with codecs.open("output_games/games_stats_"+str(current_dt)+".json", "w", "utf-8") as file:

    # client id needed to get access to Twitch
    # client_id = ... # see twitchreader.credentials.py
    # endpoint for getting current streams
    endpoint = "https://api.twitch.tv/kraken/games/top?limit=100"

    all_data = []

    headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
    result = requests.get(endpoint, headers=headers)
    json_data = result.json()
    # just add the data, leave aside the pagination cursor.
    all_data.extend(json_data["top"])
    # get out the viewer count ...
    for d in json_data["top"]:
        print(u'{}\t{}\t{}\t{}'.format(d["game"]["_id"], d["game"]["name"], d["channels"], d["viewers"]))

    if "pagination" in json_data:
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