# secret client id to be set up with the twitch account
client_id = "n.a."

with open("client_id.txt") as f:
    lines = f.readlines();
    client_id = lines[0].strip()
