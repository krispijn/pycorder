import threading

from config import Config
from datetime import datetime, timedelta
from time import sleep
import threading
import asyncio

class Recorder():
    def stop(self):
        # here we stop the recording
        self.do_record = False
        self.recThread.do_run = False
        self.recThread.join()

    def start(self):
        self.recThread = threading.Thread(target=self.start_recording)
        self.do_record = True
        self.recordingStart = datetime.now()
        self.recThread.start()


    def mark(self):
        print("MARK!")

    def start_recording(self):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            self.recordingTime = datetime.now() - self.recordingStart
            sleep(1)

    def __init__(self, conf=Config()):
        self.conf = conf
        self.do_record = False
        self.recordingTime = timedelta(0)
