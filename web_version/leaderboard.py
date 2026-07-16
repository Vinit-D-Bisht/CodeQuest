import json

FILE="data/leaderboard.json"


def save_score(name, xp):

    with open(FILE) as f:
        data=json.load(f)

    data.append({
        "name":name,
        "xp":xp
    })

    data.sort(
        key=lambda x:x["xp"],
        reverse=True
    )

    with open(FILE,"w") as f:
        json.dump(data[:10],f,indent=4)


    return data[:10]


def get_scores():

    with open(FILE) as f:
        return json.load(f)