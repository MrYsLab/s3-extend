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
import threading
import time


# import webbrowser


class S3P(threading.Thread):
    """
    This class starts the Banyan server to support Scratch 3 OneGPIO
    for the Picoboard

    It will start the backplane, picoboard gateway and websocket gateway.
    """

    def __init__(self, com_port=None, log=None):
        """
        :param com_port: Manually select serial com port
        :param log: log unhandled exceptions.
        """

        self.com_port = com_port
        self.log = log

        self.backplane_exists = False

        # pids of processes
        self.proc_bp = None
        self.proc_awg = None
        self.proc_hwg = None

        # start backplane
        self.start_backplane()

        # start the websocket gateway
        self.start_wsgw()

        # start picoboard gateway
        self.start_pbgw()

        # webbrowser.open('https://mryslab.github.io/s3onegpio/', new=1)

        # start the thread to check if processes are still alive
        threading.Thread.__init__(self)
        self.daemon = True
        self.stop_event = threading.Event()
        self.stop_event.clear()
        self.start()

        while True:
            if self.stop_event.is_set():
                print('Exiting. Error detected - is your Picoboard plugged in?')
                sys.exit(0)
            try:
                time.sleep(.01)
            except KeyboardInterrupt:
                sys.exit(0)

    def run(self):
        """
        The thread code to monitor if all processes are still alive.
        """
        while not self.stop_event.is_set():
            bp = ws = pb = None
            try:
                bp = [p.info for p in psutil.process_iter(attrs=['pid', 'name', 'status'])
                      if 'backplane' in p.info['name']]
            except psutil.NoSuchProcess:
                pass
            try:
                ws = [p.info for p in psutil.process_iter(attrs=['pid', 'name', 'status'])
                      if 'wsgw' in p.info['name']]
            except psutil.NoSuchProcess:
                pass
            try:
                pb = [p.info for p in psutil.process_iter(attrs=['pid', 'name', 'status'])
                      if 'pbgw' in p.info['name']]
            except psutil.NoSuchProcess:
                pass

            if not bp:
                self.start_backplane()
                print('start backplane')

            try:
                if bp[0]['status'] == 'zombie':
                    self.killall(bp, ws, pb)
            except IndexError:
                pass

            z = [p.info for p in psutil.process_iter(attrs=['pid', 'name', 'status'])
                 if 'wsgw' in p.info['name']]

            if not z:
                self.killall(bp, ws, pb)
            try:
                if z[0]['status'] == 'zombie':
                    self.killall(bp, ws, pb)
            except IndexError:
                pass

            z = [p.info for p in psutil.process_iter(attrs=['pid', 'name', 'status'])
                 if 'pbgw' in p.info['name']]

            if not z:
                self.killall(bp, ws, pb)

            try:
                if z[0]['status'] == 'zombie':
                    self.killall(bp, ws, pb)
            except IndexError:
                pass

            time.sleep(.1)

    def killall(self, b, w, p):
        """
        Kill all running or zombie processes
        :param b: backplane
        :param w: websocket gateway
        :param p: picoboard gateway
        """

        self.stop_event.set()
        # check for missing processes
        if b:
            try:
                p = psutil.Process(self.proc_bp)
            except psutil.NoSuchProcess:
                pass
            else:
                p.kill()
        if w:
            try:
                w = psutil.Process(self.proc_awg)
            except psutil.NoSuchProcess:
                pass
            else:
                p.kill()
        if p:
            try:
                p = psutil.Process(self.proc_hwg)
            except psutil.NoSuchProcess:
                pass
            else:
                p.kill()

    def start_backplane(self):
        """
        Start the backplane
        """
        for pid in psutil.pids():
            p = psutil.Process(pid)
            if p.name() == "backplane":
                print("Backplane already started.          PID = " + str(p.pid))
                self.backplane_exists = True
                self.proc_bp = p.pid
            else:
                continue

        # if backplane is not already running, start a new instance
        if not self.backplane_exists:
            if sys.platform.startswith('win32'):
                self.proc_bp = subprocess.Popen('backplane',
                                                creationflags=subprocess.CREATE_NO_WINDOW).pid

            else:
                self.proc_bp = subprocess.Popen('backplane',
                                                stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                                                stdout=subprocess.PIPE).pid
            self.backplane_exists = True
            print('Backplane is started...')

    def start_wsgw(self):
        """
        Start the websocket gateway
        """
        if sys.platform.startswith('win32'):
            wsgw_start = ['wsgw', '-i', '9004']
        else:
            wsgw_start = ['wsgw', '-i', '9004']

        if self.log:
            wsgw_start.append('-l')
            wsgw_start.append('True')

        if sys.platform.startswith('win32'):
            self.proc_awg = subprocess.Popen(wsgw_start,
                                             creationflags=subprocess.CREATE_NO_WINDOW).pid

        else:
            self.proc_awg = subprocess.Popen(wsgw_start,
                                             stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                                             stdout=subprocess.PIPE).pid

        print('WebSocket Gateway is started...')

    def start_pbgw(self):
        """
        Start the picoboard gateway
        """
        if sys.platform.startswith('win32'):
            pbgw_start = ['pbgw']
        else:
            pbgw_start = ['pbgw']

        if self.log:
            pbgw_start.append('-l')
            pbgw_start.append('True')
        if self.com_port:
            pbgw_start.append('-c')
            pbgw_start.append(self.com_port)

        if sys.platform.startswith('win32'):
            self.proc_hwg = subprocess.Popen(pbgw_start,
                                             creationflags=subprocess.CREATE_NO_WINDOW).pid
        else:
            self.proc_hwg = subprocess.Popen(pbgw_start,
                                             stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                                             stdout=subprocess.PIPE).pid

        print('Picoboard Gateway is started...')


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
        com_port = args.com_port

    S3P(com_port=com_port, log=log)


# listen for SIGINT
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    # replace with name of function you defined above
    s3px()
