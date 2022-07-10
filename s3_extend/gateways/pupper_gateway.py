"""
 This gateway translates messages received from the Pupper Scratch blocks
 and translates these messages into Pupper UDP packets and sends
 them to the Pupper robot.

 Copyright (c) 2022 Alan Yorinks All right reserved.

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
import signal
import socket
import sys
import time

from pupper_udp_packets import udp_packets
from python_banyan.banyan_base import BanyanBase


class PupperGateway(BanyanBase):

    def __init__(self, back_plane_ip_address=None, subscriber_port='43125',
                 publisher_port='43124', loop_time=.1, udp_port=8830):

        """
        kwargs is a dictionary that will contain the following keys:

        :param back_plane_ip_address: banyan_base back_planeIP Address -
                                    if not specified, it will be set to the
                                    local computer

        :param subscriber_port: banyan_base back plane subscriber port.
               This must match that of the banyan_base backplane

        :param publisher_port: banyan_base back plane publisher port.
                               This must match that of the
                               banyan_base backplane.

        :param process_name: Component identifier

        :param loop_time: receive loop sleep time

        """

        # save the input parameters
        self.back_plane_ip_address = back_plane_ip_address
        self.subscriber_port = subscriber_port
        self.publisher_port = publisher_port
        self.loop_time = loop_time
        self.udp_port = udp_port
        self.pupper_udp_address = None

        # initialize the parent
        super(PupperGateway, self).__init__(back_plane_ip_address=back_plane_ip_address,
                                            subscriber_port=subscriber_port,
                                            publisher_port=publisher_port,
                                            process_name='pupper_gateway v1.0',
                                            loop_time=loop_time)

        # allow zmq connections to establish
        time.sleep(.3)

        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_address = None

        # subscribe to the to_pup_gateway topic
        self.set_subscriber_topic('to_pup_gateway')
        # start the receive loop to accept messages from Scratch
        try:
            self.receive_loop()
        except KeyboardInterrupt:
            self.clean_up()
            sys.exit(0)

    def incoming_message_processing(self, topic, payload):
        """
        Messages are sent here from the receive_loop
        :param topic: Message Topic string
        :param payload: Message Data
        :return:
        """

        # if the UDP socket is not yet established look for udp ip address message
        # for all other messages at this point just toss them until connected.

        # retrieve the messages key/value pair
        for key, value in payload.items():
            if 'ipaddr' in key:
                if not self.sock_address:
                    self.sock_address = value, self.udp_port
                return
            else:
                # find command in the command table and send it to the robot

                # if the address was never set, just ignore the request
                if not self.sock_address:
                    return
                cmd = udp_packets[key][value].encode()
                sent = self.sock.sendto(cmd, self.sock_address)
                print(sent)


def echo_cmdline_client():
    parser = argparse.ArgumentParser()
    # allow user to bypass the IP address auto-discovery.
    # This is necessary if the component resides on a computer
    # other than the computing running the backplane.
    parser.add_argument("-b", dest="back_plane_ip_address", default="None",
                        help="None or IP address used by Back Plane")
    parser.add_argument("-m", dest="number_of_messages", default="10",
                        help="Number of messages to publish")
    # allow the user to specify a name for the component and have it shown on the console banner.
    # modify the default process name to one you wish to see on the banner.
    # change the default in the derived class to set the name
    parser.add_argument("-n", dest="process_name", default="EchoCmdClient",
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
    kw_options = {'back_plane_ip_address': args.back_plane_ip_address,
                  'publisher_port': args.publisher_port,
                  'subscriber_port': args.subscriber_port,
                  'udp_port': args.udp_port,
                  'loop_time': float(args.loop_time)}

    # replace with the name of your class
    EchoCmdClient(**kw_options)


# signal handler function called when Control-C occurs
# noinspection PyShadowingNames,PyUnusedLocal,PyUnusedLocal
def signal_handler(sig, frame):
    print('Exiting Through Signal Handler')
    raise KeyboardInterrupt


# listen for SIGINT
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# if __name__ == '__main__':
#     echo_cmdline_client()

z = PupperGateway()
print('zzz')
