import json


FILE = "data/player.json"


def load_stats():

    with open(FILE,"r") as f:
        return json.load(f)



def add_xp(amount):

    data = load_stats()

    data["xp"] += amount


    if data["xp"] >= 500:
        data["rank"] = "Master"

    elif data["xp"] >= 250:
        data["rank"] = "Advanced"

    elif data["xp"] >= 100:
        data["rank"] = "Coder"

    else:
        data["rank"] = "Beginner"


    with open(FILE,"w") as f:
        json.dump(data,f,indent=4)


    return data