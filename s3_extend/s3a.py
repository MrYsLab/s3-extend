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
import psutil
import signal
import subprocess
import sys
import time
# import webbrowser


class S3A:
    """
    This class starts the Banyan server to support the Scratch 3 OneGPIO Arduino
    extension.

    It will start the backplane, arduino gateway and websocket gateway.
    """

    def __init__(self, com_port=None, arduino_instance_id=None, log=None):
        self.backplane_exists = False
        self.proc_bp = None
        self.proc_agw = None
        self.proc_hwg = None

        # checking running processes.
        # if the backplane is already running, just note that and move on.
        for pid in psutil.pids():
            p = psutil.Process(pid)
            if p.name() == "backplane":
                print("Backplane already running.          PID = " + str(p.pid))
                self.backplane_exists = True
            else:
                continue

        # if backplane is not already running, start a new instance
        if not self.backplane_exists:
            self.proc_bp = subprocess.Popen(['backplane'],
                                            stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                                            stdout=subprocess.PIPE)
            # new_entry['process'] = self.proc
            # new_entry['process_id'] = self.proc.pid
            self.backplane_exists = True
            print('Backplane is now running')

        if sys.platform.startswith('win32'):
            wsgw_start = ['wsgw']
            ardgw_start = ['ardgw']
        else:
            wsgw_start = ['xterm', '-e', 'wsgw']
            ardgw_start = ['xterm', '-e', 'ardgw']

        if log:
            wsgw_start.append('-l')
            wsgw_start.append('True')
            ardgw_start.append('-l')
            ardgw_start.append('True')
        if com_port:
            ardgw_start.append('-c')
            ardgw_start.append(com_port)
        if arduino_instance_id:
            ardgw_start.append('-i')
            ardgw_start.append(arduino_instance_id)





        if sys.platform.startswith('win32'):
            self.proc_agw = subprocess.Popen(wsgw_start,
                                             creationflags=subprocess.CREATE_NEW_CONSOLE)
            self.proc_hwg = subprocess.Popen(ardgw_start,
                                             creationflags=subprocess.CREATE_NEW_CONSOLE)

        else:
            self.proc_awg = subprocess.Popen(wsgw_start,
                                                 stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                                                 stdout=subprocess.PIPE)

            self.proc_hwg = subprocess.Popen(ardgw_start,
                                             stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                                             stdout=subprocess.PIPE)

        # webbrowser.open('https://mryslab.github.io/s3onegpio/', new=1)

        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                self.proc_awg.kill()
                self.proc_hwg.kill()
                sys.exit(0)

def signal_handler(sig, frame):
    print('Exiting Through Signal Handler')
    raise KeyboardInterrupt


def s3ax():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", dest="com_port", default="None",
                        help="Use this COM port instead of auto discovery")
    parser.add_argument("-i", dest="arduino_instance_id", default="None",
                        help="Set an Arduino Instance ID and match it in FirmataExpress")
    parser.add_argument("-l", dest="log", default="False",
                        help="Set to True to turn logging on.")

    args = parser.parse_args()

    log = args.log.lower()
    if log == 'false':
        log = False
    else:
        log = True

    if args.com_port == "None":
        com_port = None
    else:
        com_port=args.com_port

    if args.arduino_instance_id == "None":
        arduino_instance_id = None
    else:
        arduino_instance_id = int(args.arduino_instance_id)

    if com_port and arduino_instance_id:
        raise RuntimeError('Both com_port arduino_instance_id were set. Only one is allowed')

    S3A(com_port=com_port, arduino_instance_id=args.arduino_instance_id, log=log)


# listen for SIGINT
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    # replace with name of function you defined above
    s3ax()
