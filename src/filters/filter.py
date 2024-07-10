class Filter:
    def __init__(self, frequencies, gains):
        self.frequencies = frequencies
        self.gains = gains

    def apply(self, samples, frame_rate):
        raise NotImplementedError("This method should be overridden by subclasses")
