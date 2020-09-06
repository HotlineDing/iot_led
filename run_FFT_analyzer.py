import time
import src.led_class as led
from src.stream_analyzer import Stream_Analyzer

ear = Stream_Analyzer(
                device = None,               # Manually play with this (int) if you don't see anything
                rate   = None,               # Audio samplerate, None uses the default source settings
                FFT_window_size_ms  = 60,    # Window size used for the FFT transform
                updates_per_second  = 1000,  # How often to read the audio stream for new data
                smoothing_length_ms = 50,    # Apply some temporal smoothing to reduce noisy features
                n_frequency_bins    = 24,   # The FFT features are grouped in bins
                visualize = 1,               # Visualize the FFT features with PyGame
                verbose   = 0                # Print running statistics (latency, fps, ...)
                )

Leds = led.Led()
Array = led.Array(ear, 'Array', '192.168.0.150', 7777, 7, 20)
Leds.add_device(Array)
#Cloud = led.Cloud(ear.visualizer, 'Cloud', '192.168.0.150', 7777, [[140, 1]])
#Leds.add_device(Cloud)
#Array2 = led.Array(ear, 'Array', '192.168.0.151', 7777, 10 , 15)
#Leds.add_device(Array2)
#Beat = led.Beat(ear, 'Beat', '192.168.0.150', 7777, 140)
#Leds.add_device(Beat)

fps = 120  #How often to update the FFT features + display
last_update = time.time()


while True:
    if (time.time() - last_update) > (1./fps):
        last_update = time.time()
        raw_fftx, raw_fft, binned_fftx, binned_fft = ear.get_audio_features()
        Leds.update()
