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
    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, "
"'L1': True, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, "
"'triangle': False, 'message_rate': 20,}"

deactivate = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, "
"'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, "
"'triangle': False, 'message_rate': 20,}"

rest = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, "
"'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, "
"'triangle': False, 'message_rate': 20,}"

trot = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': True, "
"'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, "
"'triangle': False, 'message_rate': 20,}"

raise_body = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, "
"'L1': False, 'dpady': 1, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, "
"'triangle': False, 'message_rate': 20,}"

lower_body = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, "
"'L1': False, 'dpady': -1, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, "
"'triangle': False, 'message_rate': 20,}"

roll_body_left = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, "
"'L1': False, 'dpady': 0, 'dpadx': -1, 'x': False, 'square': False, 'circle': False, "
"'triangle': False, 'message_rate': 20,}"

roll_body_right = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, "
"'L1': False, 'dpady': 0, 'dpadx': 1, 'x': False, 'square': False, 'circle': False, "
"'triangle': False, 'message_rate': 20,}"

move_forward_fast = \
    "{'ly': 1.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, "
"'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, "
"'triangle': False, 'message_rate': 20,}"

move_forward_slow = \
    "{'ly': 0.5, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, "
"'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, "
"'triangle': False, 'message_rate': 20,}"

move_back_fast = \
    "{'ly': -1.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, 'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, 'triangle': False, 'message_rate': 20,}"

move_back_slow = \
    "{'ly': -0.5, 'lx': 0.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, 'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, 'triangle': False, 'message_rate': 20,}"

move_left_fast = \
    "{'ly': 0.0, 'lx': -1.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, "
"'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, "
"'triangle': False, 'message_rate': 20,}"

move_left_slow = \
    "{'ly': 0.0, 'lx': -0.5, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, "
"'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, "
"'triangle': False, 'message_rate': 20,}"

move_right_fast = \
    "{'ly': 0.0, 'lx': 1.0, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, "
"'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, "
"'triangle': False, 'message_rate': 20,}"

move_right_slow = \
    "{'ly': 0.0, 'lx': 0.5, 'rx': 0.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, "
"'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, "
"'triangle': False, 'message_rate': 20,}"

yaw_left_mid = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': -0.5, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, "
"'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, "
"'triangle': False, 'message_rate': 20,}"

yaw_left_max = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': -1.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, "
"'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, "
"'triangle': False, 'message_rate': 20,}"

yaw_right_mid = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.5, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, "
"'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, "
"'triangle': False, 'message_rate': 20,}"

yaw_right_max = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': 1.0, 'ry': 0.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, "
"'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, "
"'triangle': False, 'message_rate': 20,}"

pitch_down_mid = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': -0.5, 'L2': -1.0, 'R2': -1.0, 'R1': False, "
"'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, "
"'triangle': False, 'message_rate': 20,}"

pitch_down_max = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': -1.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, "
"'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, "
"'triangle': False, 'message_rate': 20,}"

pitch_up_mid = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 0.5, 'L2': -1.0, 'R2': -1.0, 'R1': False, "
"'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, "
"'triangle': False, 'message_rate': 20,}"

pitch_up_max = \
    "{'ly': 0.0, 'lx': 0.0, 'rx': 0.0, 'ry': 1.0, 'L2': -1.0, 'R2': -1.0, 'R1': False, "
"'L1': False, 'dpady': 0, 'dpadx': 0, 'x': False, 'square': False, 'circle': False, "
"'triangle': False, 'message_rate': 20,}"

udp_packets = {'activate_mode': [activate, deactivate],
               'rest_trot_mode': [rest, trot],
               'raise_body_mode': [raise_body, lower_body],
               'roll_body': [roll_body_left, roll_body_right],
               'motion_mode': [move_forward_fast, move_forward_slow, move_back_fast, move_back_slow],
               'turn_mode': [move_left_fast, move_left_slow, move_right_fast, move_right_slow],
               'yaw_mode': [yaw_left_mid, yaw_left_max, yaw_right_mid, yaw_right_max],
               'pitch_mode': [pitch_down_mid, pitch_down_max, pitch_up_mid, pitch_up_max],
               }
