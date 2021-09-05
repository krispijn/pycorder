from config import Config


class Recorder():
    def __init__(self, conf=Config()):
        self.conf = conf
        self.do_record = False

    def stop(self):
        # here we stop the recording
        self.do_record = False
        print("Stop")

    def start(self):
        self.do_record = True
        print("Start")

    def mark(self):
        print("MARK!")