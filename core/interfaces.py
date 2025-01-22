from typing import Protocol, Dict, Any, Coroutine

class IVoiceToText(Protocol):
    async def process_audio(self, audio: bytes) -> Dict[str, Any]: ...

class ITextToSpeech(Protocol):
    async def synthesize(self, text: str) -> bytes: ...

class IVoiceProcessor(IVoiceToText, ITextToSpeech):
    """Composite interface for voice processing"""

class IWakeWordDetector(Protocol):
    async def detect(self) -> Coroutine[None, None, None]: ...

class ISmartHomeController(Protocol):
    async def execute_command(self, intent: Dict) -> str: ...

class ILogger(Protocol):
    def error(self, message: str) -> None: ...
    def info(self, message: str) -> None: ...
    def debug(self, message: str) -> None: ...

class IDeviceEnumerator(Protocol):
    """Interface for device discovery and enumeration"""
    async def get_devices(self) -> list[dict]:
        """Return list of discovered devices with attributes"""
