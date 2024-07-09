class Filter:
    def __init__(self, frequency):
        self.frequency = frequency

    def apply(self, samples, frame_rate):
        raise NotImplementedError("This method should be overridden by subclasses")
