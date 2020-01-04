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
import argparse
import atexit
import signal
import subprocess
import sys
import time

import psutil


# import webbrowser


class S3P:
    """
    This class starts the Banyan server to support Scratch 3 OneGPIO
    for the Picoboard

    It will start the backplane, picoboard gateway and websocket gateway.
    """

    def __init__(self, com_port=None):
        """
        :param com_port: Manually select serial com port
        """

        self.com_port = com_port

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
        else:
            print('WebSocket Gateway start failed - exiting')
            sys.exit(0)

        # start picoboard gateway
        self.proc_hwg = self.start_pbgw()
        if self.proc_hwg:
            print('Picoboard Gateway started ')
            print('To exit this program, press Control-c')

        else:
            print('Picobard Gateway start failed - exiting')
            sys.exit(0)

        # webbrowser.open('https://mryslab.github.io/s3onegpio/', new=1)

        while True:
            try:
                if not self.skip_backplane:
                    if self.proc_bp.poll() is not None:
                        self.proc_bp = None
                        print('backplane exited...')
                        self.killall()
                if self.proc_awg.poll() is not None:
                    self.proc_awg = None
                    print('Websocket Gateway exited...')
                    self.killall()
                if self.proc_hwg.poll() is not None:
                    self.proc_hwg = None
                    print('Picoboard Gateway exited. Is your Picoboard plugged in?')
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

    def start_pbgw(self):
        """
        Start the picoboard gateway
        """
        if sys.platform.startswith('win32'):
            return subprocess.Popen(['pbgw'], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP |
                                                            subprocess.CREATE_NO_WINDOW)
        else:
            return subprocess.Popen(['pbgw'], stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                                    stdout=subprocess.PIPE)


def signal_handler(sig, frame):
    print('Exiting Through Signal Handler')
    raise KeyboardInterrupt


def s3px():
    """
     Start the s3p script
     """
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", dest="com_port", default="None",
                        help="Use this COM port instead of auto discovery")

    args = parser.parse_args()

    if args.com_port == "None":
        com_port = None
    else:
        com_port = args.com_port

    S3P(com_port=com_port)


# listen for SIGINT
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    # replace with name of function you defined above
    s3px()
