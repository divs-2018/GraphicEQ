
import numpy as np

from src.filters.EqualizingFilter import EqualizingFilter
from src.filters.LowShelfFilter import LowShelfFilter
from src.filters.HighShelfFilter import HighShelfFilter
from src.filters.PeakNotchFilter import PeakNotchFilter

class CascadeFilter(EqualizingFilter):

    def __init__(self, control_frequencies, gains, horiz_scale):
        super().__init__(control_frequencies, gains)
        self.horiz_scale = horiz_scale
        self.sub_filters = []

        # Low Shelf
        low_shelf_cross_over_freq = np.sqrt(
            control_frequencies[0] * control_frequencies[1]
        )
        self.sub_filters.append(
            LowShelfFilter(
                gains[0],
                low_shelf_cross_over_freq,
                horiz_scale
            )
        )

        # High Shelf
        high_shelf_cross_over_freq = np.sqrt(
            control_frequencies[-1] * control_frequencies[-2]
        )
        self.sub_filters.append(
            HighShelfFilter(
                gains[-1],
                high_shelf_cross_over_freq,
                horiz_scale
            )
        )

        # Peak Notches
        for i in range(1, self.num_bands - 1):
            self.sub_filters.append(
                PeakNotchFilter(
                    gains[i],
                    control_frequencies[i],
                    horiz_scale
                )
            )

    # H(f)
    def frequency_response(self, f):
        return_val = super().frequency_response(f)

        for i in range(0, len(self.sub_filters)):
            return_val *= self.sub_filters[i].frequency_response(f)

        return return_val
