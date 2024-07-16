
import numpy as np

from src.filters.Filter import Filter

class ShelfFilter(Filter):

    def __init__(self, gain, cross_over_freq_Hz, horiz_scale):
        self.gain = gain
        self.cross_over_freq_Hz = cross_over_freq_Hz
        self.horiz_scale = horiz_scale

    # H(f)
    def frequency_response(self, f):
        freq_ratio = np.abs(f / self.cross_over_freq_Hz)
        return 1 + (self.gain - 1) / (1 + np.power(freq_ratio, self.horiz_scale))
