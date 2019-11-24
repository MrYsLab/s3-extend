#!/usr/bin/env python3

"""
 This is the Python Banyan GUI that communicates with
 the Raspberry Pi Banyan Gateway

 Copyright (c) 2019 Alan Yorinks All right reserved.

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
# noinspection PyPackageRequirements
import logging
import pathlib
import serial
# noinspection PyPackageRequirements
from serial.tools import list_ports
import signal
import sys
import threading
import time
from python_banyan.banyan_base import BanyanBase


# noinspection PyMethodMayBeStatic
# class PicoboardGateway(BanyanBase, threading.Thread):
class PicoboardGateway(threading.Thread):
    """
    This class is the interface class for the picoboard supporting
    Scratch 3.

    It will regularly poll the picoboard, normalize the sensor data, and then
    publish it.
    """

    def __init__(self, back_plane_ip_address=None, subscriber_port='43125',
                 publisher_port='43124', process_name='PicoboardGateway',
                 com_port=None, publisher_topic=None, log=False):
        """
        :param back_plane_ip_address:
        :param subscriber_port:
        :param publisher_port:
        :param process_name:
        :param com_port: picoboard com_port
        """

        # super(PicoboardGateway, self).__init__(back_plane_ip_address, subscriber_port,
        #                                        publisher_port, process_name=process_name)

        self.log = log
        if self.log:
            fn = str(pathlib.Path.home()) + "/pbgw.log"
            self.logger = logging.getLogger(__name__)
            logging.basicConfig(filename=fn, filemode='w', level=logging.DEBUG)
            sys.excepthook = self.my_handler

        self.baud_rate = 38400
        self.publisher_topic = publisher_topic

        # place to receive data from picoboard
        self.data_packet = None

        # channel 0 = board id
        # channel 1 = D  analog
        # channel 2 = C  analog
        # channel 3 = B  analog
        # channel 4 = Button  digital inverted logic
        # channel 5 = A  analog
        # channel 6 = Light  analog inverted logic
        # channel 7 = sound  analog
        # channel 8 = slider analog

        self.analog_sensor_list = [1, 2, 3, 5, 6, 7, 8]

        self.button_channel = 4
        self.light_channel = 6

        # payload used to publish picoboard values
        self.payload = {0: 0, 1: 0, 2: 0, 3: 0,
                        4: 0, 5: 0,
                        6: 0, 7: 0, 8: 0}

        # poll request for picoboard data
        self.poll_byte = b'\x01'

        # if a com port was specified use it.
        if com_port:
            self.picoboard = serial.Serial(com_port, self.baud_rate,
                                           timeout=1, writeTimeout=0)
        # otherwise try to find a picoboard
        else:
            self.find_the_picoboard()
            print('picoboard found on:', self.picoboard.port)

        # start the thread to receive data from the picoboard
        threading.Thread.__init__(self)
        self.daemon = True
        self.stop_event = threading.Event()
        self.start()

        # allow thread time to start
        time.sleep(.2)

        while True:
            try:
                time.sleep(.001)
                # request data
                self.picoboard.write(self.poll_byte)
            except KeyboardInterrupt:
                self.picoboard.close()
                sys.exit(0)

    def find_the_picoboard(self):
        """
        Go through the ports looking for an active board
        """
        #
        the_ports_list = list_ports.comports()
        for port in the_ports_list:
            if port.pid is None:
                continue
            else:
                print('Looking for picoboard on: ', port.device)
                self.picoboard = serial.Serial(port.device, self.baud_rate,
                                               timeout=1, writeTimeout=0)
                # send multiple polls to allow for serial port to open
                for send in range(10):
                    self.picoboard.write(self.poll_byte)
                    time.sleep(.2)
                    num_bytes = self.picoboard.inWaiting()
                    if num_bytes == 18:
                        self.picoboard.reset_input_buffer()
                        self.picoboard.reset_output_buffer()
                        return
                    else:
                        continue
            continue
        print('Could not find a picoboard')
        sys.exit(0)

    def analog_scaling(self, value, channel):
        """
        scale the normal analog input range of 0-1023 to 0-100
        :param value:
        :param channel: sensor channel
        :return: A value scaled between 0 and 100
        """
        if channel == self.light_channel:  # the light channel
            input_low = 1023
            input_high = 0
        else:
            input_low = 0
            input_high = 1023

        new_value_low = 0
        new_value_high = 100

        return round(((value - input_low) * ((new_value_high - new_value_low) / (input_high - input_low))) +
                     new_value_low)

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
        """
        This method run continually, receiving responses
        to the poll request.
        """
        while True:
            self.data_packet = None
            # if there is data available from the picoboard
            # retrieve 18 bytes - a full picoboard packet
            if self.picoboard.inWaiting():
                self.data_packet = self.picoboard.read(18)
                # get the channel number and data for the channel
                for i in range(9):
                    # pico_channel = self.channels[(int(self.data_packet[2 * i]) - 128) >> 3]
                    raw_sensor_value = ((int(self.data_packet[2 * i]) & 7) << 7) + int(self.data_packet[2 * i + 1])
                    if i == 0:  # id
                        self.payload[0] = raw_sensor_value
                    if i in self.analog_sensor_list:
                        # scale for standard analog:
                        cooked = self.analog_scaling(raw_sensor_value, i)
                        # self.payload[pico_channel] = cooked
                        self.payload[i] = cooked

                    elif i == self.button_channel:  # invert digital input
                        cooked = int(not raw_sensor_value)
                        # self.payload[pico_channel] = cooked
                        self.payload[i] = cooked

                # self.publish_payload(self.payload, self.publisher_topic)
                print(self.payload)
            else:
                # no data available, just kill some time
                try:
                    time.sleep(.001)
                except KeyboardInterrupt:
                    sys.exit(0)


def picoboard_gateway():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", dest="back_plane_ip_address", default="None",
                        help="None or IP address used by Back Plane")
    parser.add_argument("-c", dest="com_port", default="None",
                        help="Use this COM port instead of auto discovery")
    parser.add_argument("-l", dest="log", default="False",
                        help="Set to True to turn logging on.")
    parser.add_argument("-n", dest="process_name",
                        default="PicoboardGateway", help="Set process name in "
                                                         "banner")
    parser.add_argument("-p", dest="publisher_port", default='43124',
                        help="Publisher IP port")
    parser.add_argument("-r", dest="publisher_topic",
                        default="from_picoboard", help="Report topic")
    parser.add_argument("-s", dest="subscriber_port", default='43125',
                        help="Subscriber IP port")

    args = parser.parse_args()

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

    PicoboardGateway(**kw_options)


# signal handler function called when Control-C occurs
# noinspection PyShadowingNames,PyUnusedLocal
def signal_handler(sig, frame):
    print('Exiting Through Signal Handler')
    raise KeyboardInterrupt


# listen for SIGINT
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    picoboard_gateway()
