# config_flow.py

from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN


class Esp32CameraConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ESP32 Camera."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return Esp32CameraOptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(step_id="user")

        return self.async_create_entry(title="ESP32 Camera", data={})


class Esp32CameraOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return self.async_show_form(step_id="init")
