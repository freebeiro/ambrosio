import asyncio
import os
from config.settings import Settings
from core.di import initialize_components
from utils.audio import AudioRecorder, AudioPlayer
from utils.logger import ProductionLogger

async def main():
    logger = ProductionLogger()
    settings = Settings()

    try:
        components = initialize_components(settings)
        recorder = AudioRecorder()
        player = AudioPlayer()

        while True:
            try:
                await components["wake_word_detector"].detect()
                audio = await recorder.record()
                response = await components["voice_processor"].process_audio(audio)
                feedback = await components["smart_home"].execute_command(response)
                await player.play(await components["voice_processor"].text_to_speech(feedback))
            except Exception as e:
                logger.error(f"Error: {e}")
                await asyncio.sleep(1)

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
