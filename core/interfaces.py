from typing import Protocol, Dict, Any, Coroutine

class IVoiceProcessor(Protocol):
    async def process_audio(self, audio: bytes) -> Dict[str, Any]: ...
    async def text_to_speech(self, text: str) -> bytes: ...

class IWakeWordDetector(Protocol):
    async def detect(self) -> Coroutine[None, None, None]: ...

class ISmartHomeController(Protocol):
    async def execute_command(self, intent: Dict) -> str: ...

class ILogger(Protocol):
    def error(self, message: str) -> None: ...
    def info(self, message: str) -> None: ...
    def debug(self, message: str) -> None: ...
