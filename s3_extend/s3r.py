"""
 Copyright (c) 2019 Alan Yorinks All rights reserved.

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

import psutil
import signal
import subprocess
import sys
import time


# import webbrowser


class S3R:
    """
    This class starts the Banyan server to support the Scratch 3 OneGPIO Raspberry Pi
    extension for local mode. That means the browser and components are all executing
    on a single RPi.

    It will start the backplane, Raspberry Pi gateway and websocket gateway.
    """

    def __init__(self):

        # backplane status string
        # bp_string = ""
        self.backplane_exists = False
        self.proc_bp = None
        self.proc_agw = None
        self.proc_hwg = None

        print("Only run this script on a Raspberry Pi!")

        # checking running processes.
        # if the backplane is already running, just note that and move on.
        for pid in psutil.pids():
            p = psutil.Process(pid)
            if p.name() == "backplane":
                # new_entry['process_id'] = p
                # bp_string = "Backplane already running.          PID = " + str(p.pid)
                print("Backplane already running.          PID = " + str(p.pid))
                self.backplane_exists = True
            else:
                continue

        # if backplane is not already running, start a new instance
        if not self.backplane_exists:
            self.proc_bp = subprocess.Popen(['backplane'],
                                            stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                                            stdout=subprocess.PIPE)
            self.backplane_exists = True
            print('backplane started')
        if sys.platform.startswith('win32'):
            print('This must be run on a Raspberry Pi.')
            sys.exit(0)
        else:
            self.proc_awg = subprocess.Popen(['xterm', '-e', 'wsgw -i 9001'],
                                             stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                                             stdout=subprocess.PIPE)
            self.proc_hwg = subprocess.Popen(['xterm', '-e', 'rpigw'],
                                             stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                                             stdout=subprocess.PIPE)
        # webbrowser.open('https://mryslab.github.io/s3onegpio/')

        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                sys.exit(0)


def signal_handler(sig, frame):
    print('Exiting Through Signal Handler')
    raise KeyboardInterrupt


def s3rx():
    S3R()


# listen for SIGINT
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    # replace with name of function you defined above
    s3rx()
