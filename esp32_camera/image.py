# image.py

import datetime
from homeassistant.components.image import ImageEntity
from .const import DOMAIN, IMAGE_ENTITY


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Esp32ImageEntity from a config entry."""
    image_entity = Esp32ImageEntity(hass)

    async_add_entities([image_entity], update_before_add=True)

    return True


class Esp32ImageEntity(ImageEntity):
    def __init__(self, hass):
        self.hass = hass
        self._image_url = None
        self._image_last_updated = None

    @property
    def image_last_updated(self):
        """Timestamp of when the image was last updated."""
        return self._image_last_updated

    @property
    def image(self):
        """Return URL of camera image."""
        return self._image_url

    def update_image(self, image_url):
        """Update the image URL and the timestamp."""
        self._image_url = image_url
        self._image_last_updated = datetime.datetime.now()
        self.async_write_ha_state()  # Inform Home Assistant of the update
