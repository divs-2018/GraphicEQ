import numpy as np
from pydub import AudioSegment

class AudioPreprocessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def process_audio(self):
        audio = AudioSegment.from_file(self.file_path)
        samples = audio.get_array_of_samples()
        samples = np.array(samples).astype(np.float32)
        return samples, audio.frame_rate
