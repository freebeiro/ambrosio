from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    PICOVOICE_ACCESS_KEY: str = Field(..., env="PICOVOICE_ACCESS_KEY")
    HOME_ASSISTANT_URL: str = Field(..., env="HOME_ASSISTANT_URL")
    HOME_ASSISTANT_TOKEN: str = Field(..., env="HOME_ASSISTANT_TOKEN")
    WAKE_WORD_PATH: str = Field(..., env="WAKE_WORD_PATH")
    VOICE_PROVIDER: str = Field("openai", env="VOICE_PROVIDER")

    # Optional fields (if needed)
    google_api_key: str | None = Field(None, env="google_api_key")
    elevenlabs_api_key: str | None = Field(None, env="elevenlabs_api_key")
    elevenlabs_api_voice_id: str | None = Field(None, env="elevenlabs_api_voice_id")
    charles_voice_id: str | None = Field(None, env="charles_voice_id")
    lily_voice_id: str | None = Field(None, env="lily_voice_id")
    bob_model: str | None = Field(None, env="bob_model")
    bob_wake_word: str | None = Field(None, env="bob_wake_word")
    bob_wake_word_sensitivity: str | None = Field(None, env="bob_wake_word_sensitivity")
    bob_listen_duration: str | None = Field(None, env="bob_listen_duration")
    bob_sample_rate: str | None = Field(None, env="bob_sample_rate")
    bob_temperature: str | None = Field(None, env="bob_temperature")
    bob_max_length: str | None = Field(None, env="bob_max_length")

    # Use model_config for configuration
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }