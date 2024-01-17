# camera.py

import logging
from homeassistant.components.camera import Camera
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities: AddEntitiesCallback):
    """Set up the ESP32 Camera from a config entry."""
    unique_id = config_entry.data.get("unique_id", "default_unique_identifier")
    name = "ESP32 Camera"

    # Create a single camera entity
    camera = Esp32Camera(hass, name, unique_id)
        
    async_add_entities([camera], True)

class Esp32Camera(Camera):
    def __init__(self, hass, name, unique_id):
        super().__init__()
        self.hass = hass
        self._name = name
        self._unique_id = f"esp32_camera_{unique_id}"
        self._image = None

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._unique_id

    @property
    def name(self):
        """Return the name of the camera."""
        return "ESP32 Camera"

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return bytes of camera image."""

    def update(self):
        """Update camera image."""
        # Image updating is handled via MQTT, no additional logic needed here
