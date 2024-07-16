
import numpy as np
import math

from src.filters.Filter import Filter

class ShelfFilter(Filter):

    def __init__(self, gain, cross_over_freq_Hz, horiz_scale):
        self.gain = gain
        self.cross_over_freq_Hz = cross_over_freq_Hz
        self.horiz_scale = horiz_scale

    def H_shelf(self, f):
        return 1 + (self.gain - 1) / (1 + np.pow(np.abs(f) / self.cross_over_freq_Hz, self.horiz_scale))

    def apply(self, samples, frame_rate):
        fft_samples = np.fft.fft(samples)
        freqs = np.fft.fftfreq(len(fft_samples), 1.0 / frame_rate)
        
        filtered_fft_samples = fft_samples * self.H_shelf(freqs)

        filtered_samples = np.fft.ifft(filtered_fft_samples)

        return np.real(filtered_samples)
        