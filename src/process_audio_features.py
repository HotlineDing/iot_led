import numpy as np
import time, sys, math
from matplotlib import cm


class Audio_Features:
    '''
    The Audio_Features class uses raw FFT processed audio input for further processing.
    Used to gather beat data, bins, and more.
    '''

    def __init__(self, ear):
        self.ear = ear
