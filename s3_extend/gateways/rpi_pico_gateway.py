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
import logging
import pathlib
import signal
import sys
from python_banyan.gateway_base_aio import GatewayBaseAIO
from tmx_pico_aio import tmx_pico_aio


# noinspection PyAbstractClass,PyMethodMayBeStatic,PyRedundantParentheses,DuplicatedCode,GrazieInspection
class RpiPicoGateway(GatewayBaseAIO):
    # This class implements the GatewayBase interface adapted for asyncio.
    # It supports the Raspberry Pi Pico.

    # NOTE: This class requires the use of Python 3.8 or above

    def __init__(self, *subscriber_list, back_plane_ip_address=None,
                 subscriber_port='43125',
                 publisher_port='43124', process_name='RpiPicoGateway',
                 event_loop=None, com_port=None,
                 log=False):
        """
        Set up the gateway for operation

        :param subscriber_list: a tuple or list of subscription topics.
        :param back_plane_ip_address: ip address of backplane or none if local
        :param subscriber_port: backplane subscriber port
        :param publisher_port: backplane publisher port
        :param process_name: name to display on the console
        :param event_loop: optional parameter to pass in an asyncio
                           event loop
        :param com_port: force pymata-express to use this comport
        :param log: enable logging
        """

        # set up logging if requested
        self.log = log
        if self.log:
            fn = str(pathlib.Path.home()) + "/rpi_pico_gw.log"
            self.logger = logging.getLogger(__name__)
            logging.basicConfig(filename=fn, filemode='w', level=logging.DEBUG)
            sys.excepthook = self.my_handler

        # set the event loop to be used. accept user's if provided
        self.event_loop = event_loop
        self.com_port = com_port

        # instantiate tmx-pico-aio that controls the Pico board
        # if user want to pass in a com port, then pass it in
        try:
            self.pico = tmx_pico_aio.TmxPicoAio(loop=self.event_loop,
                                   com_port=com_port)
        except RuntimeError:
            if self.log:
                logging.exception("Exception occurred", exc_info=True)
            raise

        # Initialize the parent
        super(RpiPicoGateway, self).__init__(subscriber_list=subscriber_list,
                                             event_loop=self.event_loop,
                                             back_plane_ip_address=back_plane_ip_address,
                                             subscriber_port=subscriber_port,
                                             publisher_port=publisher_port,
                                             process_name=process_name,
                                             )

    def init_pins_dictionary(self):
        """
        This method will initialize the pins dictionary contained
        in gateway base parent class. This method is called by
        the gateway base parent in its init method.

        NOTE: that this a non-asyncio method.
        """
        pass  # not used for this gateway

    async def main(self):
        # call the inherited begin method located in banyan_base_aio
        await self.begin()

        # sit in an endless loop to receive protocol messages
        while True:
            await self.receive_loop()

    # The following methods and are called
    # by the gateway base class in its incoming_message_processing
    # method. They overwrite the default methods in the gateway_base.

    async def digital_write(self, topic, payload):
        """
        This method performs a digital write
        :param topic: message topic
        :param payload: {"command": "digital_write", "pin": “PIN”, "value": “VALUE”}
        """
        await self.pico.digital_write(payload["pin"], payload['value'])

    async def disable_analog_reporting(self, topic, payload):
        """
        This method disables analog input reporting for the selected pin.
        :param topic: message topic
        :param payload: {"command": "disable_analog_reporting", "pin": “PINset_mode_digital_output”, "tag": "TAG"}
        """
        await self.pico.disable_analog_reporting(payload["pin"])

    async def disable_digital_reporting(self, topic, payload):
        """
        This method disables digital input reporting for the selected pin.

        :param topic: message topic
        :param payload: {"command": "disable_digital_reporting", "pin": “PIN”, "tag": "TAG"}
        """
        await self.pico.disable_digital_reporting(payload["pin"])

    async def enable_analog_reporting(self, topic, payload):
        """
        This method enables analog input reporting for the selected pin.
        :param topic: message topic
        :param payload:  {"command": "enable_analog_reporting", "pin": “PIN”, "tag": "TAG"}
        """
        await self.pico.enable_analog_reporting(payload["pin"])

    async def enable_digital_reporting(self, topic, payload):
        """
        This method enables digital input reporting for the selected pin.
        :param topic: message topic
        :param payload: {"command": "enable_digital_reporting", "pin": “PIN”, "tag": "TAG"}
        """
        await self.pico.enable_digital_reporting(payload["pin"])

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

        await self.pico.i2c_read(payload['addr'],
                                 payload['register'],
                                 payload['number_of_bytes'],
                                 callback=self.i2c_callback)

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
        await self.pico.i2c_write(payload['addr'], payload['data'])

    async def play_tone(self, topic, payload):
        """
        This method plays a tone on a piezo device connected to the selected
        pin at the frequency and duration requested.
        Frequency is in hz and duration in milliseconds.

        Call set_mode_tone before using this method.
        :param topic: message topic
        :param payload: {"command": "play_tone", "pin": “PIN”, "tag": "TAG",
                         “freq”: ”FREQUENCY”, duration: “DURATION”}
        """
        raise NotImplementedError

    async def pwm_write(self, topic, payload):
        """
        This method sets the pwm value for the selected pin.
        Call set_mode_pwm before calling this method.
        :param topic: message topic
        :param payload: {“command”: “pwm_write”, "pin": “PIN”,
                         "tag":”TAG”,
                          “value”: “VALUE”}
        """
        await self.pico.pwm_write(payload['pin'], payload['value'])

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
        await self.pico.servo_write(payload["pin"], payload["position"])

    async def set_mode_analog_input(self, topic, payload):
        """
        This method sets a GPIO pin as analog input.
        :param topic: message topic
        :param payload: {"command": "set_mode_analog_input", "pin": “PIN”, "tag":”TAG” }
        """
        pin = payload["pin"]
        # self.pins_dictionary[pin + self.first_analog_pin][GatewayBaseAIO.PIN_MODE] = \
        #     GatewayBaseAIO.ANALOG_INPUT_MODE
        await self.pico.set_pin_mode_analog_input(pin,
                                                  callback=self.analog_input_callback)

    async def set_mode_digital_input(self, topic, payload):
        """
        This method sets a pin as digital input.
        :param topic: message topic
        :param payload: {"command": "set_mode_digital_input", "pin": “PIN”, "tag":”TAG” }
        """
        pin = payload["pin"]
        pull = payload["pull"]
        # self.pins_dictionary[pin][
        #     GatewayBaseAIO.PIN_MODE] = GatewayBaseAIO.DIGITAL_INPUT_MODE
        if pull == '^':
            await self.pico.set_pin_mode_digital_input_pullup(pin,
                                                   callback=self.digital_input_callback)
        else:
            await self.pico.set_pin_mode_digital_input(pin,
                                                              callback=self.digital_input_callback)

    async def set_mode_digital_input_pullup(self, topic, payload):
        """
        This method sets a pin as digital input with pull up enabled.
        :param topic: message topic
        :param payload: message payload
        """
        pin = payload["pin"]
        # self.pins_dictionary[pin][
        #     GatewayBaseAIO.PIN_MODE] = GatewayBaseAIO.DIGITAL_INPUT_PULLUP_MODE
        await self.pico.set_pin_mode_digital_input_pullup(pin,
                                                          callback=self.digital_input_callback)

    async def set_mode_digital_output(self, topic, payload):
        """
        This method sets a pin as a digital output pin.
        :param topic: message topic
        :param payload: {"command": "set_mode_digital_output", "pin": PIN, "tag":”TAG” }
        """
        pin = payload["pin"]
        # self.pins_dictionary[pin][
        #     GatewayBaseAIO.PIN_MODE] = GatewayBaseAIO.DIGITAL_OUTPUT_MODE
        await self.pico.set_pin_mode_digital_output(pin)

    async def set_mode_i2c(self, topic, payload):
        """
        This method sets up the i2c pins for i2c operations.
        :param topic: message topic
        :param payload: {"command": "set_mode_i2c"}
        """
        # self.pins_dictionary[200][GatewayBaseAIO.PIN_MODE] = GatewayBaseAIO.I2C_MODE
        await self.pico.set_pin_mode_i2c()

    async def set_mode_pwm(self, topic, payload):
        """
        This method sets a GPIO pin capable of PWM for PWM operation.
        :param topic: message topic
        :param payload: {"command": "set_mode_pwm", "pin": “PIN”, "tag":”TAG” }
        """
        pin = payload["pin"]
        # self.pins_dictionary[pin][
        #     GatewayBaseAIO.PIN_MODE] = GatewayBaseAIO.PWM_OUTPUT_MODE
        await self.pico.set_pin_mode_pwm_output(pin)

    async def set_mode_servo(self, topic, payload):
        """
        This method establishes a GPIO pin for servo operation.
        :param topic: message topic
        :param payload: {"command": "set_mode_servo", "pin": “PIN”, "tag":”TAG” }
        """
        pin = payload["pin"]
        # self.pins_dictionary[pin][GatewayBaseAIO.PIN_MODE] = GatewayBaseAIO.SERVO_MODE
        await self.pico.set_pin_mode_servo(pin, min_pulse=300, max_pulse=1900)

    async def set_mode_sonar(self, topic, payload):
        """
        This method sets the trigger and echo pins for sonar operation.
        :param topic: message topic
        :param payload: {"command": "set_mode_sonar", "trigger_pin": “PIN”, "tag":”TAG”
                         "echo_pin": “PIN”"tag":”TAG” }
        """

        trigger = payload["trigger_pin"]
        echo = payload["echo_pin"]
        # self.pins_dictionary[trigger][GatewayBaseAIO.PIN_MODE] =
        # GatewayBaseAIO.SONAR_MODE
        # self.pins_dictionary[echo][GatewayBaseAIO.PIN_MODE] = GatewayBaseAIO.SONAR_MODE

        await self.pico.set_pin_mode_sonar(trigger, echo, callback=self.sonar_callback)

    async def set_mode_stepper(self, topic, payload):
        """
        This method establishes either 2 or 4 GPIO pins to be used in stepper
        motor operation.
        :param topic:
        :param payload:{"command": "set_mode_stepper", "pins": [“PINS”],
                        "steps_per_revolution": “NUMBER OF STEPS”}
        """
        raise NotImplementedError

    async def set_mode_tone(self, topic, payload):
        """
        Establish a GPIO pin for tone operation.
        :param topic:
        :param payload:{"command": "set_mode_tone", "pin": “PIN”, "tag":”TAG” }
        """
        raise NotImplementedError

    async def stepper_write(self, topic, payload):
        """
        Move a stepper motor for the specified number of steps.
        :param topic:
        :param payload: {"command": "stepper_write", "motor_speed": “SPEED”,
                         "number_of_steps":”NUMBER OF STEPS” }
        """
        raise NotImplementedError

    # Callbacks
    async def digital_input_callback(self, data):
        """
        Digital input data change reported by the Pico
        :param data:
        :return:
        """
        # data = [pin mode, pin, current reported value, timestamp]
        # self.pins_dictionary[data[1]][GatewayBaseAIO.LAST_VALUE] = data[2]
        payload = {'report': 'digital_input', 'pin': data[1],
                   'value': data[2], 'timestamp': data[3]}
        await self.publish_payload(payload, 'from_rpi_pico_gateway')

    async def analog_input_callback(self, data):
        payload = {'report': 'analog_input', 'pin': data[1],
                   'value': data[2], 'timestamp': data[3]}
        await self.publish_payload(payload, 'from_rpi_pico_gateway')

    async def i2c_callback(self, data):
        """
        Analog input data change reported by the Pico

        :param data:
        :return:
        """
        # creat a string representation of the data returned
        # self.pins_dictionary[200] = data[1]
        report = ', '.join([str(elem) for elem in data])
        payload = {'report': 'i2c_data', 'value': report}
        await self.publish_payload(payload, 'from_rpi_pico_gateway')

    async def sonar_callback(self, data):
        """
        Sonar data change reported by the Pico

        :param data:
        :return:
        """
        # self.pins_dictionary[data[1]][GatewayBaseAIO.LAST_VALUE] = data[2]
        payload = {'report': 'sonar_data', 'value': data[2]}
        await self.publish_payload(payload, 'from_rpi_pico_gateway')

    def my_handler(self, tp, value, tb):
        """
        for logging uncaught exceptions
        :param tp:
        :param value:
        :param tb:
        :return:
        """
        self.logger.exception("Uncaught exception: {0}".format(str(value)))


