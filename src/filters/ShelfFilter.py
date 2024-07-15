
import numpy as np
import math

from src.filters.Filter import Filter

class ShelfFilter(Filter):

    def __init__(self, gain, cross_over_freq_Hz, horiz_scale):
        self.gain = gain
        self.cross_over_freq_Hz = cross_over_freq_Hz
        self.horiz_scale = horiz_scale

    def H_shelf(self, f, gain, centre_freq_Hz, B):
        return 1 + (gain - 1) / (1 + np.pow(np.abs(f) / centre_freq_Hz, B))

    def apply(self, samples, frame_rate):
        fft_samples = np.fft.fft(samples)
        freqs = np.fft.fftfreq(len(fft_samples), 1.0 / frame_rate)
        
        filtered_fft_samples = fft_samples
        filtered_fft_samples *= self.H_shelf(freqs, self.gain, self.cross_over_freq_Hz, self.horiz_scale)

        filtered_samples = np.fft.ifft(filtered_fft_samples)

        return np.real(filtered_samples)
        

            
