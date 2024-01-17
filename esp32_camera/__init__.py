import logging
import asyncio
from homeassistant.components.mqtt import DOMAIN as MQTT_DOMAIN
from homeassistant.const import Platform, EVENT_HOMEASSISTANT_STOP
from .const import CAMERA_TOPIC, DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.CAMERA]

async def async_setup(hass, config):
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass, entry):
    """Set up ESP32 Camera from a config entry."""
    # Forward the setup to the camera platform
    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    # Define a function to handle incoming MQTT messages
    async def message_received(msg):
        _LOGGER.info("Image received from ESP32 camera")
        # Store binary payload as-is in hass.data
        hass.data[DOMAIN]["camera_image"] = msg.payload

    # Subscribe to the camera topic for raw binary data
    await hass.components.mqtt.async_subscribe(
        CAMERA_TOPIC, 
        message_received,
        encoding=None  # Specify None to handle binary data
    )

    # Handle the case when Home Assistant stops
    entry.async_on_unload(
        hass.bus.async_listen_once(
            EVENT_HOMEASSISTANT_STOP,
            lambda event: hass.components.mqtt.async_unsubscribe(
                CAMERA_TOPIC, message_received
            ),
        )
    )

    return True
