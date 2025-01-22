import websockets
import json
import base64
from tenacity import retry, stop_after_attempt, wait_exponential
from core.interfaces import IVoiceProcessor

class OpenAIVoiceProcessor(IVoiceProcessor):
    def __init__(self, api_key: str, system_prompt: str):
        self.headers = {"Authorization": f"Bearer {api_key}", "OpenAI-Beta": "realtime=v1"}
        self.system_prompt = system_prompt

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def process_audio(self, audio: bytes) -> dict:
        async with websockets.connect("wss://api.openai.com/v1/realtime", extra_headers=self.headers) as ws:
            await self._configure_session(ws)
            await self._send_audio(ws, audio)
            return await self._receive_response(ws)

    async def text_to_speech(self, text: str) -> bytes:
        return b"dummy_audio_data"

    async def _configure_session(self, ws):
        await ws.send(json.dumps({
            "type": "session.update",
            "session": {
                "system_message": self.system_prompt,
                "language": "pt-PT",
                "voice": "nova",
                "turn_detection": {"type": "server_vad", "silence_duration_ms": 600},
                "input_audio_format": "pcm16",
                "output_audio_format": "pcm16"
            }
        }))

    async def _send_audio(self, ws, audio: bytes):
        await ws.send(json.dumps({
            "type": "input_audio_buffer.append",
            "audio": base64.b64encode(audio).decode("utf-8")
        }))

    async def _receive_response(self, ws):
        return json.loads(await ws.recv())
