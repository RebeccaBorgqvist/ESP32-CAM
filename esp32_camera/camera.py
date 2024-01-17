import logging
import base64
from homeassistant.components.camera import Camera
from .const import DOMAIN, CAMERA_TOPIC

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([Esp32Camera(hass)])

class Esp32Camera(Camera):
    def __init__(self, hass):
        super().__init__()
        self._hass = hass
        self._last_image = None

        # Subscribe to MQTT topic
        def message_received(msg):
            _LOGGER.info("Image received from ESP32 camera")
            try:
                self._last_image = base64.b64decode(msg.payload)
                self.schedule_update_ha_state()
            except Exception as e:
                _LOGGER.error("Error processing image: %s", e)

        hass.components.mqtt.subscribe(CAMERA_TOPIC, message_received)

    @property
    def name(self):
        return "ESP32 Camera"

    def camera_image(self):
        return self._last_image