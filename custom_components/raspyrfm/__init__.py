"""Home Assistant integration for the RaspyRFM gateway."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN, PLATFORMS
from .hub import RaspyRFMHub
from .panel import async_register_panel, async_unregister_panel
from .websocket import async_register_websocket_handlers

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up RaspyRFM from a config entry."""
    hub = RaspyRFMHub(hass, entry)

    try:
        await hub.async_setup()
    except OSError as err:
        raise ConfigEntryNotReady("Unable to initialise RaspyRFM hub") from err

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = hub

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    await async_register_panel(hass, entry)
    async_register_websocket_handlers(hass)

    entry.async_on_unload(entry.add_update_listener(async_update_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a RaspyRFM config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hub = hass.data[DOMAIN].pop(entry.entry_id)
        await hub.async_unload()
        await async_unregister_panel(hass, entry)

    return unload_ok


async def async_update_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    hub: RaspyRFMHub = hass.data[DOMAIN][entry.entry_id]
    await hub.async_update_entry(entry)
