import asyncio

import core
import modules


async def init():
    await core.Db.init()
    core.Console.init()


async def main():
    m = modules.hello_world.MyModel(data='test', headx='kekwait')
    core.Log.info(m)
    await m.save()
    core.Log.info(m)

    core.Console.terminate()
    await core.Db.close()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(init())
    loop.run_until_complete(main())
