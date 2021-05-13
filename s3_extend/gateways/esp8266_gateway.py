"""
 Copyright (c) 2018-2021 Alan Yorinks All rights reserved.

 This program is free software; you can redistribute it and/or
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
import asyncio
import signal
import sys
import time

from python_banyan.gateway_base_aio import GatewayBaseAIO
from telemetrix_aio.telemetrix_aio import TelemetrixAIO


# noinspection PyAbstractClass,PyMethodMayBeStatic,PyRedundantParentheses,DuplicatedCode,GrazieInspection
class Esp8266Gateway(GatewayBaseAIO):
    # This class implements the GatewayBase interface adapted for asyncio.
    # It supports ESP8266 boards, tested with nodemcu.

    # NOTE: This class requires the use of Python 3.8 or above

    # serial_port = None

    def __init__(self, *subscriber_list, back_plane_ip_address=None,
                 subscriber_port='43125',
                 publisher_port='43124', process_name='Esp8266Gateway',
                 event_loop=None):
        """
        Set up the gateway for operation

        :param subscriber_list: a tuple or list of subscription topics.
        :param back_plane_ip_address: ip address of backplane or none if local
        :param subscriber_port: backplane subscriber port
        :param publisher_port: backplane publisher port
        :param process_name: name to display on the console
        :param event_loop: optional parameter to pass in an asyncio
                           event loop

        """

        self.pin_info = {}
        self.gpio_pins = [4, 5, 12, 13, 14, 15]

        self.back_plane_ip_address = back_plane_ip_address
        self.publisher_port = publisher_port
        self.subscriber_port = subscriber_port

        self.subscriber_list = subscriber_list

        # set the event loop to be used. accept user's if provided
        self.event_loop = event_loop

        self.connection_socket = False

        # instantiate TelemetrixAIO
        # if user want to pass in a com port, then pass it in
        self.esp = TelemetrixAIO(autostart=False, loop=self.event_loop, com_port=None)

        # Initialize the parent
        super(Esp8266Gateway, self).__init__(subscriber_list=subscriber_list,
                                             event_loop=self.event_loop,
                                             back_plane_ip_address=back_plane_ip_address,
                                             subscriber_port=subscriber_port,
                                             publisher_port=publisher_port,
                                             process_name=process_name,
                                             )

    time.sleep(.5)

    def init_pins_dictionary(self):
        """
        This method will initialize the pins dictionary contained
        in gateway base parent class. This method is called by
        the gateway base parent in its init method.

        NOTE: that this a a non-asyncio method.
        """
        # pins data structure
        # pins supported: GPIO4, GPIO5, GPIO12, GPIO13, GPIO14, GPIO15
        # modes - IN - PULL_UP, OUT - OPEN_DRAIN, PWM
        # irqs - Pin.IRQ_RISING | Pin.IRQ_FALLING

        # build a status table for the pins
        for x in self.gpio_pins:
            entry = {'mode': None, 'pull_up': False, 'drain': False,
                     'irq': None, 'duty': None, 'freq': None, 'count': 0,
                     'value': 0}
            self.pin_info[x] = entry

    async def main(self):
        # call the inherited begin method located in banyan_base_aio
        await self.begin()

        # sit in an endless loop to receive protocol messages
        while True:
            await self.receive_loop()

    async def additional_banyan_messages(self, topic, payload):
        if payload['command'] == 'ip_address':
            # start up telemetrix-aio
            if not self.connection_socket:
                self.connection_socket = True
                self.esp.ip_port = 31335
                self.esp.ip_address = payload['address']
                await self.esp.start_aio()
                await asyncio.sleep(1)

    # The following methods and are called
    # by the gateway base class in its incoming_message_processing
    # method. They overwrite the default methods in the gateway_base.

    async def digital_write(self, topic, payload):
        """
        This method performs a digital write
        :param topic: message topic
        :param payload: {"command": "digital_write", "pin": “PIN”, "value": “VALUE”}
        """

        await self.esp.digital_write(payload["pin"], payload['value'])

    async def disable_analog_reporting(self, topic, payload):
        """
        This method disables analog input reporting for the selected pin.
        :param topic: message topic
        :param payload: {"command": "disable_analog_reporting", "pin": “PIN”, "tag": "TAG"}
        """
        await self.esp.disable_analog_reporting(payload["pin"])

    async def disable_digital_reporting(self, topic, payload):
        """
        This method disables digital input reporting for the selected pin.

        :param topic: message topic
        :param payload: {"command": "disable_digital_reporting", "pin": “PIN”, "tag": "TAG"}
        """
        await self.esp.disable_digital_reporting(payload["pin"])

    async def enable_analog_reporting(self, topic, payload):
        """
        This method enables analog input reporting for the selected pin.
        :param topic: message topic
        :param payload:  {"command": "enable_analog_reporting", "pin": “PIN”, "tag": "TAG"}
        """
        await self.esp.enable_analog_reporting(payload["pin"])

    async def enable_digital_reporting(self, topic, payload):
        """
        This method enables digital input reporting for the selected pin.
        :param topic: message topic
        :param payload: {"command": "enable_digital_reporting", "pin": “PIN”, "tag": "TAG"}
        """
        await self.esp.enable_digital_reporting(payload["pin"])

    async def i2c_read(self, topic, payload):
        """
        This method will perform an i2c read by specifying the i2c
        device address, i2c device register and the number of bytes
        to read.

        Call set_mode_i2c first to establish the pins for i2c operation.

        :param topic: message topic
        :param payload: {"command": "i2c_read", "pin": “PIN”, "tag": "TAG",
                         "addr": “I2C ADDRESS, "register": “I2C REGISTER”,
                         "number_of_bytes": “NUMBER OF BYTES”}
        :return via the i2c_callback method
        """

        await self.esp.i2c_read(payload['addr'],
                                payload['register'],
                                payload['number_of_bytes'], callback=self.i2c_callback)

    async def i2c_write(self, topic, payload):
        """
        This method will perform an i2c write for the i2c device with
        the specified i2c device address, i2c register and a list of byte
        to write.

        Call set_mode_i2c first to establish the pins for i2c operation.

        :param topic: message topic
        :param payload: {"command": "i2c_write", "pin": “PIN”, "tag": "TAG",
                         "addr": “I2C ADDRESS, "register": “I2C REGISTER”,
                         "data": [“DATA IN LIST FORM”]}
        """
        await self.esp.i2c_write(payload['addr'], payload['data'])

    async def pwm_write(self, topic, payload):
        """
        This method sets the pwm value for the selected pin.
        Call set_mode_pwm before calling this method.
        :param topic: message topic
        :param payload: {“command”: “pwm_write”, "pin": “PIN”,
                         "tag":”TAG”,
                          “value”: “VALUE”}
        """
        await self.esp.analog_write(payload["pin"], payload['value'])

    async def servo_position(self, topic, payload):
        """
        This method will set a servo's position in degrees.
        Call set_mode_servo first to activate the pin for
        servo operation.

        :param topic: message topic
        :param payload: {'command': 'servo_position',
                         "pin": “PIN”,'tag': 'servo',
                        “position”: “POSITION”}
        """
        await self.esp.servo_write(payload["pin"], payload["position"])

    async def set_mode_analog_input(self, topic, payload):
        """
        This method sets a GPIO pin as analog input.
        :param topic: message topic
        :param payload: {"command": "set_mode_analog_input", "pin": “PIN”, "tag":”TAG” }
        """
        pin = payload["pin"]
        await self.esp.set_pin_mode_analog_input(pin, callback=self.analog_input_callback)

    async def set_mode_digital_input(self, topic, payload):
        """
        This method sets a pin as digital input.
        :param topic: message topic
        :param payload: {"command": "set_mode_digital_input", "pin": “PIN”, "tag":”TAG” }
        """
        pin = payload["pin"]

        await self.esp.set_pin_mode_digital_input(pin, self.digital_input_callback)
        await asyncio.sleep(0.4)

    async def set_mode_digital_input_pullup(self, topic, payload):
        """
        This method sets a pin as digital input with pull up enabled.
        :param topic: message topic
        :param payload: message payload
        """
        pin = payload["pin"]

        await self.esp.set_pin_mode_digital_input_pullup(pin, self.digital_input_callback)

    async def set_mode_digital_output(self, topic, payload):
        """
        This method sets a pin as a digital output pin.
        :param topic: message topic
        :param payload: {"command": "set_mode_digital_output", "pin": PIN, "tag":”TAG” }
        """
        pin = payload["pin"]

        await self.esp.set_pin_mode_digital_output(pin)

    async def set_mode_i2c(self, topic, payload):
        """
        This method sets up the i2c pins for i2c operations.
        :param topic: message topic
        :param payload: {"command": "set_mode_i2c"}
        """
        # self.pins_dictionary[200][GatewayBaseAIO.PIN_MODE] = GatewayBaseAIO.I2C_MODE
        await self.esp.set_pin_mode_i2c()

    async def set_mode_pwm(self, topic, payload):
        """
        This method sets a GPIO pin capable of PWM for PWM operation.
        :param topic: message topic
        :param payload: {"command": "set_mode_pwm", "pin": “PIN”, "tag":”TAG” }
        """
        pin = payload["pin"]

        await self.esp.set_pin_mode_analog_output(pin)

    async def set_mode_servo(self, topic, payload):
        """
        This method establishes a GPIO pin for servo operation.
        :param topic: message topic
        :param payload: {"command": "set_mode_servo", "pin": “PIN”, "tag":”TAG” }
        """
        pin = payload["pin"]

        await self.esp.set_pin_mode_servo(pin)

    async def set_mode_sonar(self, topic, payload):
        """
        This method sets the trigger and echo pins for sonar operation.
        :param topic: message topic
        :param payload: {"command": "set_mode_sonar", "trigger_pin": “PIN”, "tag":”TAG”
                         "echo_pin": “PIN”"tag":”TAG” }
        """

        trigger = payload["trigger_pin"]
        echo = payload["echo_pin"]

        await self.esp.set_pin_mode_sonar(trigger, echo, self.sonar_callback)

    # Callbacks
    async def digital_input_callback(self, data):
        """
        Digital input data change reported by ESP
        :param data:
        :return:
        """
        payload = {'report': 'digital_input', 'pin': data[1],
                   'value': data[2], 'timestamp': data[3]}
        await self.publish_payload(payload, 'from_esp8266_gateway')

    async def analog_input_callback(self, data):
        payload = {'report': 'analog_input', 'pin': data[1],
                   'value': data[2], 'timestamp': data[3]}
        await self.publish_payload(payload, 'from_esp8266_gateway')

    async def i2c_callback(self, data):
        """
        Analog input data change reported by ESP

        :param data:
        :return:
        """
        # creat a string representation of the data returned
        report = ', '.join([str(elem) for elem in data])
        payload = {'report': 'i2c_data', 'value': report}
        await self.publish_payload(payload, 'from_esp8266_gateway')

    async def sonar_callback(self, data):
        """
        Sonar data change reported by ESP

        :param data:
        :return:
        """
        payload = {'report': 'sonar_data', 'value': data[2]}
        await self.publish_payload(payload, 'from_esp8266_gateway')


# noinspection DuplicatedCode
def esp8266_gateway():
    # allow user to bypass the IP address auto-discovery. This is necessary if the component resides on a computer
    # other than the computing running the backplane.

    parser = argparse.ArgumentParser()
    parser.add_argument("-b", dest="back_plane_ip_address", default="None",
                        help="None or IP address used by Back Plane")
    parser.add_argument("-c", dest="com_port", default="None",
                        help="Use this COM port instead of auto discovery")
    parser.add_argument("-m", dest="subscriber_list",
                        default="to_esp8266_gateway", nargs='+',
                        help="Banyan topics space delimited: topic1 topic2 topic3")
    parser.add_argument("-n", dest="process_name",
                        default="ESP8266Gateway", help="Set process name in "
                                                       "banner")
    parser.add_argument("-p", dest="publisher_port", default='43124',
                        help="Publisher IP port")
    parser.add_argument("-r", dest="publisher_topic",
                        default="from_rpi_gpio", help="Report topic")
    parser.add_argument("-s", dest="subscriber_port", default='43125',
                        help="Subscriber IP port")

    args = parser.parse_args()

    subscriber_list = args.subscriber_list

    kw_options = {
        'publisher_port': args.publisher_port,
        'subscriber_port': args.subscriber_port,
        'process_name': args.process_name,
    }
    if args.back_plane_ip_address != 'None':
        kw_options['back_plane_ip_address'] = args.back_plane_ip_address

    if args.com_port != 'None':
        kw_options['com_port'] = args.com_port

    # get the event loop
    # this is for python 3.8
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.get_event_loop()

    # replace with the name of your class
    app = Esp8266Gateway(subscriber_list, **kw_options, event_loop=loop)
    try:
        loop.run_until_complete(app.main())
    except (KeyboardInterrupt, asyncio.CancelledError, RuntimeError):
        loop.stop()
        loop.close()
        sys.exit(0)


# signal handler function called when Control-C occurs
# noinspection PyShadowingNames,PyUnusedLocal
def signal_handler(sig, frame):
    print('Exiting Through Signal Handler')
    raise KeyboardInterrupt


# listen for SIGINT
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    esp8266_gateway()
