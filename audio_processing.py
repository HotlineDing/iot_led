import numpy as np
import sys
import pyaudio
import config
import matplotlib.pyplot as plt

my_pyaudio = pyaudio.PyAudio()

def start_stream(callback):
    global stream_flag

    pyaud = pyaudio.PyAudio()
    samples_per_frame = int(config.SAMPLE_RATE / config.FPS)

    stream = pyaud.open(channels=1,
                        format=pyaudio.paInt16,
                        rate=config.SAMPLE_RATE,
                        input=True,
                        frames_per_buffer=samples_per_frame)

    stream_flag = True 
    while stream_flag:
        audio_raw = stream.read(frames_per_buffer)
        audio_data = np.fromstring(audio_raw, dtype=np.int16)
        audio_data = audio_data.astype(np.float32)
        callback(audio_data, config.SAMPLE_RATE)



def spectrogram(samples, sample_rate, stride_ms=10.0,
                window_ms=20.0, max_freq=None, eps=1e-14):
    
    stride_size = int(0.001 * sample_rate * stride_ms)
    window_size = int(0.001 * sample_rate * window_ms)

    truncate_size = (len(samples) - window_size) % stride_size
    samples = samples[:len(samples) - truncate_size]
    nshape = (window_size, (len(samples) - window_size) // stride_size + 1)
    nstrides = (samples.strides[0], samples.strides[0] * stride_size)
    windows = np.lib.stride_tricks.as_strided(samples,
                                                shape = nshape, strides = nstrides)
    assert np.all(windows[:, 1] == samples[stride_size:(stride_size + window_size)])

    weighting = np.hanning(window_size)[:, None]

    fft = np.fft.rfft(windows * weighting, axis=0)
    fft = np.absolute(fft)
    fft = fft**2

    scale = np.sum(weighting**2) * sample_rate
    fft[1:-1, :] *= (2.0 / scale)
    fft[(0, -1), :] /= scale

    freqs = float(sample_rate) / window_size * np.arange(fft.shape[0])

    ind = np.where(freqs <= max_freq)[0][-1] + 1
    specgram = np.log(fft[:ind, :] + eps)
    return specgram


start_stream(print)






