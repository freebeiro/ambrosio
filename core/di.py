from config.settings import Settings
from core.interfaces import ILogger
from utils.logger import ProductionLogger
from integrations.voice_processing.openai_realtime import OpenAIVoiceProcessor
from integrations.wake_word.porcupine import PorcupineWakeWordDetector
from integrations.smart_home.home_assistant import HomeAssistantController

PROVIDER_MAP = {"openai": OpenAIVoiceProcessor}

def initialize_components(settings: Settings):
    voice_cls = PROVIDER_MAP.get(settings.VOICE_PROVIDER)
    if not voice_cls:
        raise ValueError(f"Unsupported provider: {settings.VOICE_PROVIDER}")

    return {
        "voice_processor": voice_cls(
            settings.OPENAI_API_KEY,
            open("config/system_prompt.txt").read()
        ),
        "wake_word_detector": PorcupineWakeWordDetector(
            settings.PICOVOICE_ACCESS_KEY,
            settings.WAKE_WORD_PATH,
            logger=ProductionLogger()
        ),
        "smart_home": HomeAssistantController(
            settings.HOME_ASSISTANT_URL,
            settings.HOME_ASSISTANT_TOKEN
        )
    }
