from .filter import Filter
import numpy as np

class ParallelFilter(Filter):
    def __init__(self, frequencies, gains):
        super().__init__(frequencies, gains)

    def apply(self, samples, frame_rate):
        fft_samples = np.fft.fft(samples)
        freqs = np.fft.fftfreq(len(fft_samples), 1.0/frame_rate)
        
        for frequency, gain in zip(self.frequencies, self.gains):
            if gain != 0:
                gain_factor = 10**(gain/20)
                fft_samples[np.abs(freqs - frequency) < frequency/10] *= gain_factor

        filtered_samples = np.fft.ifft(fft_samples)
        return np.real(filtered_samples)
