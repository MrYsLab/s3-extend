import socket
import utime

from esp_8266_min import Esp8266

from machine import Pin


class Esp8266TcpServer:
    """
    This is an on-board esp8266 tcp server
    """

    def __init__(self):
        # allow time to connect serial monitor
        # uncomment next line for debugging
        # utime.sleep(10)

        # set pin that Red LED is connected to output
        p = Pin(16, Pin.OUT)

        print('turning led on')

        # blink Red LED 3 times to indicate this
        # is a server (morse code 'S')
        for x in range(3):
            p.value(0)
            utime.sleep_ms(50)
            p.value(1)
            utime.sleep_ms(50)
            p.value(0)
            utime.sleep_ms(50)

        # leave it lit until connection is established

        # allow any IP address on LAN to connect using port 31337
        addr = socket.getaddrinfo('0.0.0.0', 31337)[0][-1]
        print(addr)
        s = socket.socket()
        s.bind(addr)

        # wait for connection request - allow only one connection
        s.listen(1)

        # wait to accept connection request
        connect_socket, addr = s.accept()

        # set the
        # turn off Red LED
        p.value(1)
        print(connect_socket)

        # start the data processing script
        # pass in the connection socket as a result of
        # client connecting to this server
        Esp8266(connect_socket)


# create an instance of the server
Esp8266TcpServer()
