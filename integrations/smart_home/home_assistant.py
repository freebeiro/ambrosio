import asyncio
from homeassistant_api import Client, HomeassistantAPIError
from core.interfaces import ISmartHomeController, IDeviceEnumerator
import time
from typing import Callable, Optional

class ServiceMapper:
    """Maps Portuguese voice commands to Home Assistant services"""
    _mappings = {
        "ligar": "turn_on",
        "desligar": "turn_off",
        "ajustar": "set_temperature"
    }

class DeviceRegistry:
    """Caching registry with TTL-based expiration"""
    def __init__(self, fetch_callback: Callable, ttl: int = 600):
        self._fetch = fetch_callback
        self._cache: Optional[list[dict]] = None
        self._last_updated: float = 0
        self.ttl = ttl

    async def get_devices(self) -> list[dict]:
        """Get cached devices or fetch fresh data"""
        if self._cache_expired:
            # Run synchronous API call in thread pool
            self._cache = await asyncio.get_event_loop().run_in_executor(
                None, self._fetch
            )
            self._last_updated = time.time()
        return self._normalized_devices

    @property
    def _cache_expired(self) -> bool:
        return (time.time() - self._last_updated) > self.ttl

    @property
    def _normalized_devices(self) -> list[dict]:
        """Standardized device format across integrations"""
        return [
            {
                "id": entity.entity_id,
                "name": entity.attributes.get("friendly_name"),
                "type": entity.entity_id.split(".", 1)[0],
                "state": entity.state,
                "attributes": dict(entity.attributes)
            }
            for entity in self._cache
        ]

class HomeAssistantController(ISmartHomeController, IDeviceEnumerator):
    def __init__(self, url: str | None = None, token: str | None = None):
        from dotenv import load_dotenv
        import os
        load_dotenv()
        base_url = url or os.getenv("HA_URL")
        api_token = token or os.getenv("HA_TOKEN")
        if not base_url or not api_token:
            raise ValueError("Missing Home Assistant configuration. Check HA_URL and HA_TOKEN in .env")
        self.client = Client(base_url.rstrip('/') + '/', api_token)
        self.device_registry = DeviceRegistry(self._fetch_devices)

    async def get_devices(self) -> list[dict]:
        """Implement IDeviceEnumerator interface"""
        return await self.device_registry.get_devices()

    def _fetch_devices(self) -> list[dict]:
        """Fetch devices using the existing client library"""
        return self.client.get_states()

    async def execute_command(self, intent: dict) -> str:
        try:
            entity_id = intent["entity_id"]
            service = self._map_service(intent["action"])
            await self.client.call_service(
                entity_id.split(".")[0],
                service,
                entity_id=entity_id
            )
            return f"Executed {intent['action']} on {entity_id}"
        except HomeassistantAPIError as e:
            raise RuntimeError(f"Home Assistant error: {e}")

    def _map_service(self, action: str) -> str:
        return ServiceMapper._mappings[action]
