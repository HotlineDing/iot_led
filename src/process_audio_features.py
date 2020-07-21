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
        
        self.bin_energies = self.ear.frequency_bin_energies


    def update(self):
        if np.min(self.ear.bin_mean_values) > 0: #not sure why this is needed
            self.bin_energies = AVERAGE HEIGHT * self.ear.bin_energies / self.ear.bin_mean_values
        
