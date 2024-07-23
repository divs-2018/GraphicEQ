
import numpy as np

class Filter:

    # H(f)
    def frequency_response(self, f):
        return np.array([1] * len(f), dtype = 'float64')

    def apply(self, samples, frame_rate):
        fft_samples = np.fft.fft(samples)
        freqs = np.fft.fftfreq(len(fft_samples), 1.0 / frame_rate)

        filtered_fft_samples = fft_samples * self.frequency_response(freqs)

        filtered_samples = np.fft.ifft(filtered_fft_samples)

        return np.real(filtered_samples)


