
from src.filters.LowShelfFilter import LowShelfFilter

class HighShelfFilter(LowShelfFilter):

    def __init__(self, gain, cross_over_freq_Hz, horiz_scale):
        super().__init__(gain, cross_over_freq_Hz, -horiz_scale)