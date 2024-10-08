
import numpy as np

from src.filters.Filter import Filter

class LowPassFilter(Filter):

    def __init__(self, gain, cross_over_freq_Hz, horiz_scale):
        self.gain = gain
        self.cross_over_freq_Hz = cross_over_freq_Hz
        self.horiz_scale = horiz_scale

    # H(f)
    def frequency_response(self, f):
        return_val = np.zeros(len(f), dtype = 'float64')

        freq_ratio = np.abs(f[1:] / self.cross_over_freq_Hz)
        return_val[1:] = self.gain / (1 + np.power(freq_ratio, self.horiz_scale))

        return return_val