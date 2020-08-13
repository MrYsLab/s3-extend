#!/usr/bin/env python3

"""
robohat_gateway.py

This is the OneGPIO gateway for pymata_rh

 Copyright (c) 2020 Alan Yorinks All right reserved.

 This software is free software; you can redistribute it and/or
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

from python_banyan.gateway_base import GatewayBase
from pymata_rh import pymata_rh
import argparse
import signal
import sys


class RoboHatGateway(GatewayBase):
    """
    This is a good starting point for creating your own Banyan GPIO Gateway

    Search for GpioGatewayTemplate and gpio_gateway_template, and then replace
    with a names of your own making.

    Change the -l and -n options at the bottom of this file
    to be consistent with the specific board type
    """

    # noinspection PyDefaultArgument,PyRedundantParentheses
    def __init__(self, *subscriber_list, **kwargs):
        """

        :param subscriber_list: a tuple or list of topics to be subscribed to
        :param kwargs: contains the following parameters:

            back_plane_ip_address: banyan_base back_planeIP Address -
               if not specified, it will be set to the local computer
            subscriber_port: banyan_base back plane subscriber port.
               This must match that of the banyan_base backplane
            publisher_port: banyan_base back plane publisher port.
                               This must match that of the banyan_base
                               backplane
            process_name: Component identifier
            board_type: target micro-controller type ID

        """
        # initialize the parent
        super(RoboHatGateway, self).__init__(
            subscriber_list=subscriber_list,
            back_plane_ip_address=kwargs[
                'back_plane_ip_address'],
            subscriber_port=kwargs[
                'subscriber_port'],
            publisher_port=kwargs[
                'publisher_port'],
            process_name=kwargs[
                'process_name'],
            board_type=kwargs['board_type']
        )

        # instantiate pymata_rh
        self.robohat = pymata_rh.PymataRh(kwargs[
                                              'com_port'], kwargs['arduino_instance_id'])
        # start the banyan receive loop
        try:
            self.receive_loop()
        except KeyboardInterrupt:
            self.clean_up()
            sys.exit(0)

    def init_pins_dictionary(self):
        """
        The pins dictionary is an array of dictionary items that you create
        to describe each GPIO pin. In this dictionary, you can store things
        such as the pins current mode, the last value reported for an input pin
        callback method for an input pin, etc.
        """

        # not used for robohat gateway, but must be initialized.
        self.pins_dictionary = []

    def additional_banyan_messages(self, topic, payload):
        """
        This method will pass any messages not handled by this class to the
        specific gateway class. Must be overwritten by the hardware gateway
        class.
        :param topic: message topic
        :param payload: message payload
        """
        if payload['command'] == 'initialize_mpu':
            self.robohat.mpu_9250_initialize(callback=self.mpu_callback)
        elif payload['command'] == 'read_mpu':
            self.robohat.mpu_9250_read_data()
        elif payload['command'] == 'initialize_ina':
            self.robohat.ina_initialize(callback=self.ina_callback)
        elif payload['command'] == 'get_ina_bus_voltage':
            self.robohat.ina_read_bus_voltage()
        elif payload['command'] == 'get_ina_bus_current':
            self.robohat.ina_read_bus_current()
        elif payload['command'] == 'get_supply_voltage':
            self.robohat.ina_read_supply_voltage()
        elif payload['command'] == 'get_shunt_voltage':
            self.robohat.ina_read_shunt_voltage()
        elif payload['command'] == 'get_power':
            self.robohat.ina_read_power()

    def digital_write(self, topic, payload):
        """
        This method will pass any messages not handled by this class to the
        specific gateway class. Must be overwritten by the hardware gateway
        class.
        :param topic: message topic
        :param payload: message payload
        """
        self.robohat.digital_write(payload["pin"], payload['value'])

    def disable_analog_reporting(self, topic, payload):
        """
        This method will pass any messages not handled by this class to the
        specific gateway class. Must be overwritten by the hardware gateway
        class.
        :param topic: message topic
        :param payload: message payload
        """
        raise NotImplementedError

    def disable_digital_reporting(self, topic, payload):
        """
        This method will pass any messages not handled by this class to the
        specific gateway class. Must be overwritten by the hardware gateway
        class.
        :param topic: message topic
        :param payload: message payload
        """
        raise NotImplementedError

    def enable_analog_reporting(self, topic, payload):
        """
        This method will pass any messages not handled by this class to the
        specific gateway class. Must be overwritten by the hardware gateway
        class.
        :param topic: message topic
        :param payload: message payload
        """
        raise NotImplementedError

    def enable_digital_reporting(self, topic, payload):
        """
        This method will pass any messages not handled by this class to the
        specific gateway class. Must be overwritten by the hardware gateway
        class.
        :param topic: message topic
        :param payload: message payload
        """
        raise NotImplementedError

    def i2c_read(self, topic, payload):
        """
        This method will pass any messages not handled by this class to the
        specific gateway class. Must be overwritten by the hardware gateway
        class.
        :param topic: message topic
        :param payload: message payload
        """
        raise NotImplementedError

    def i2c_write(self, topic, payload):
        """
        This method will pass any messages not handled by this class to the
        specific gateway class. Must be overwritten by the hardware gateway
        class.
        :param topic: message topic
        :param payload: message payload
        """
        raise NotImplementedError

    def play_tone(self, topic, payload):
        """
        This method will pass any messages not handled by this class to the
        specific gateway class. Must be overwritten by the hardware gateway
        class.
        :param topic: message topic
        :param payload: message payload
        """
        raise NotImplementedError

    def pwm_write(self, topic, payload):
        """

        This method sets the pwm value for the selected pin.
        Call set_mode_pwm before calling this method.
        :param topic: from_robohat_gui
        :param payload: {“command”: “pwm_write”, "pin": “PIN”,
                         "tag":”TAG”,
                          “value”: “VALUE”}
        """
        self.robohat.pwm_write(payload["pin"], payload['value'])

    def servo_position(self, topic, payload):
        """
        This method will pass any messages not handled by this class to the
        specific gateway class. Must be overwritten by the hardware gateway
        class.
        :param topic: message topic
        :param payload: message payload
        """
        # self.pins_dictionary[pin][GatewayBase.PIN_MODE] = GatewayBase.SERVO_MODE
        self.robohat.servo_write(payload["pin"], payload["position"])

    def set_mode_analog_input(self, topic, payload):
        """
        This method will pass any messages not handled by this class to the
        specific gateway class. Must be overwritten by the hardware gateway
        class.
        :param topic: message topic
        :param payload: message payload
        """
        pin = payload["pin"]
        # self.pins_dictionary[pin + self.first_analog_pin][GatewayBase.PIN_MODE] = \
        #     GatewayBase.ANALOG_INPUT_MODE
        self.robohat.set_pin_mode_analog_input(pin, self.analog_input_callback)

    def set_mode_digital_input(self, topic, payload):
        """
        This method will pass any messages not handled by this class to the
        specific gateway class. Must be overwritten by the hardware gateway
        class.
        :param topic: message topic
        :param payload: message payload
        """
        pin = payload["pin"]
        # self.pins_dictionary[pin][GatewayBase.PIN_MODE] = GatewayBase.DIGITAL_INPUT_PULLUP_MODE
        self.robohat.set_pin_mode_digital_input_pullup(pin, self.digital_input_callback)

    def set_mode_digital_input_pullup(self, topic, payload):
        """
        This method will pass any messages not handled by this class to the
        specific gateway class. Must be overwritten by the hardware gateway
        class.
        :param topic: message topic
        :param payload: message payload
        """
        raise NotImplementedError

    def set_mode_digital_output(self, topic, payload):
        """
        This method will pass any messages not handled by this class to the
        specific gateway class. Must be overwritten by the hardware gateway
        class.
        :param topic: message topic
        :param payload: message payload
        """
        pin = payload["pin"]
        # self.pins_dictionary[pin][GatewayBase.PIN_MODE] = GatewayBase.DIGITAL_OUTPUT_MODE
        self.robohat.set_pin_mode_digital_output(pin)

    def set_mode_i2c(self, topic, payload):
        """
        This method will pass any messages not handled by this class to the
        specific gateway class. Must be overwritten by the hardware gateway
        class.
        :param topic: message topic
        :param payload: message payload
        """
        raise NotImplementedError

    def set_mode_pwm(self, topic, payload):
        """
        This method will pass any messages not handled by this class to the
        specific gateway class. Must be overwritten by the hardware gateway
        class.
        :param topic: message topic
        :param payload: message payload
        """
        pin = payload["pin"]
        # self.pins_dictionary[pin][GatewayBase.PIN_MODE] = GatewayBase.PWM_OUTPUT_MODE
        self.robohat.set_pin_mode_pwm_output(pin)

    def set_mode_servo(self, topic, payload):
        """
        This method will pass any messages not handled by this class to the
        specific gateway class. Must be overwritten by the hardware gateway
        class.
        :param topic: message topic
        :param payload: message payload
        """
        pin = payload["pin"]
        # self.pins_dictionary[pin][GatewayBase.PIN_MODE] = GatewayBase.SERVO_MODE
        self.robohat.set_pin_mode_servo(pin)

    def set_mode_sonar(self, topic, payload):
        """
        This method will pass any messages not handled by this class to the
        specific gateway class. Must be overwritten by the hardware gateway
        class.
        :param topic: message topic
        :param payload: message payload
        """
        raise NotImplementedError

    def set_mode_stepper(self, topic, payload):
        """
        Set the mode for the specific board.
        Must be overwritten by the hardware gateway class.
        :param topic: message topic
        :param payload: message payload
        """
        raise NotImplementedError

    def set_mode_tone(self, topic, payload):
        """
        Must be overwritten by the hardware gateway class.
        Handles a digital write
        :param topic: message topic
        :param payload: message payload
        """
        raise NotImplementedError

    def digital_read(self, pin):
        raise NotImplementedError

    def stepper_write(self, topic, payload):
        """
        Must be overwritten by the hardware gateway class.
        Handles a pwm write
        :param topic: message topic
        :param payload: message payload
        """
        raise NotImplementedError

    def analog_input_callback(self, data):
        # data = [pin mode, pin, current reported value, timestamp]
        # self.pins_dictionary[data[1] + self.arduino.first_analog_pin][GatewayBase.LAST_VALUE] = data[2]
        payload = {'report': 'analog_input', 'pin': data[1],
                   'value': data[2], 'timestamp': data[3]}
        self.publish_payload(payload, 'from_robohat_gateway')

    def digital_input_callback(self, data):
        """
        Digital input data change reported by Arduino
        :param data:
        :return:
        """
        # data = [pin mode, pin, current reported value, timestamp]
        # self.pins_dictionary[data[1]][GatewayBase.LAST_VALUE] = data[2]
        payload = {'report': 'digital_input', 'pin': data[1],
                   'value': data[2], 'timestamp': data[3]}
        self.publish_payload(payload, 'from_robohat_gateway')

    def mpu_callback(self, data):
        """
        Digital input data change reported by Arduino
        :param data:
                 index[0] = pin type - for mpu9250 the value is 16
                 index[1] = mpu address
                 index[2] = accelerometer x axis
                 index[3] = accelerometer y axis
                 index[4] = accelerometer z axis
                 index[5] = gyroscope x axis
                 index[6] = gyroscope y axis
                 index[7] = gyroscope z axis
                 index[8] = magnetometer x axis
                 index[9] = magnetometer y axis
                 index[10] = magnetometer z axis
                 index[11] = temperature
                 index[12] = timestamp
        :return:
        """
        # data = [pin mode, pin, current reported value, timestamp]
        # self.pins_dictionary[data[1]][GatewayBase.LAST_VALUE] = data[2]
        payload = {'report': 'mpu',
                   'Ax': data[2], 'Ay': data[3], 'Az': data[4],
                   'Gx': data[5], 'Gy': data[6], 'Gz': data[7],
                   'Mx': data[8], 'My': data[9], 'Mz': data[10],
                   'Temperature': data[11]
                   }
        self.publish_payload(payload, 'from_robohat_gateway')

    def ina_callback(self, data):
        payload = {}
        cb_reported_value = data[3]
        if data[2] == 0:
            payload = {'report': 'ina', 'param': 'V', 'value': cb_reported_value}
        elif data[2] == 1:
            payload = {'report': 'ina', 'param': ' A', 'value': cb_reported_value}
        elif data[2] == 2:
            payload = {'report': 'ina', 'param': 'Supply', 'value': cb_reported_value}
        elif data[2] == 3:
            payload = {'report': 'ina', 'param': 'Shunt', 'value': cb_reported_value}
        elif data[2] == 4:
            payload = {'report': 'ina', 'param': 'Power', 'value': cb_reported_value}
        self.publish_payload(payload, 'from_robohat_gateway')


def robohat_gateway():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", dest="back_plane_ip_address", default="None",
                        help="None or IP address used by Back Plane")
    parser.add_argument("-c", dest="com_port", default="None",
                        help="Use this COM port instead of auto discovery")
    parser.add_argument("-d", dest="board_type", default="None",
                        help="This parameter identifies the target GPIO "
                             "device")
    parser.add_argument("-i", dest="arduino_instance_id", default="1",
                        help="Set an Arduino Instance ID and match it in FirmataExpress")
    parser.add_argument("-g", dest="log", default="False",
                        help="Set to True to turn logging on.")
    parser.add_argument("-l", dest="subscriber_list",
                        default="to_robohat_gateway", nargs='+',
                        help="Banyan topics space delimited: topic1 topic2 "
                             "topic3")
    parser.add_argument("-n", dest="process_name", default="RoboHatGateway",
                        help="Set process name in banner")
    parser.add_argument("-p", dest="publisher_port", default='43124',
                        help="Publisher IP port")
    parser.add_argument("-s", dest="subscriber_port", default='43125',
                        help="Subscriber IP port")
    parser.add_argument("-t", dest="loop_time", default=".1",
                        help="Event Loop Timer in seconds")

    args = parser.parse_args()
    if args.back_plane_ip_address == 'None':
        args.back_plane_ip_address = None
    if args.board_type == 'None':
        args.back_plane_ip_address = None
    if args.com_port == 'None':
        args.com_port = None
    kw_options = {
        'back_plane_ip_address': args.back_plane_ip_address,
        'publisher_port': args.publisher_port,
        'subscriber_port': args.subscriber_port,
        'process_name': args.process_name,
        'loop_time': float(args.loop_time),
        'board_type': args.board_type,
        'com_port': args.com_port,
        'arduino_instance_id': int(args.arduino_instance_id)
    }
    try:
        RoboHatGateway(args.subscriber_list, **kw_options)
    except KeyboardInterrupt:
        sys.exit()


# signal handler function called when Control-C occurs
# noinspection PyShadowingNames,PyUnusedLocal,PyUnusedLocal
def signal_handler(sig, frame):
    print('Exiting Through Signal Handler')
    raise KeyboardInterrupt


# listen for SIGINT
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    # replace with name of function you defined above
    robohat_gateway()
