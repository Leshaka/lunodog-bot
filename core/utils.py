import re
import random
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
            match part[-1]:
                case 's':
                    duration += val
                case 'm':
                    duration += val * 60
                case 'h':
                    duration += val * 60 * 60
                case 'd':
                    duration += val * 60 * 60 * 24
                case 'W':
                    duration += val * 60 * 60 * 24 * 7
                case 'M':
                    duration += val * 60 * 60 * 24 * 30
                case 'Y':
                    duration += val * 365 * 24 * 60
                case _:
                    raise ValueError(f"Invalid time duration format {string}")
        return timedelta(seconds=int(duration))
    else:
        raise ValueError(f"Invalid time duration format {string}")


def random_string(length):
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(letters) for i in range(length))
