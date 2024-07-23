
import numpy as np

from src.filters.Filter import Filter

class ShelfFilter(Filter):

    def __init__(self, gain, cross_over_freq_Hz, horiz_scale, is_cascade):
        self.gain = gain
        self.cross_over_freq_Hz = cross_over_freq_Hz
        self.horiz_scale = horiz_scale
        self.is_cascade = is_cascade

    # H(f)
    def frequency_response(self, f):
        return_val = super().frequency_response(f)

        freq_ratio = np.abs(f[1:] / self.cross_over_freq_Hz)
        scale_factor = (self.gain - 1) / (1 + np.power(freq_ratio, self.horiz_scale))
        return_val[1:] = 1 + scale_factor if self.is_cascade else 2 * scale_factor
        
        return return_val
