
import numpy as np

from src.filters.BandPassFilter import BandPassFilter

class PeakNotchFilter(BandPassFilter):

    def __init__(self, gain, centre_freq_Hz, horiz_scale):
        super().__init__(gain - 1, centre_freq_Hz, horiz_scale)

    # H(f)
    def frequency_response(self, f):
        return super().frequency_response(f) + 1
