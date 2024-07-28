
from src.filters.basic.LowPassFilter import LowPassFilter

class HighPassFilter(LowPassFilter):

    def __init__(self, gain, cross_over_freq_Hz, horiz_scale):
        super().__init__(gain, cross_over_freq_Hz, -horiz_scale)