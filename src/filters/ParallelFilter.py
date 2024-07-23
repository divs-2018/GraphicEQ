
import numpy as np

from src.filters.EqualizingFilter import EqualizingFilter
from src.filters.ShelfFilter import ShelfFilter
from src.filters.PeakNotchFilter import PeakNotchFilter

class ParallelFilter(EqualizingFilter):

    def __init__(self, control_frequencies, gains, horiz_scale):
        super().__init__(control_frequencies, gains)
        self.horiz_scale = horiz_scale
        self.num_bands = len(control_frequencies)
        self.sub_filters = []

        # Low Shelf
        low_shelf_cross_over_freq = np.sqrt(
            control_frequencies[0] * control_frequencies[1]
        )
        self.sub_filters.append(
            ShelfFilter(
                gains[0],
                low_shelf_cross_over_freq,
                horiz_scale,
                False
            )
        )

        # High Shelf
        high_shelf_cross_over_freq = np.sqrt(
            control_frequencies[-1] * control_frequencies[-2]
        )
        self.sub_filters.append(
            ShelfFilter(
                gains[-1],
                high_shelf_cross_over_freq,
                -horiz_scale,
                False
            )
        )

        # Peak Notches
        for i in range(1, self.num_bands - 1):
            self.sub_filters.append(
                PeakNotchFilter(
                    gains[i],
                    control_frequencies[i],
                    horiz_scale,
                    False
                )
            )

    # H(f)
    def frequency_response(self, f):
        return_val = super().frequency_response(f)

        for i in range(0, len(self.sub_filters)):
            return_val += self.sub_filters[i].frequency_response(f)

        return return_val