from tenacity import retry, stop_after_attempt, wait_exponential, RetryError, TryAgain, before_sleep_log, retry_if_exception_type
from core.interfaces import IVoiceToText, ITextToSpeech
from core.interfaces import ILogger
import websockets
import json
import base64
import uuid
import unicodedata
import logging
import ssl
from tenacity import retry, stop_after_attempt, wait_exponential, RetryError, TryAgain, before_sleep_log, retry_if_exception_type
from core.interfaces import IVoiceToText, ITextToSpeech
from integrations.smart_home.home_assistant import HomeAssistantController
from core.exceptions import PermanentError

class OpenAIVoiceProcessor(IVoiceToText, ITextToSpeech):
    def __init__(self, api_key: str, system_prompt: str, smart_home_controller: HomeAssistantController, logger: ILogger, model: str = "gpt-4o-realtime-preview-2024-10-01"):
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "OpenAI-Beta": "realtime=v1",
            "Model": model
        }
        self.system_prompt = system_prompt
        self.smart_home_controller = smart_home_controller
        self.model = model
        self.logger = logger

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        retry=retry_if_exception_type(TryAgain),
        before_sleep=before_sleep_log(logging.getLogger("ambrosio"), logging.WARNING)
    )
    async def process_audio(self, audio: bytes) -> dict:
        self.logger.debug(f"Initializing connection to OpenAI Realtime API ({self.model})")
        try:
            ws = await websockets.connect(
                f"wss://api.openai.com/v1/realtime?model={self.model}",
                extra_headers=self.headers,
                ping_interval=20,
                ping_timeout=30,
                ssl_context=ssl.create_default_context(),
                logger=self.logger,
                open_timeout=15,
                close_timeout=10
            )
            self.logger.info("WebSocket connection established successfully")
            
            await self._configure_session(ws)
            await self._send_audio(ws, audio)
            
            final_response = None
            async for message in ws:
                response = json.loads(message)
                self.logger.debug(f"Received message: {response['type']}")

                if response.get('type') == 'transcript':
                    transcript = response['transcript']
                    normalized_transcript = unicodedata.normalize('NFKD', transcript.lower()).encode('ascii', 'ignore').decode()
                    
                    if "listar dispositivos disponiveis" in normalized_transcript:
                        try:
                            self.logger.info("Processing device listing request")
                            devices = await self.smart_home_controller.get_devices()
                            final_response = {
                                "text": "Dispositivos disponíveis:\n" + "\n".join(
                                    f"- {d['name']} ({d['type']}): {d['state']}"
                                    for d in devices
                                ) if devices else "Nenhum dispositivo encontrado",
                                "metadata": {
                                    "devices": devices or [],
                                    "count": len(devices) if devices else 0,
                                    "types": list({d['type'] for d in devices}) if devices else []
                                }
                            }
                            
                            await ws.send(json.dumps({
                                "type": "response.complete",
                                "response": final_response,
                                "correlation_id": str(uuid.uuid4())
                            }))
                            self.logger.debug("Sent device list response to API")
                            
                        except Exception as e:
                            self.logger.error(f"Device listing failed: {str(e)}", exc_info=True)
                            final_response = {"error": f"Erro ao listar dispositivos: {str(e)}"}
                            await ws.send(json.dumps({
                                "type": "response.complete",
                                "error": final_response
                            }))
                
                elif response.get('type') == 'response.done':
                    self.logger.info("Successfully completed voice processing")
                    return final_response
                
                elif response.get('type') == 'error':
                    error_msg = response.get('message', 'Unknown error')
                    error_code = response.get('code', 'UNKNOWN')
                    self.logger.error(f"API Error ({error_code}): {error_msg}")
                    
                    if error_code in ['RATE_LIMITED', 'SERVER_BUSY']:
                        raise TryAgain()
                    elif error_code in ['AUTH_REQUIRED', 'INVALID_KEY']:
                        raise PermanentError("Invalid API credentials")
                    else:
                        return {
                            "error": "Erro no processamento de voz",
                            "code": error_code,
                            "details": error_msg
                        }

            return {"error": "Conexão fechada sem resposta completa"}
            
        except websockets.WebSocketException as e:
            self.logger.error(f"WebSocket error: {str(e)}")
            raise TryAgain()
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return {"error": "Erro interno no processamento de voz"}

    async def text_to_speech(self, text: str) -> bytes:
        return b"dummy_audio_data"

    async def _configure_session(self, ws):
        self.logger.debug("Configuring API session")
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
        self.logger.info(f"Sending audio data ({len(audio)} bytes)")
        chunk_size = 960
        for i in range(0, len(audio), chunk_size):
            chunk = audio[i:i+chunk_size]
            if len(chunk) < chunk_size:
                chunk += b'\x00' * (chunk_size - len(chunk))
            
            await ws.send(json.dumps({
                "type": "input_audio_buffer.append",
                "audio": base64.b64encode(chunk).decode("utf-8"),
                "sample_rate": 24000,
                "format": "pcm16le"
            }))
        self.logger.debug("Finished sending audio chunks")
