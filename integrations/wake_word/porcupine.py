import pvporcupine
import sounddevice as sd
import numpy as np
from pvporcupine import PorcupineError
from core.interfaces import IWakeWordDetector

from core.interfaces import ILogger

class PorcupineWakeWordDetector(IWakeWordDetector):
    def __init__(self, access_key: str, wake_word_path: str, logger: ILogger):
        self.logger = logger
        try:
            self.engine = pvporcupine.create(
                access_key=access_key,
                keyword_paths=[wake_word_path],
                model_path="config/porcupine_params_pt.pv"
            )
            self.stream = sd.InputStream(
                samplerate=self.engine.sample_rate,
                channels=1,
                dtype='int16',
                blocksize=self.engine.frame_length
            )
        except PorcupineError as e:
            raise RuntimeError(f"Porcupine init failed: {e}")

    async def detect(self):
        self.stream.start()
        try:
            self.logger.info(f"🔊 Audio stream started | Sample rate: {self.engine.sample_rate}Hz | Buffer size: {self.engine.frame_length}")
            
            while True:
                audio_data = self.stream.read(self.engine.frame_length)
                if audio_data[0].size == 0:
                    continue
                audio = np.frombuffer(audio_data[0], dtype=np.int16)
                detection_score = self.engine.process(audio)
                
                # Calculate RMS volume for monitoring
                rms = np.sqrt(np.mean(np.square(audio.astype(np.float32))))
                db = 20 * np.log10(rms) if rms > 0 else -np.inf
                
                if detection_score >= 0:
                    self.logger.info(f"🔔 WAKE WORD DETECTED! Confidence: {detection_score:.2f} | Peak volume: {db:.1f}dB")
                    return
                
                # Log ambient noise level periodically
                if np.random.random() < 0.01:  # 1% sampling rate
                    self.logger.debug(f"🎚 Ambient noise level: {db:.1f}dB")

        except Exception as e:
            self.logger.error(f"🚨 Detection error: {str(e)}")
            raise
        finally:
            self.stream.stop()
            self.logger.info("🔇 Audio stream closed")
