from tenacity import retry, stop_after_attempt, wait_exponential, RetryError, before_sleep_log, retry_if_exception_type
from core.interfaces import IVoiceToText, ITextToSpeech, ILogger
from pydantic import BaseModel, ValidationError
import websockets
import json
import base64
import uuid
import unicodedata
import logging
import ssl
from integrations.smart_home.home_assistant import HomeAssistantController
from core.exceptions import PermanentError, RetryableError

class OpenAIVoiceProcessor(IVoiceToText, ITextToSpeech):
    class IntentResponse(BaseModel):
        intent_type: str 
        entities: list[dict]
        confidence: float
        requires_confirmation: bool = False
        entity_id: str  # Required field that was missing

    def __init__(self, api_key: str, system_prompt: str, smart_home_controller: HomeAssistantController, logger: ILogger, model: str = "gpt-4o-realtime-preview-2024-10-01"):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "OpenAI-Beta": "realtime=v1"
        }
        self.system_prompt = system_prompt
        self.smart_home_controller = smart_home_controller
        self.model = model
        self.logger = logger

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        retry=retry_if_exception_type(RetryableError),
        before_sleep=lambda retry_state: self.logger.log(
            "WARNING",
            f"Retrying ({retry_state.attempt_number}): {retry_state.outcome.exception()}"
        ) if self.logger else None
    )
    async def process_audio(self, audio: bytes) -> dict:
        self.logger.debug(f"Initializing connection to OpenAI Realtime API ({self.model})")
        try:
            # Create standard logger for websockets library compatibility
            ws_logger = logging.getLogger(__name__)
            ws_logger.setLevel(logging.WARNING)
            
            ws = await websockets.connect(
                f"wss://api.openai.com/v1/realtime/voice?model={self.model}",
                extra_headers=self.headers,
                ping_interval=20,
                ping_timeout=30,
                open_timeout=15,
                close_timeout=10,
                ssl=ssl.create_default_context(),
                logger=ws_logger  # Use separate logger that supports isEnabledFor
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
                    try:
                        intent = await self._validate_intent(transcript)
                        if intent.intent_type == "home_assistant":
                            final_response = await self._execute_home_assistant_command(intent)
                        else:
                            final_response = await self._handle_conversation(intent)
                    except ValidationError as e:
                        self.logger.error(f"Invalid intent structure: {str(e)}")
                        return {"error": "Invalid command structure", "details": str(e)}
                
                elif response.get('type') == 'response.done':
                    return final_response
                
                elif response.get('type') == 'error':
                    return self._handle_api_error(response)

            return {"error": "Connection closed without complete response"}
            
        except websockets.WebSocketException as e:
            self.logger.error(f"WebSocket error: {str(e)}")
            raise RetryableError("WebSocket communication failed") from e
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            return {"error": "Voice processing error"}

    @retry(
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type((ValidationError, json.JSONDecodeError)),
        before_sleep=lambda retry_state: self.logger.log(
            "WARNING",
            f"Intent validation retry ({retry_state.attempt_number}): {retry_state.outcome.exception()}"
        ) if self.logger else None
    )
    async def _validate_intent(self, transcript: str) -> IntentResponse:
        """Validate and parse LLM response structure"""
        llm_response = await self._get_llm_response(transcript)
        try:
            return self.IntentResponse(**llm_response)
        except ValidationError as e:
            self.logger.error(f"Validation failed: {str(e)}")
            raise

    async def _get_llm_response(self, transcript: str) -> dict:
        """Get raw LLM response with error handling"""
        # Implementation here

    async def _execute_home_assistant_command(self, intent: IntentResponse):
        """Execute validated home assistant command"""
        # Implementation here

    # Rest of the file remains the same with proper validation integration
