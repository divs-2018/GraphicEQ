
import numpy as np
import math

from src.filters.Filter import Filter

class PeakNotchFilter(Filter):

    def __init__(self, gain, centre_freq_Hz, horiz_scale):
        self.gain = gain
        self.centre_freq_Hz = centre_freq_Hz
        self.horiz_scale = horiz_scale

    def H_peakNotch(self, f):
        freq_ratio = np.abs(f / self.centre_freq_Hz)
        return 1 + (self.gain - 1) / np.pow(freq_ratio, self.horiz_scale * np.log10(freq_ratio))
    
    def apply(self, samples, frame_rate):
        fft_samples = np.fft.fft(samples)
        freqs = np.fft.fftfreq(len(fft_samples), 1.0 / frame_rate)
        
        filtered_fft_samples = fft_samples * self.H_peakNotch(freqs)
        
        filtered_samples = np.fft.ifft(filtered_fft_samples)

        return np.real(filtered_samples)
