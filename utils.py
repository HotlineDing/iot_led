import numpy as np
import math, scipy



class circular_data_buffer:
    '''
    A large circular data buffer that is designed for speed
    '''

    def __init__(self,
                n_blocks,
                samples_per_block,
                dtype = np.float32,
                start_value = 0)

        self.n_blocks = n_blocks
        self.samples_per_block = samples_per_block
        self.data = start_value * np.zeros((self.n_blocks, self.samples_per_block), dtype = dtype)

        self.elements_in_buffer = 0
        self.current_block = 0
        self.indices = np.arange(self.n_blocks, dtype=np.int32)

    def add_data(self, data_block):
        next_block = (self.current_block + 1) % self.n_blocks
        self.data[next_block, :] = data_block
        
        self.current_block = next_block

    def get_current_block(self):
        data = self.data[self.current_block]
        self.current_block += 1
        return data
