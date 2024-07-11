from .filter import Filter
import numpy as np

class ParallelFilter(Filter):
    # frequencies is a list of -centre- frequencies, e.g. [60, 125, 250, 500, 1000, 2000, 4000, 8000, 16000].
    # gains is a list of gains for each of the frequencies, e.g. [6, 0, 0, 0, 0, 0, -5, 0, 0].
    def __init__(self, frequencies, gains):
        super().__init__(frequencies, gains)

    # samples is a list of direct samples from the time-domain file.
    # frame_rate is by default 44100 samples of audio per second.
    def apply(self, samples, frame_rate):

        # fft_samples is a huge list of complex numbers (as many as there were audio samples), representing
        # the magnitude and phase of every single frequency component. (strictly speaking, not every single
        # frequency component as there are an infinite number, but it has as many as there were time samples).
        fft_samples = np.fft.fft(samples)
        # freqs are the equivalent frequencies for each frequency component (i.e., the evenly-spaced domain of fft_samples).
        freqs = np.fft.fftfreq(len(fft_samples), 1.0/frame_rate)
        
        for frequency, gain in zip(self.frequencies, self.gains):
            if gain != 0:
                gain_factor = 10**(gain/20)
                fft_samples[np.abs(freqs - frequency) < frequency/10] *= gain_factor

        filtered_samples = np.fft.ifft(fft_samples)
        return np.real(filtered_samples)
