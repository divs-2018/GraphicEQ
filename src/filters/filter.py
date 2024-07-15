class Filter:
    def __init__(self, control_frequencies, gains):
        self.control_frequencies = control_frequencies
        self.gains = gains

    def apply(self, samples, frame_rate):
        raise NotImplementedError("This method should be overridden by subclasses")
