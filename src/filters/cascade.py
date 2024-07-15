from .filter import Filter
import numpy as np

class CascadeFilter(Filter):
    def __init__(self, frequencies, gains):
        super().__init__(frequencies, gains)

    def apply(self, samples, frame_rate):
        filtered_samples = samples
        for frequency, gain in zip(self.control_frequencies, self.gains):
            if gain != 0:
                gain_factor = 10**(gain/20)
                fft_samples = np.fft.fft(filtered_samples)
                freqs = np.fft.fftfreq(len(fft_samples), 1.0/frame_rate)
                fft_samples[np.abs(freqs - frequency) < frequency/10] *= gain_factor
                filtered_samples = np.fft.ifft(fft_samples)
                filtered_samples = np.real(filtered_samples)
        return filtered_samples
