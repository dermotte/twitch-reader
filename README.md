# Twitch Reader

Goal of this python scripts is to read streams from twitch to give predicitions on their popularity. The _New Twitch API_ allows for scraping the running channels using `https://api.twitch.tv/helix/streams?...` and returns number of viewers, etc.

Note: The Python script youtube-dl can download and store streams.

Problems: Twitch does the pagination online, that means that we cannot access the full list. Entries may be twice in there or not even show up at all. The faster we scrape the list the better.

`read_streams_data.py` can analyze the downloads from `read_streams.py` and currently is able to create simple plots, i.e. analysis of rank to viewer_count shows typical power law distributions:

<p align="center">
  <img src="https://github.com/dermotte/twitch-reader/raw/master/rank2viewercount.png"/>
</p>

Games and game ids can be queried using `read_top_games.py`.

## How to setup

First get a client ID from Twitch, then put it into the file `credentials.py` or create a text file `client_id.txt` in the project root folder with just the client id in a single line. `client_id.txt` will be read by `credentials.py` on import.
