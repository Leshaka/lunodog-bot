import re
from datetime import timedelta
from nextcord.utils import get, find, escape_markdown


def get_emoji(string, guild):
    emoji = get(guild.emojis, name=string)
    return '<:{}:{}>'.format(emoji.name, emoji.id) if emoji else None


def parse_duration(string):
    # Parse format 14:00:15
    if re.match(r"^\d\d:\d\d:\d\d$", string):
        x = sum(x * int(t) for x, t in zip([3600, 60, 1], string.split(":")))
        return timedelta(seconds=x)

    # Parse format 14h 0m 15s
    elif re.match(r"^(\d+\w ?)+$", string):
        duration = 0
        for part in re.findall(r"\d+\w", string):
            val = float(part[:-1])
            if part[-1] == 's':
                duration += val
            elif part[-1] == 'm':
                duration += val * 60
            elif part[-1] == 'h':
                duration += val * 60 * 60
            elif part[-1] == 'd':
                duration += val * 60 * 60 * 24
            elif part[-1] == 'W':
                duration += val * 60 * 60 * 24 * 7
            elif part[-1] == 'M':
                duration += val * 60 * 60 * 24 * 30
            elif part[-1] == 'Y':
                duration += val * 365 * 24 * 60
            else:
                raise ValueError()
        return timedelta(seconds=int(duration))
    else:
        raise ValueError(f"Invalid time duration format {string}")
