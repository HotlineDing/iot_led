import numpy as np
import pyaudio
import time, sys, math


class Audio_Stream:
    '''
    The Audio_Stream class reads bytes from a input source through PyAudio.
    '''

    def __init__(self,
        device = None,
        rate = None,
        updates_per_second = 1000,
        verbose = False):

        self.rate = rate
        self.verbose = verbose
        self.pa = pyaudio.PyAudio()

        self.stream = self.pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate
            input=True,
            frames_per_buffer=
            stream_callback=self.non_blocking_stream_read)

        self.data_buffer = None

    
    def non_blocking_stream_read(self, in_data, frame_count, time_info, status_flags):
        self.data_buffer.append_data(
