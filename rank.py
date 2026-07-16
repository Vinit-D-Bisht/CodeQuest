def get_rank(xp):
    if xp < 100:
        return "🥉 Beginner"
    elif xp < 250:
        return "🥈 Learner"
    elif xp < 500:
        return "🥇 Explorer"
    elif xp < 1000:
        return "🏆 Scholar"
    elif xp < 2000:
        return "💎 Expert"
    else:
        return "👑 Legend"