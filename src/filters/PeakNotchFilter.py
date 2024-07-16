
import numpy as np

from src.filters.Filter import Filter

class PeakNotchFilter(Filter):

    def __init__(self, gain, centre_freq_Hz, horiz_scale):
        self.gain = gain
        self.centre_freq_Hz = centre_freq_Hz
        self.horiz_scale = horiz_scale

    # H(f)
    def frequency_response(self, f):
        freq_ratio = np.abs(f / self.centre_freq_Hz)
        return 1 + (self.gain - 1) / np.power(freq_ratio, self.horiz_scale * np.log10(freq_ratio))
