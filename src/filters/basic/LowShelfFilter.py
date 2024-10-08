
from src.filters.basic.LowPassFilter import LowPassFilter

class LowShelfFilter(LowPassFilter):

    def __init__(self, gain, cross_over_freq_Hz, horiz_scale):
        super().__init__(gain - 1, cross_over_freq_Hz, horiz_scale)

    # H(f)
    def frequency_response(self, f):
        return super().frequency_response(f) + 1