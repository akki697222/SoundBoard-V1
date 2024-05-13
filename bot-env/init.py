import sys
import os
import json

print("initializing...")
if not os.path.exists("sounds/sounds.json"):
    print("sounds.json not found. creating...")
    with open("config.json", "w") as file:
        json.dump({}, file, indent=4)
else:
    print("sounds.json found.")
if not os.path.exists("blacklist.json"):
    print("blacklist.json not found. creating...")
    with open("blacklist.json", "w") as file:
        json.dump({}, file, indent=4)
else:
    print("blacklist.json found.")
if not os.path.exists("config.json"):
    print("config.json not found. creating...")
    with open("config.json", "w") as file:
        json.dump({"token": "your token here", "showtoken": True, "volume": 1, "prefix": ".", "autoconnect": False, "denybot": True}, file, indent=4)
    print("Created config.json. Please insert the token in config.json before running your bot.")
    print("Exiting...")
    sys.exit()
else:
    print("config.json found.")