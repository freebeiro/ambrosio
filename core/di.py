from config.settings import Settings
from core.interfaces import ILogger, IVoiceProcessor
from utils.logger import ProductionLogger
from integrations.wake_word.porcupine import PorcupineWakeWordDetector
from integrations.smart_home.home_assistant import HomeAssistantController
from typing import Dict, Type

class VoiceProviderRegistry:
    _providers: Dict[str, Type[IVoiceProcessor]] = {}

    @classmethod
    def register(cls, name: str):
        def decorator(provider: Type[IVoiceProcessor]):
            cls._providers[name] = provider
            return provider
        return decorator

    @classmethod
    def get_provider(cls, name: str) -> Type[IVoiceProcessor]:
        if name not in cls._providers:
            raise ValueError(f"Unsupported provider: {name}")
        return cls._providers[name]

def initialize_components(settings: Settings):
    # Late import breaks circular dependency while maintaining SOLID principles
    from integrations.voice_processing.openai_realtime import OpenAIVoiceProcessor
    VoiceProviderRegistry._providers["openai"] = OpenAIVoiceProcessor
    
    voice_cls = VoiceProviderRegistry.get_provider(settings.VOICE_PROVIDER)
    if not voice_cls:
        raise ValueError(f"Unsupported provider: {settings.VOICE_PROVIDER}")

    # Initialize smart home controller first
    smart_home = HomeAssistantController(
        settings.HOME_ASSISTANT_URL,
        settings.HOME_ASSISTANT_TOKEN
    )
    
    # Create voice processor with smart home dependency
    voice_processor = voice_cls(
        settings.OPENAI_API_KEY,
        open("config/system_prompt.txt").read(),
        smart_home_controller=smart_home
    )
    
    return {
        "voice_processor": voice_processor,
        "wake_word_detector": PorcupineWakeWordDetector(
            settings.PICOVOICE_ACCESS_KEY,
            settings.WAKE_WORD_PATH,
            logger=ProductionLogger()
        ),
        "smart_home": smart_home
    }
