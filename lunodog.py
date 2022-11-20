import asyncio
import signal
import time
import queue
import traceback

import core
import modules
import api


def ctrl_c():
    core.Console.terminate()


async def init():
    await core.Db.init()
    core.Console.init()
    for task in core.dc.events['on_init']:
        await task()


# Run commands from user console
async def run_console():
    try:
        cmd = core.Console.user_input_queue.get(False)
    except queue.Empty:
        return

    core.Log.info(cmd)
    try:
        x = eval(cmd)
        if asyncio.iscoroutine(x):
            core.Log.info(await x)
        else:
            core.Log.info(x)
    except Exception as e:
        core.Log.error("CONSOLE| ERROR: " + str(e))


# Background logic loop
async def main():

    # Loop runs roughly every 1 second
    while core.Console.alive:
        frame_time = time.time()
        await run_console()
        for task in core.dc.events['on_think']:
            try:
                await task(frame_time)
            except Exception as e:
                core.Log.error('Error running background task from {}: {}\n{}'.format(
                    task.__module__, str(e), traceback.format_exc())
                )
        await asyncio.sleep(1)

    # Exit signal received
    for task in core.dc.events['on_exit']:
        try:
            await task()
        except Exception as e:
            core.Log.error('Error running exit task from {}: {}\n{}'.format(
                task.__module__, str(e), traceback.format_exc())
            )

    core.Log.info("Waiting for connection to close...")
    await core.dc.close()

    if core.cfg.API_ENABLE:
        core.Log.info("Closing API server...")
        await api.ApiServer.runner.cleanup()

    core.Log.info("Closing db...")
    await core.Db.close()

    core.Log.info("Closing log...")
    core.Log.close()

    print("Exit now.")
    loop.stop()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    for signal in [signal.SIGINT, signal.SIGTERM]:
        loop.add_signal_handler(signal, ctrl_c)
    loop.run_until_complete(init())
    if core.cfg.API_ENABLE:
        loop.run_until_complete(api.ApiServer.start())
    loop.create_task(core.dc.start(core.cfg.DC_BOT_TOKEN))
    loop.run_until_complete(main())
