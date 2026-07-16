import save

def check(player, score=None, level=None):

    badges = []

    if score == 5:
        badges.append("🏅 Perfect Score")

    if level == 3:
        badges.append("👑 Level Master")

    if player["xp"] >= 100:
        badges.append("⭐ Beginner")

    if player["xp"] >= 300:
        badges.append("🔥 Intermediate")

    if player["xp"] >= 600:
        badges.append("💎 Expert")

    if player["coins"] >= 200:
        badges.append("🪙 Rich")

    return badges