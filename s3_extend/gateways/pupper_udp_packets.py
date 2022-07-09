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
# udp_packets is a Python dictionary that is used to map the command message
# sent by the WebSocket gateway to the actual UDP packet required by the pupper.

# There is a key value for each Scratch block:
#   activate_mode, rest_trot_mode, raise_body_mode, roll_body mode,
#   motion_mode, turn_mode, yaw_mode, pitch mode

# The associated value for each key is an array of UDP frames.


udp_packets = {'activate_mode': [
    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, "
    "'L1': True, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False,"
    "'triangle': False, 'message_rate': 20,}",

    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, "
    "'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False,"
    "'triangle': False, 'message_rate': 20,}"],

    'rest_trot_mode': [
        "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, "
        "'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': "
        "False,"
        "'triangle': False, 'message_rate': 20,}",

        "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, "
        "'R1': True, "
        "'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False,"
        "'triangle': False, 'message_rate': 20,}"],

    'raise_body_mode': ["{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, "
                        "'R2': -1.0, 'R1': False, "
                        "'L1': False, 'dpady': 1, 'dpadx': 0, 'x': False, 'square': False, 'circle': "
                        "False,"
                        "'triangle': False, 'message_rate': 20,}",

                        "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, "
                        "'R1': False, "
                        "'L1': False, 'dpady': -1, 'dpadx': 0, 'x': False, 'square': False, 'circle': "
                        "False,"
                        "'triangle': False, 'message_rate': 20,}"],

    'roll_body': ["{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, "
                  "'R2': -1.0, 'R1': False, "
                  "'L1': False, 'dpady': 0, 'dpadx': -1, 'x': False, 'square': False, 'circle': "
                  "False,"
                  "'triangle': False, 'message_rate': 20,}",

                  "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, "
                  "'R1': False, "
                  "'L1': False, 'dpady': 0, 'dpadx': 1, 'x': False, 'square': False, 'circle': "
                  "False,"
                  "'triangle': False, 'message_rate': 20,}"],

    'motion_mode': ["{'ly': 1.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, "
                    "'R2': -1.0, 'R1': False, "
                    "'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': "
                    "False,"
                    "'triangle': False, 'message_rate': 20,}",

                    "{'ly': 0.5, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, "
                    "'R1': False, "
                    "'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': "
                    "False,"
                    "'triangle': False, 'message_rate': 20,}",

                    "{'ly': -1.0, 'lx': -0.5, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, "
                    "'R2': -1.0, 'R1': False, "
                    "'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': "
                    "False,"
                    "'triangle': False, 'message_rate': 20,}",

                    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, "
                    "'R1': False, "
                    "'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': "
                    "False,"
                    "'triangle': False, 'message_rate': 20,}"],

    'turn_mode': ["{'ly': 0.0, 'lx': -1.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, "
                  "'R2': -1.0, 'R1': False, "
                  "'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': "
                  "False,"
                  "'triangle': False, 'message_rate': 20,}",

                  "{'ly': 0.0, 'lx': -0.5, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, "
                  "'R1': False, "
                  "'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': "
                  "False,"
                  "'triangle': False, 'message_rate': 20,}",

                  "{'ly': -1.0, 'lx': 1.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, "
                  "'R2': -1.0, 'R1': False, "
                  "'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': "
                  "False,"
                  "'triangle': False, 'message_rate': 20,}",

                  "{'ly': 0.0, 'lx': -0.5, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, "
                  "'R1': False, "
                  "'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': "
                  "False,"
                  "'triangle': False, 'message_rate': 20,}"],

    'yaw_mode': ["{'ly': 0.0, 'lx': -0.0, 'rx': -0.5, 'ry': 0.0, 'L2': -1.0, "
                 "'R2': -1.0, 'R1': False, "
                 "'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': "
                 "False,"
                 "'triangle': False, 'message_rate': 20,}",

                 "{'ly': 0.0, 'lx': 0.0, 'rx': -1.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, "
                 "'R1': False, "
                 "'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': "
                 "False,"
                 "'triangle': False, 'message_rate': 20,}",

                 "{'ly': -1.0, 'lx': 0.0, 'rx': 0.5, 'ry': 0.0, 'L2': -1.0, "
                 "'R2': -1.0, 'R1': False, "
                 "'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': "
                 "False,"
                 "'triangle': False, 'message_rate': 20,}",

                 "{'ly': 0.0, 'lx': 0.0, 'rx': 1.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, "
                 "'R1': False, "
                 "'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': "
                 "False,"
                 "'triangle': False, 'message_rate': 20,}"],
    'pitch_mode': ["{'ly': 0.0, 'lx': -0.0, 'rx': 0.0, 'ry': -0.5, 'L2': -1.0, "
                   "'R2': -1.0, 'R1': False, "
                   "'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': "
                   "False,"
                   "'triangle': False, 'message_rate': 20,}",

                   "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': -1.0, 'L2': -1.0, 'R2': -1.0, "
                   "'R1': False, "
                   "'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': "
                   "False,"
                   "'triangle': False, 'message_rate': 20,}",

                   "{'ly': -1.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.5, 'L2': -1.0, "
                   "'R2': -1.0, 'R1': False, "
                   "'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': "
                   "False,"
                   "'triangle': False, 'message_rate': 20,}",

                   "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 1.0, 'L2': -1.0, 'R2': -1.0, "
                   "'R1': False, "
                   "'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': "
                   "False,"
                   "'triangle': False, 'message_rate': 20,}"],
}
