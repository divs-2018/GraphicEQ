class Filter:
    def __init__(self, name):
        self.name = name

    def apply(self, samples):
        raise NotImplementedError("This method should be overridden by subclasses")