import asyn
from asyn import *


@cancellable
async def foo(sleep):
    for i in range(sleep):
        await asyn.sleep(1)
        print(i)


@cancellable
async def candel(name):
    await asyn.sleep(3)
    await NamedTask.cancel(name)

loop = asyncio.get_event_loop()
loop.create_task(NamedTask('asd', foo, 10)())
loop.create_task(NamedTask('timerx', candel, 'asd')())
loop.run_forever()
