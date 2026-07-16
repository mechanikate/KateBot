# SHOULD BE RUN EVERY DAY AT 00:00
import json, os
def daily(path):
    print(f"{path.replace('.json','')} ...", end=" ")
    data = {"odds_power": 3, "balances": {}}
    with open(f"/home/kate/bots/katebot-2.0/econ/{path}", "r") as f:
        data = json.load(f)
    data["odds_power"] = 3
    with open(f"/home/kate/bots/katebot-2.0/econ/{path}", "w+") as f:
        json.dump(data, f)
    print("done.")
[daily(path) for path in os.listdir("/home/kate/bots/katebot-2.0/econ/")]
