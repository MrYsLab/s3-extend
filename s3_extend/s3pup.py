"""
 Copyright (c) 2022 Alan Yorinks All rights reserved.

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
import atexit
import signal
import subprocess
import sys
import time

import psutil


class S3PUP:
    """
    This class starts the Banyan server to support Scratch 3 OneGPIO
    for the Pupper Robot

    It will start the backplane, pupper gateway and websocket gateway.
    """

    def __init__(self, udp_port=None):
        """
        :param udp_port: Manually select udp port
        """

        self.udp_port = udp_port

        # psutil pids
        self.proc_bp = None
        self.proc_awg = None
        self.proc_hwg = None

        atexit.register(self.killall)
        self.skip_backplane = False

        # start backplane
        self.proc_bp = self.start_backplane()
        if self.proc_bp:
            print('backplane started')

        else:
            print('backplane start failed - exiting')
            sys.exit(0)

        self.proc_awg = self.start_wsgw()
        if self.proc_awg:
            print('Websocket Gateway started')
            time.sleep(1)
        else:
            print('WebSocket Gateway start failed - exiting')
            sys.exit(0)

        # start pupper gateway
        self.proc_hwg = self.start_pupgw()

        if self.proc_hwg:
            print('Pupper Gateway started ')
            print('To exit this program, press Control-c')
            time.sleep(1)

        else:
            print('Pupper Gateway start failed - exiting')
            sys.exit(0)

        while True:
            try:
                if not self.skip_backplane:
                    if self.proc_bp.poll() is not None:
                        self.proc_bp = None
                        print('backplane exited...')
                        self.killall()
                z = self.proc_awg.poll()
                if not z:
                    self.proc_awg = None
                    print('Websocket Gateway exited...')
                    self.killall()
                p = self.proc_hwg.poll
                # if self.proc_hwg.poll() is not None:
                if not p:
                    self.proc_hwg = None
                    print('pupper Gateway exited.')
                    self.killall()

                # allow some time between polls
                time.sleep(.4)
            except KeyboardInterrupt:
                self.killall()

    def killall(self):
        """
        Kill all running processes
        """
        # prevent loop from running for a clean exit
        # self.stop_event.set()
        # check for missing processes
        if self.proc_bp:
            try:
                if sys.platform.startswith('win32'):
                    subprocess.run(['taskkill', '/F', '/t', '/PID', str(self.proc_bp.pid)],
                                   creationflags=subprocess.CREATE_NEW_PROCESS_GROUP |
                                                 subprocess.CREATE_NO_WINDOW
                                   )
                else:
                    self.proc_bp.kill()
                self.proc_bp = None
            except:
                pass
        if self.proc_awg:
            try:
                if sys.platform.startswith('win32'):
                    subprocess.run(['taskkill', '/F', '/t', '/pid', str(self.proc_awg.pid)],
                                   creationflags=subprocess.CREATE_NEW_PROCESS_GROUP |
                                                 subprocess.CREATE_NO_WINDOW
                                   )
                else:
                    self.proc_awg.kill()
                self.proc_awg = None
            except:
                pass
        if self.proc_hwg:
            try:
                if sys.platform.startswith('win32'):
                    subprocess.run(['taskkill', '/F', '/t', '/PID', str(self.proc_hwg.pid)],
                                   creationflags=subprocess.CREATE_NEW_PROCESS_GROUP |
                                                 subprocess.CREATE_NO_WINDOW
                                   )
                else:
                    self.proc_hwg.kill()
                self.proc_hwg = None
            except:
                pass
        sys.exit(0)

    def start_backplane(self):
        """
        Start the backplane
        """

        # check to see if the backplane is already running
        try:
            for proc in psutil.process_iter(attrs=['pid', 'name']):
                if 'backplane' in proc.info['name']:
                    self.skip_backplane = True
                    # its running - return its pid
                    return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

        # backplane is not running, so start one
        if sys.platform.startswith('win32'):
            return subprocess.Popen(['backplane'],
                                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP |
                                                  subprocess.CREATE_NO_WINDOW)
        else:
            return subprocess.Popen(['backplane'],
                                    stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                                    stdout=subprocess.PIPE)

    def start_wsgw(self):
        """
        Start the websocket gateway
        """
        if sys.platform.startswith('win32'):
            return subprocess.Popen(['wsgw', '-i', '9004'],
                                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                                                  |
                                                  subprocess.CREATE_NO_WINDOW)
        else:
            return subprocess.Popen(['wsgw', '-i', '9004'],
                                    stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                                    stdout=subprocess.PIPE)

    def start_pupgw(self):
        """
        Start the pupper gateway
        """
        if sys.platform.startswith('win32'):
            hwgw_start = ['pupgw']
        else:
            hwgw_start = ['pupgw']

        if self.udp_port:
            hwgw_start.append('-u')
            hwgw_start.append(self.udp_port)

        if sys.platform.startswith('win32'):
            return subprocess.Popen(['pupgw'],
                                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP |
                                                            subprocess.CREATE_NO_WINDOW)
        else:
            return subprocess.Popen(['pupgw'], stdin=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    stdout=subprocess.PIPE)


def signal_handler(sig, frame):
    print('Exiting Through Signal Handler')
    raise KeyboardInterrupt


def s3pupx():
    """
     Start the s3p script
     """
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", dest="udp_port", default="None",
                        help="Use this UDP port instead of default of 8830")

    args = parser.parse_args()

    if args.udp_port == "None":
        udp_port = 8830
    else:
        udp_port = int(args.udp_port)

    S3PUP(udp_port=udp_port)


# listen for SIGINT
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    # replace with name of function you defined above
    s3pupx()
