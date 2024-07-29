
import numpy as np

from src.filters.Filter import Filter

class BandPassFilter(Filter):

    def __init__(self, gain, centre_freq_Hz, horiz_scale, cutoff_ratio):
        self.gain = gain
        self.centre_freq_Hz = centre_freq_Hz
        self.horiz_scale = horiz_scale
        self.cutoff_ratio = cutoff_ratio

    # H(f)
    def frequency_response(self, f):
        return_val = np.zeros(len(f), dtype = 'float64')

        freq_ratio = np.abs(f / self.centre_freq_Hz)

        # Create a mask for elements of the frequency ratio under a threshold
        # Calculate the frequency response for the elements marked by the mask
        # Other elements leave at 0
        mask = [False] * len(f)
        mask[1:] = np.abs(np.log10(freq_ratio[1:])) < self.cutoff_ratio

        return_val[mask] = self.gain / np.power(freq_ratio[mask], self.horiz_scale * np.log10(freq_ratio[mask]))

        return return_val