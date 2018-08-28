import machine
import neopixel
import time
import socket
import os
import math
from struct import unpack
import _thread as th


def begin():
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


def recive_socket():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(addr)
    s.listen(5)
    print('socket established')

    return s


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


def get_command(soc):
    conn, addr = soc.accept()
    rq = str(conn.recv(512))
    conn.send('ESP32')
    command = rq[rq.find('/')+1:rq.find('&')]
    conn.close()
    print(command)

    return command


def color(np, leds, br, r, g, b):

    br = int(br)
    r, g, b = int(int(r)*(br/255)), int(int(g)*(br/255)), int(int(b)*(br/255))
    for led in leds:
        np[led] = (r, g, b)


def random_player(T=0.01, Txp=10):
    color(np, range(102), 0, 0, 0, 0)
    RNG, = unpack('<H', os.urandom(2))
    RNG = RNG % 6
    for i in range(18+RNG):
        color(np, all_leds[i % 6], 255, 255, 255, 255)
        np.write()
        time.sleep(math.sqrt(T))
        color(np, all_leds[i % 6], 0, 0, 0, 0)
        Tx, = unpack('<H', os.urandom(2))
        Tx = Tx % Txp
        T += Tx/1000

    color(np, all_leds[RNG], 255, 255, 0, 0)
    np.write()
    time.sleep_ms(2000)


def fire_effect(br):
    tx = 0
    while tx < 2000:
        for i in range(102):
            flicker, = unpack('<H', os.urandom(2))
            flicker = flicker % 40
            r = 255 - flicker
            g = 96 - flicker
            b = abs(12 - flicker)
            color(np, [i], br, r, g, b)
        np.write()
        t, = unpack('<H', os.urandom(2))
        t = t % 100 + 50
        time.sleep_ms(t)
        tx += t

    return 2


def update(np):
    soc = recive_socket()
    while True:
        try:
            command = get_command(soc)
            conds, br, r, g, b, mode = command.split('?')
        except Exception as e:
            print('Time~!')
            mode = form_mode
            soc.setblocking(False)
            continue

        table = zip(list(conds), all_leds)
        for con, leds in table:
            if int(con):
                color(np, leds, br, r, g, b)

        if int(mode) == 1:
            colors = [np[i] for i in range(102)]
            random_player()

            for led, colo in enumerate(colors):
                np[led] = colo

        elif int(mode) == 2:
            colors = [np[i] for i in range(102)]
            soc.settimeout(2)
            fire_effect(br)

        np.write()
        time.sleep_ms(5)


if __name__ == '__main__':
    np, all_leds = begin()
    do_connect()
    update(np)
