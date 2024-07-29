
import numpy as np

from src.filters.Filter import Filter

class EqualizingFilter(Filter):

    def __init__(self, control_frequencies, gains):
        self.control_frequencies = control_frequencies
        self.gains = gains
        self.num_bands = len(control_frequencies)