# noinspection DuplicatedCode
def rpi_pico_gateway():
    # allow user to bypass the IP address auto-discovery. This is necessary if the component resides on a computer
    # other than the computing running the backplane.

    parser = argparse.ArgumentParser()
    parser.add_argument("-b", dest="back_plane_ip_address", default="None",
                        help="None or IP address used by Back Plane")
    parser.add_argument("-c", dest="com_port", default="None",
                        help="Use this COM port instead of auto discovery")
    parser.add_argument("-l", dest="log", default="False",
                        help="Set to True to turn logging on.")
    parser.add_argument("-m", dest="subscriber_list",
                        default="to_rpi_pico_gateway", nargs='+',
                        help="Banyan topics space delimited: topic1 topic2 topic3")
    parser.add_argument("-n", dest="process_name",
                        default="RpiPicoGateway", help="Set process name in "
                                                       "banner")
    parser.add_argument("-p", dest="publisher_port", default='43124',
                        help="Publisher IP port")
    parser.add_argument("-r", dest="publisher_topic",
                        default="from_rpi_pico_gpio", help="Report topic")
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
    app = RpiPicoGateway(subscriber_list, **kw_options, event_loop=loop)
    try:
        loop.run_until_complete(app.main())
    except (KeyboardInterrupt, asyncio.CancelledError, RuntimeError):
        if app.log:
            logging.exception("Exception occurred", exc_info=True)
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
    rpi_pico_gateway()
