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
import msgpack
import socket
import sys
import time

# from pupper_udp_packets import udp_packets
from python_banyan.banyan_base import BanyanBase

"""
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
# udp_packets is a Python dictionary that is used to map the command message
# sent by the WebSocket gateway to the actual UDP packet required by the pupper.

# There is a key value for each Scratch block:
#   activate_mode, rest_trot_mode, raise_body_mode, roll_body mode,
#   motion_mode, turn_mode, yaw_mode, pitch mode

# The associated value for each key is an array of UDP frames.

activate = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, 'L1': True, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, 'triangle': False, 'message_rate': 20,}" \

deactivate = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, 'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, 'triangle': False, 'message_rate': 20,}"

rest = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False,'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, 'triangle': False, 'message_rate': 20,}"

trot = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': True, 'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, 'triangle': False, 'message_rate': 20,}"

raise_body = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, 'L1': False, 'dpady': 1, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, 'triangle': False, 'message_rate': 20,}"

lower_body = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, 'L1': False, 'dpady': -1, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, 'triangle': False, 'message_rate': 20,}"

roll_body_left = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, 'L1': False, 'dpady': 0, 'dpadx': -1, 'x': False, 'square': False, 'circle': False, 'triangle': False, 'message_rate': 20,}"

roll_body_right = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, 'L1': False, 'dpady': 0, 'dpadx': 1, 'x': False, 'square': False, 'circle': False, 'triangle': False, 'message_rate': 20,}"

move_forward_fast = \
    "{'ly': 1.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, 'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, 'triangle': False, 'message_rate': 20,}"

move_forward_slow = \
    "{'ly': 0.5, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, 'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, 'triangle': False, 'message_rate': 20,}"

move_back_fast = \
    "{'ly': -1.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, 'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, 'triangle': False, 'message_rate': 20,}"

move_back_slow = \
    "{'ly': -0.5, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, 'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, 'triangle': False, 'message_rate': 20,}"

move_left_fast = \
    "{'ly': 0.0, 'lx': -1.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, 'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, 'triangle': False, 'message_rate': 20,}"

move_left_slow = \
    "{'ly': 0.0, 'lx': -0.5, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, 'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, 'triangle': False, 'message_rate': 20,}"

move_right_fast = \
    "{'ly': 0.0, 'lx': 1.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, 'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, 'triangle': False, 'message_rate': 20,}"

move_right_slow = \
    "{'ly': 0.0, 'lx': 0.5, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, 'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, 'triangle': False, 'message_rate': 20,}"

yaw_left_mid = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': -0.5, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, 'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, 'triangle': False, 'message_rate': 20,}"

yaw_left_max = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': -1.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, 'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, 'triangle': False, 'message_rate': 20,}"

yaw_right_mid = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.5, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, 'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, 'triangle': False, 'message_rate': 20,}"

yaw_right_max = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': 1.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, 'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, 'triangle': False, 'message_rate': 20,}"

pitch_down_mid = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': -0.5, 'L2': -1.0, 'R2': -1.0, 'R1': False, 'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, 'triangle': False, 'message_rate': 20,}"

pitch_down_max = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': -1.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, 'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, 'triangle': False, 'message_rate': 20,}"

pitch_up_mid = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.5, 'L2': -1.0, 'R2': -1.0, 'R1': False, 'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, 'triangle': False, 'message_rate': 20,}"

pitch_up_max = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 1.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, 'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, 'triangle': False, 'message_rate': 20,}"

udp_packets = {'activate_mode': [activate, deactivate],
               'rest_trot_mode': [rest, trot],
               'raise_body_mode': [raise_body, lower_body],
               'roll_body_mode': [roll_body_left, roll_body_right],
               'motion_mode': [move_forward_fast, move_forward_slow, move_back_fast,
                               move_back_slow],
               'turn_mode': [move_left_fast, move_left_slow, move_right_fast,
                             move_right_slow],
               'yaw_mode': [yaw_left_mid, yaw_left_max, yaw_right_mid, yaw_right_max],
               'pitch_mode': [pitch_down_mid, pitch_down_max, pitch_up_mid, pitch_up_max],
               }


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
        time.sleep(1)

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
                cmd = udp_packets[key][value]
                message = msgpack.packb(cmd, use_bin_type=True)

                # cmd = udp_packets[key][value].encode()
                sent = self.sock.sendto(message, self.sock_address)
                print(sent)


def pupper_gateway():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", dest="back_plane_ip_address", default="None",
                        help="None or IP address used by Back Plane")
    parser.add_argument("-p", dest="publisher_port", default='43124',
                        help="Publisher IP port")
    parser.add_argument("-s", dest="subscriber_port", default='43125',
                        help="Subscriber IP port")
    parser.add_argument("-t", dest="loop_time", default=".1",
                        help="Event Loop Timer in seconds")
    parser.add_argument("-u", dest="udp_port", default='8830',
                        help="UDP port number")

    args = parser.parse_args()

    if args.back_plane_ip_address == 'None':
        args.back_plane_ip_address = None
    kw_options = {'back_plane_ip_address': args.back_plane_ip_address,
                  'publisher_port': args.publisher_port,
                  'subscriber_port': args.subscriber_port,
                  'udp_port': int(args.udp_port),
                  'loop_time': float(args.loop_time)}

    # replace with the name of your class
    PupperGateway(**kw_options)


# signal handler function called when Control-C occurs
# noinspection PyShadowingNames,PyUnusedLocal,PyUnusedLocal
def signal_handler(sig, frame):
    print('Exiting Through Signal Handler')
    raise KeyboardInterrupt


# listen for SIGINT
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    pupper_gateway()
