import audioop
import struct

import numpy as np

from config import Config
from datetime import datetime, timedelta
from time import sleep
import threading
import alsaaudio
import numpy
import wave
import audioop

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

        sTime = datetime.now().strftime('%H%M')
        sDate = datetime.now().strftime('%Y%m%d')

        pcmDevices = alsaaudio.pcms(alsaaudio.PCM_CAPTURE)
        pcmDeviceFound = None

        for device in pcmDevices:
            if 'sysdefault' in device and self.conf.devicename in device:
                pcmDeviceFound = device
                break

        if pcmDeviceFound is None:
            # TODO throw actual error
            print ("ERROR: Device not found. Cards available: " + str(alsaaudio.pcms()))
            return

        inp = alsaaudio.PCM(type=alsaaudio.PCM_CAPTURE,
                            device=pcmDeviceFound)

        inp.setformat(alsaaudio.PCM_FORMAT_S24_LE)
        inp.setchannels(self.conf.channels)
        inp.setrate(self.conf.sampleRate)
        inp.setperiodsize(self.conf.bufferSize)

        self.info = inp.dumpinfo()
        print (self.info)

        wavFileName='test_' + sDate + '_' + sTime  + '.wav'
        
        w = wave.open(wavFileName, 'w')
        w.setnchannels(self.conf.channels)
        w.setsampwidth(3)
        w.setframerate(self.conf.sampleRate)

        while getattr(t, "do_run", True):

            l, data = inp.read()

            # Determine signal levels (for use in GUI)
            a = np.fromstring(data, dtype=np.int32) # 24 bit packed into int32 because Python
            peakL = self.convert_to_decibel(np.max(np.abs(a[0])), 2 ** 23)
            peakR = self.convert_to_decibel(np.max(np.abs(a[1])), 2 ** 23)

            self.peak = [peakL, peakR]

            if np.max(self.peak) >= -0.01:
                self.clip = True
                print ("CLIP")

            # Write data to wave file output
            w.writeframes(data)

            self.recordingTime = datetime.now() - self.recordingStart

        w.close()

        inp.close()

    def convert_to_decibel(self, arr, ref):
        if arr != 0:
            return 20 * numpy.log10(abs(arr) / ref)
        else:
            return -60

    def __init__(self, conf=Config()):
        self.conf = conf
        self.do_record = False
        self.recordingTime = timedelta(0)

