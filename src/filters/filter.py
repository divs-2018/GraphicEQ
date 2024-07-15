class Filter:
    def apply(self, samples, frame_rate):
        raise NotImplementedError("This method should be overridden by subclasses")
