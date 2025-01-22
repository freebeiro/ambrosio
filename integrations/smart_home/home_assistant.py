from homeassistant_api import Client, HomeassistantAPIError
from core.interfaces import ISmartHomeController

class ServiceMapper:
    """Maps Portuguese voice commands to Home Assistant services"""
    _mappings = {
        "ligar": "turn_on",
        "desligar": "turn_off",
        "ajustar": "set_temperature"
    }

class HomeAssistantController(ISmartHomeController):
    def __init__(self, url: str, token: str):
        self.client = Client(url, token)

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
