import sounddevice as sd
import numpy as np

class AudioRecorder:
    def __init__(self, sample_rate: int = 24000, duration: int = 5):
        self.sample_rate = sample_rate
        self.duration = duration

    async def record(self) -> bytes:
        frames = int(self.duration * self.sample_rate)
        audio = sd.rec(frames, samplerate=self.sample_rate, channels=1, dtype='int16')
        sd.wait()
        return audio.tobytes()

class AudioPlayer:
    def __init__(self, sample_rate: int = 24000):
        self.sample_rate = sample_rate

    async def play(self, audio_data: bytes):
        audio = np.frombuffer(audio_data, dtype=np.int16)
        sd.play(audio, samplerate=self.sample_rate)
        sd.wait()
