import numpy as np
import os
import time
import config
from audio_processing import start_stream



'''
pid = os.fork()
if pid:
    audio_processing.start_stream(print)
else:
    print("STARTING")
    time.sleep(3)
    audio_processing.stream_flag = False
    print(audio_processing.stream_flag)
    print("DONE")
'''
