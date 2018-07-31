import machine
import neopixel
import time
import socket
import os
import math
from asyn import *
import asyn


async def begin():
    np = neopixel.NeoPixel(machine.Pin(13, machine.Pin.OUT), 102)
    all_leds = list(range(17*i, 17*(i+1)) for i in reversed(range(6)))

    for i in range(102):
        np[i] = (255, 255, 255)
        np.write()
        time.sleep_ms(25)

    for i in range(102):
        np[i] = (0, 0, 0)
    time.sleep_ms(10)
    np.write()

    return np, all_leds


def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('JaskiniaSmoka', 'Czerwony$m0k')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


async def color(np, leds, br, r, g, b):
    br = int(br)
    r, g, b = int(int(r)*(br/255)), int(int(g)*(br/255)), int(int(b)*(br/255))
    for led in leds:
        np[led] = (r, g, b)


async def serve(reader, writer):
    data = await reader.read(512)
    message = data.decode()
    conds, br, r, g, b, mode = str(
        message[message.find('/') + 1:message.find(' HTTP')]).split('?')
    await writer.awrite(message)
    await writer.aclose()
    np, all_leds = await begin()

    if message == 'x':
        await NamedTask('loops', loops)
    else:
        await NamedTask.cancel('loops')

# THAT IS GOOD SHIT =D


@cancellable
async def loops():
    while True:
        print("Dupa")
        await asyncio.sleep(1)


if __name__ == '__main__':
    do_connect()

    loop = asyncio.get_event_loop()
    loop.create_task(asyncio.start_server(serve, "0.0.0.0", 80))
    loop.run_forever()
    loop.close()
cd