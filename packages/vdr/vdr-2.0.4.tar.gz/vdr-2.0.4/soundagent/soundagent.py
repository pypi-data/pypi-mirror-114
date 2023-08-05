import sys
import time
import socket
import os
import configparser
import logging


config = configparser.ConfigParser()
config.read('config.ini')

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


class SoundAgent:

    config = configparser.ConfigParser()
    config.read('config.ini')

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock = sock
        self.duration = int(self.config['voice']['duration'])

    def send_sound(self):
        filename = "record.mp3"
        buf = 8192
        while True:
            try:
                if not os.path.exists(filename):
                    os.system('arecord -d ' + str(self.duration) + ' -f U8 ' + filename)

                f = open(filename, 'rb')

                self.sock.sendto(b'start', (self.ip, self.port))
                logging.info("Sending sound...")
                data = f.read(buf)

                while data:
                    if self.sock.sendto(data, (self.ip, self.port)):
                        data = f.read(buf)
                        time.sleep(0.02)

                self.sock.sendto(b'stop', (self.ip, self.port))
                if os.path.exists(filename):
                    os.remove(filename)

            except KeyboardInterrupt:
                sys.exit()




