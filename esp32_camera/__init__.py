import logging
from homeassistant.components.mqtt import DOMAIN as MQTT_DOMAIN
from homeassistant.const import CONF_PLATFORM, EVENT_HOMEASSISTANT_STOP
from .const import DOMAIN, CAMERA_TOPIC

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    """Set up the ESP32 Camera component."""
    return True

async def async_setup_entry(hass, entry):
    """Set up ESP32 Camera from a config entry."""

    # Define a function to handle incoming MQTT messages
    async def message_received(msg):
        _LOGGER.info(f"Message received on topic {msg.topic}: {msg.payload}")

    # Subscribe to the camera topic
    await hass.components.mqtt.async_subscribe(CAMERA_TOPIC, message_received)

    # Handle the case when Home Assistant stops
    entry.async_on_unload(
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, lambda event: 
            hass.components.mqtt.async_unsubscribe(CAMERA_TOPIC, message_received))
    )

    return True
