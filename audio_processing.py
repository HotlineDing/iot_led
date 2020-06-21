import numpy as np
import sys
import pyaudio
import config

my_pyaudio = pyaudio.PyAudio()

def start_stream(callback):
    global stream_flag

    pyaud = pyaudio.PyAudio()
    frames_per_buffer = int(config.SAMPLE_RATE / config.FPS)

    stream = pyaud.open(channels=1,
                        format=pyaudio.paInt16,
                        rate=config.SAMPLE_RATE,
                        input=True,
                        frames_per_buffer=frames_per_buffer)

    stream_flag = True 
    while stream_flag:
        audio_raw = stream.read(frames_per_buffer)
        audio_data = np.fromstring(audio_raw, dtype=np.int16)
        audio_data = audio_data.astype(np.float32)


