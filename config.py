import alsaaudio

class Config():
    devicename = "US2x2" # Should uniquely identify our audio interface
    channels = 2
    sampleRate = 48000
    format = alsaaudio.PCM_FORMAT_S24_3LE
    recordingDirectory = "/home/yoga/Recordings/"
    bufferSize = 1024
    maxFileTime = 3600 # maximum number of seconds each file is