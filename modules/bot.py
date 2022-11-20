from core import dc, Log


class Bot:
    bot_ready = False
    was_ready = False


@dc.event
async def on_think(frame_time: float):
    Log.debug(f'tick @ {frame_time}')


@dc.event
async def on_ready():
    if not Bot.was_ready:
        Log.info(f"Logged in discord as '{dc.user.name}#{dc.user.discriminator}'.")
        Bot.was_ready = True
        Bot.bot_ready = True
    else:
        Log.info(f"Reconnected to discord.")


@dc.event
async def on_disconnect():
    Log.info("Connection to discord is lost.")
    Bot.bot_ready = False


@dc.event
async def on_resumed():
    Log.info("Connection to discord is resumed.")
    if Bot.was_ready:
        Bot.bot_ready = True
