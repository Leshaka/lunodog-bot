from core import dc, Log


class Bot:
    was_ready = False


@dc.event
async def on_think(frame_time: float):
    Log.debug(f'tick @ {frame_time}')


@dc.event
async def on_ready():
    if not Bot.was_ready:
        Log.info(f"Logged in discord as '{dc.user.name}#{dc.user.discriminator}'.")
        Bot.was_ready = True
    else:
        Log.info(f"Reconnected to discord")
