"""
 This is the Python Banyan Hardware Gateway for the
 Adafruit Circuit Playground Express.

 Copyright (c) 2020 Alan Yorinks All right reserved.

 Python Banyan is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
import argparse
import atexit
import logging
import math
import os
import pathlib
import signal
import sys
import threading
import time

import serial
from pymata_cpx.pymata_cpx import PyMataCpx
from python_banyan.gateway_base import GatewayBase


# noinspection PyMethodMayBeStatic
class CpxGateway(GatewayBase, threading.Thread):
    """
    This class is the interface class for the Circuit Playground
    Express supporting Scratch 3.
    """

    def __init__(self, *subscriber_list, back_plane_ip_address=None, subscriber_port='43125',
                 publisher_port='43124', process_name='CpxGateway',
                 publisher_topic=None, log=False):
        """
        :param subscriber_list: a tuple or list of subscription topics.
        :param back_plane_ip_address:
        :param subscriber_port:
        :param publisher_port:
        :param process_name:
        """

        # initialize parent
        super(CpxGateway, self).__init__(subscriber_list=subscriber_list,
                                         back_plane_ip_address=back_plane_ip_address,
                                         subscriber_port=subscriber_port,
                                         publisher_port=publisher_port, process_name=process_name)
        self.log = log
        if self.log:
            fn = str(pathlib.Path.home()) + "/cpxgw.log"
            self.logger = logging.getLogger(__name__)
            logging.basicConfig(filename=fn, filemode='w', level=logging.DEBUG)
            sys.excepthook = self.my_handler

        self.publisher_topic = publisher_topic
        self.cpx = PyMataCpx()
        atexit.register(self.shutdown)

        # hold the time of the last analog data to be received.
        # use to determine if connectivity is gone.
        self.last_analog_data_time = None

        # start up all the sensors
        self.cpx.cpx_accel_start(self.tilt_callback)
        self.cpx.cpx_button_a_start(self.switch_callback)
        self.cpx.cpx_button_b_start(self.switch_callback)
        self.cpx.cpx_slide_switch_start(self.switch_callback)

        self.cpx.cpx_light_sensor_start(self.analog_callback)
        self.cpx.cpx_microphone_start(self.analog_callback)
        self.cpx.cpx_temperature_start(self.analog_callback)
        for touch_pad in range(1, 8):
            self.cpx.cpx_cap_touch_start(touch_pad, self.touchpad_callback)

        threading.Thread.__init__(self)
        self.daemon = True

        # start the watchdog thread
        self.start()
        # start the banyan receive loop
        try:
            self.receive_loop()
        except:
            pass
        # except KeyboardInterrupt:
        # except KeyboardInterrupt:
            # self.cpx.cpx_close_and_exit()
            # sys.exit(0)
        #     os._exit(1)


    def init_pins_dictionary(self):
        pass

    def play_tone(self, topic, payload):
        """
        This method plays a tone on a piezo device connected to the selected
        pin at the frequency and duration requested.
        Frequency is in hz and duration in milliseconds.

        Call set_mode_tone before using this method.
        :param topic: message topic
        :param payload: {"command": "play_tone", "pin": “PIN”, "tag": "TAG",
                         “freq”: ”FREQUENCY”, duration: “DURATION”}
        """
        self.cpx.cpx_tone(payload['freq'], payload['duration'])

    def additional_banyan_messages(self, topic, payload):
        if payload['command'] == 'pixel':
            self.set_pixel(payload)

    def set_pixel(self, payload):
        self.cpx.cpx_pixel_set(payload['pixel'], payload['red'],
                               payload['green'], payload['blue'])
        self.cpx.cpx_pixels_show()

    def digital_write(self, topic, payload):
        """
        This method performs a digital write to the board LED
        :param topic: message topic
        :param payload: {"command": "digital_write", "pin": “PIN”, "value": “VALUE”}
        """
        if payload['value']:
            self.cpx.cpx_board_light_on()
        else:
            self.cpx.cpx_board_light_off()

    # The CPX sensor callbacks

    def tilt_callback(self, data):
        """
        Report the tilt of the express board

        Take the raw xyz data and transform it to
        positional strings.
        :param data: data [0] = data mode 32 is analog.
                     data[1] = the pin number - this is a pseudo pin number
                     data[2] = x value
                     data[3] = y value
                     data[4] = z value
        """
        x = data[2]
        y = data[3]
        z = data[4]

        # Convert raw Accelerometer values to degrees
        x_angle = int((math.atan2(y, z) + math.pi) * (180 / math.pi))
        y_angle = int((math.atan2(z, x) + math.pi) * (180 / math.pi))

        h = v = -1

        if 175 < x_angle < 185 and 265 < y_angle < 275:
            h = v = 0  # 'flat'

        elif h or v:
            if 180 <= x_angle <= 270:
                v = 1  # up

            elif 90 <= x_angle <= 180:
                v = 2  # down

            if 180 <= y_angle <= 270:
                h = 3  # left

            elif 270 <= y_angle <= 360:
                h = 4  # right

        payload = {'report': 'tilted', 'value': [v, h]}
        self.publish_payload(payload, 'from_cpx_gateway')

    def switch_callback(self, data):
        """
        This handles switches a, b, and slide
        :param data: data[1] - a=4 b=5, slice=7,
        """
        if data[1] == 4:
            switch = 'a'
        elif data[1] == 5:
            switch = 'b'
        else:
            # 0 = right, 1 = left
            switch ='slide'

        payload = {'report': switch, 'value': data[2]}
        self.publish_payload(payload, 'from_cpx_gateway')

    def analog_callback(self, data):
        """
        This handles the light, temperature and sound sensors.

        It also sets up a "watchdog timer" and if there is no activity
        for > 1 second will exit.


        :param data: data[1] - 8 = light, temp = 9, 10 = sound,
        """

        self.last_analog_data_time = time.time()

        if data[1] == 8:
            sensor = 'light'
        elif data[1] == 9:
            sensor = 'temp'
        else:
            sensor = 'sound'
        payload = {'report': sensor, 'value': round(data[2], 2)}
        self.publish_payload(payload, 'from_cpx_gateway')

    def touchpad_callback(self, data):
        """
        Build and send a banyan message for the pad and value
        :param data: data[1] = touchpad and data[2] = boolean value
        """
        payload = {'report': 'touch' + str(data[1]), 'value': int(data[2])}
        self.publish_payload(payload, 'from_cpx_gateway')

    def shutdown(self):
        try:
            self.cpx.cpx_close_and_exit()
            sys.exit(0)
        except serial.serialutil.SerialException:
            pass

    def my_handler(self, xtype, value, tb):
        """
        for logging uncaught exceptions
        :param xtype:
        :param value:
        :param tb:
        :return:
        """
        self.logger.exception("Uncaught exception: {0}".format(str(value)))

    def run(self):
        if not self.last_analog_data_time:
            self.last_analog_data_time = time.time()
        while True:
            if time.time() - self.last_analog_data_time > 1.0:
                print('Watchdog timed out - exiting.')
                os._exit(1)

            time.sleep(1)


def cpx_gateway():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", dest="back_plane_ip_address", default="None",
                        help="None or IP address used by Back Plane")
    parser.add_argument("-c", dest="com_port", default="None",
                        help="Use this COM port instead of auto discovery")
    parser.add_argument("-l", dest="log", default="False",
                        help="Set to True to turn logging on.")
    parser.add_argument("-m", dest="subscriber_list",
                        default="to_cpx_gateway", nargs='+',
                        help="Banyan topics space delimited: topic1 topic2 topic3")
    parser.add_argument("-n", dest="process_name",
                        default="CpxGateway", help="Set process name in "
                                                   "banner")
    parser.add_argument("-p", dest="publisher_port", default='43124',
                        help="Publisher IP port")
    parser.add_argument("-r", dest="publisher_topic",
                        default="from_cpx_gateway", help="Report topic")
    parser.add_argument("-s", dest="subscriber_port", default='43125',
                        help="Subscriber IP port")

    args = parser.parse_args()

    subscriber_list = args.subscriber_list

    kw_options = {
        'publisher_port': args.publisher_port,
        'subscriber_port': args.subscriber_port,
        'process_name': args.process_name,
        'publisher_topic': args.publisher_topic
    }

    if args.back_plane_ip_address != 'None':
        kw_options['back_plane_ip_address'] = args.back_plane_ip_address

    if args.com_port != 'None':
        kw_options['com_port'] = args.com_port

    log = args.log.lower()
    if log == 'false':
        log = False
    else:
        log = True

    kw_options['log'] = log

    cpx = CpxGateway(subscriber_list, **kw_options)


# signal handler function called when Control-C occurs
# noinspection PyShadowingNames,PyUnusedLocal
def signal_handler(sig, frame):
    print('Exiting Through Signal Handler')
    raise



# listen for SIGINT
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


if __name__ == '__main__':
    cpx_gateway()
