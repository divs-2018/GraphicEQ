
import numpy as np

from src.filters.EqualizingFilter import EqualizingFilter
from src.filters.ShelfFilter import ShelfFilter
from src.filters.PeakNotchFilter import PeakNotchFilter

class CascadeFilter(EqualizingFilter):

    def __init__(self, control_frequencies, gains, horiz_scale):
        super().__init__(control_frequencies, gains)
        self.horiz_scale = horiz_scale
        self.num_bands = len(control_frequencies)
        self.sub_filters = []
        
        # Low Shelf
        self.sub_filters.append(
            ShelfFilter(
                gains[0],
                control_frequencies[0],
                horiz_scale
            )
        )

        # High Shelf
        self.sub_filters.append(
            ShelfFilter(
                gains[-1],
                control_frequencies[-1],
                -horiz_scale
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

    def apply(self, samples, frame_rate):
        filtered_samples = samples

        for i in range(0, self.num_bands):
            filtered_samples = self.sub_filters[i].apply(filtered_samples, frame_rate)

        return filtered_samples
