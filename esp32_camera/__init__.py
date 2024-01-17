# __init__.py

import logging
import asyncio
from homeassistant.components.mqtt import DOMAIN as MQTT_DOMAIN
from homeassistant.const import Platform, EVENT_HOMEASSISTANT_STOP
from .const import CAMERA_TOPIC, DOMAIN, IMAGE_ENTITY

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.CAMERA, Platform.IMAGE]


async def async_setup(hass, config):
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass, entry):
    """Set up ESP32 Camera from a config entry."""
    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )
        return True

async def message_received(msg):
    """Define a function to handle incoming MQTT messages"""
    _LOGGER.info("Image URL received from ESP32 camera")
    image_url = msg.payload.decode("utf-8")
    hass.data[DOMAIN][IMAGE_ENTITY].update_image(image_url)

    await hass.components.mqtt.async_subscribe(CAMERA_TOPIC, message_received)

    entry.async_on_unload(
        hass.bus.async_listen_once(
            EVENT_HOMEASSISTANT_STOP,
            lambda event: hass.components.mqtt.async_unsubscribe(
                CAMERA_TOPIC, message_received
            ),
        )
    )

    mqtt_subscription = await hass.components.mqtt.async_subscribe(
        CAMERA_TOPIC,
        message_received,
        encoding=None
    )

    def stop_homeassistant(event):
        hass.async_create_task(mqtt_subscription())

    entry.async_on_unload(
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, stop_homeassistant)
    )

    return True
