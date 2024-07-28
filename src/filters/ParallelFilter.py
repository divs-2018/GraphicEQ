
import numpy as np

from src.filters.EqualizingFilter import EqualizingFilter
from src.filters.SidePassFilter import SidePassFilter
from src.filters.BandPassFilter import BandPassFilter

class ParallelFilter(EqualizingFilter):

    def __init__(self, control_frequencies, gains, horiz_scale):
        super().__init__(control_frequencies, gains)
        self.horiz_scale = horiz_scale
        self.sub_filters = []

        # Low Pass
        low_pass_cross_over_freq = np.sqrt(
            control_frequencies[0] * control_frequencies[1]
        )
        self.sub_filters.append(
            SidePassFilter(
                gains[0],
                low_pass_cross_over_freq,
                horiz_scale
            )
        )

        # High Pass
        high_pass_cross_over_freq = np.sqrt(
            control_frequencies[-1] * control_frequencies[-2]
        )
        self.sub_filters.append(
            SidePassFilter(
                gains[-1],
                high_pass_cross_over_freq,
                -horiz_scale
            )
        )

        # Band Passes
        for i in range(1, self.num_bands - 1):
            self.sub_filters.append(
                BandPassFilter(
                    gains[i],
                    control_frequencies[i],
                    horiz_scale
                )
            )

    # H(f)
    def frequency_response(self, f):
        return_val = np.zeros(len(f), dtype = 'float64')

        for i in range(0, len(self.sub_filters)):
            return_val += self.sub_filters[i].frequency_response(f)

        return return_val
