"""Config flow for the RaspyRFM integration."""

from __future__ import annotations

import socket
from typing import Any, Dict

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from .const import CONF_HOST, CONF_PORT, DEFAULT_PORT, DOMAIN


async def _validate_input(hass: HomeAssistant, data: Dict[str, Any]) -> Dict[str, Any]:
    host = data[CONF_HOST]
    port = data[CONF_PORT]

    def _resolve() -> str:
        return socket.gethostbyname(host)

    await hass.async_add_executor_job(_resolve)
    return {"title": f"RaspyRFM ({host})", "host": host, "port": port}


class RaspyRFMConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for RaspyRFM."""

    VERSION = 1

    async def async_step_user(self, user_input: Dict[str, Any] | None = None):
        errors: Dict[str, str] = {}

        if user_input is not None:
            try:
                info = await _validate_input(self.hass, user_input)
            except OSError:
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(user_input[CONF_HOST])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=info["title"], data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
        })
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    async def async_step_import(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """Handle YAML import."""

        return await self.async_step_user(user_input)

    async def async_get_options_flow(self, entry: config_entries.ConfigEntry):
        return RaspyRFMOptionsFlow(entry)


class RaspyRFMOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for RaspyRFM."""

    def __init__(self, entry: config_entries.ConfigEntry) -> None:
        self._entry = entry

    async def async_step_init(self, user_input: Dict[str, Any] | None = None):
        errors: Dict[str, str] = {}

        if user_input is not None:
            new_data = {
                CONF_HOST: user_input[CONF_HOST],
                CONF_PORT: user_input[CONF_PORT],
            }
            self.hass.config_entries.async_update_entry(self._entry, data=new_data)
            return self.async_create_entry(title="", data={})

        schema = vol.Schema({
            vol.Required(CONF_HOST, default=self._entry.data.get(CONF_HOST)): str,
            vol.Required(CONF_PORT, default=self._entry.data.get(CONF_PORT, DEFAULT_PORT)): int,
        })
        return self.async_show_form(step_id="init", data_schema=schema, errors=errors)
