import numpy as np
from pydub import AudioSegment
from pydub.playback import play
import soundfile as sf

class AudioPreprocessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def process_audio(self):
        audio = AudioSegment.from_file(self.file_path)
        samples = audio.get_array_of_samples()
        samples = np.array(samples).astype(np.float32)
        return samples, audio.frame_rate

    def save_audio(self, samples, frame_rate, file_path):
        max_sample = max(samples)

        # Scale down samples if over max
        if(max_sample > (np.iinfo(np.int16)).max):
            ratio = (np.iinfo(np.int16)).max / max_sample
            samples *= ratio
            
        samples = samples.astype(np.int16)
        sf.write(file_path, samples, frame_rate)
