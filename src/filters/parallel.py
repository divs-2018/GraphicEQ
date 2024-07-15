from src.filters.MultiFilter import MultiFilter
import numpy as np
import math

class ParallelFilter(MultiFilter):
    def __init__(self, control_frequencies, gains):
        super().__init__(control_frequencies, gains)

    def apply(self, samples, frame_rate):
        fft_samples = np.fft.fft(samples)
        freqs = np.fft.fftfreq(len(fft_samples), 1.0/frame_rate)

        N_umBands = len(self.control_frequencies)
        f_LBoundHz = self.control_frequencies[0]
        f_UBoundHz = self.control_frequencies[-1]
        R = (f_UBoundHz / f_LBoundHz)**(1 / N_umBands)

        def safe_log(x):
            return np.log(x) if np.all(x > 0) else -np.inf
        
        def f_l(n, f_LBoundHz, R):
            return f_LBoundHz * R**(n-1)

        def f_u(n, f_LBoundHz, R):
            return f_l(n+1, f_LBoundHz, R)

        def f_c(n, f_LBoundHz, R):
            return np.sqrt(f_u(n, f_LBoundHz, R) * f_l(n, f_LBoundHz, R))

        def H_lowPass(f, G_ain, f_centre, B):
            return G_ain / (1 + np.exp(safe_log(f / f_centre) * B**2))

        def H_highPass(f, G_ain, f_centre, B):
            return G_ain / (1 + np.exp(safe_log(f / f_centre) * -B**2))

        def H_bandPass(f, G_ain, f_centre, B):
            try:
                exp_val = np.exp(B * safe_log(f / f_centre))
                result = np.zeros_like(f)
                valid_indices = np.logical_and(np.isfinite(exp_val), exp_val != 0)
                result[valid_indices] = G_ain / (exp_val[valid_indices]**2)
                return result
            except (ZeroDivisionError, ValueError):
                return np.zeros_like(f)

        def H_parallelLowBand(f):
            return H_lowPass(f, self.gains[0], f_u(1, f_LBoundHz, R), 4)

        def H_parallelHighBand(f):
            return H_highPass(f, self.gains[-1], f_l(N_umBands, f_LBoundHz, R), 4)

        def H_parallelMiddleBands(f):
            middle_band_sum = np.zeros_like(f)
            for n in range(1, N_umBands - 1):
                middle_band_sum += H_bandPass(f, self.gains[n], f_c(n, f_LBoundHz, R), 4)
            return middle_band_sum

        def H_parallel(f):
            parallel_low_band = H_parallelLowBand(f)
            parallel_high_band = H_parallelHighBand(f)
            return parallel_low_band + parallel_high_band + H_parallelMiddleBands(f)
        
        def scale_values(array):
            max_abs_real = np.max(np.abs(array.real))
            
            if max_abs_real > 16384:
                scaled_array = (array / max_abs_real) * (16384 * 2) # we take 16384 to be the maximum tolerable value for wav data. I thought it should be 32767, but seemingly not.
            return scaled_array
        
        print("mid")
        for i in range(0, len(freqs), 1000):
            print(H_parallelMiddleBands(freqs[i]))

        fft_samples *= H_parallel(freqs)

        filtered_samples = np.fft.ifft(fft_samples)
        filtered_samples = scale_values(filtered_samples)
        return np.real(filtered_samples)