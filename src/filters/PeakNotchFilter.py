
import numpy as np

from src.filters.Filter import Filter

class PeakNotchFilter(Filter):

    def __init__(self, gain, centre_freq_Hz, horiz_scale):
        self.gain = gain
        self.centre_freq_Hz = centre_freq_Hz
        self.horiz_scale = horiz_scale

    # H(f)
    def frequency_response(self, f):
        return_val = super().frequency_response(f)

        freq_ratio = np.abs(f[1:] / self.centre_freq_Hz)
        return_val[1:] = 1 + (self.gain - 1) / np.power(freq_ratio, self.horiz_scale * np.log10(freq_ratio))
        
        return return_val
