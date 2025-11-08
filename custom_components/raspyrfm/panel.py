"""Frontend panel registration for RaspyRFM."""

from __future__ import annotations

from importlib import resources
from typing import Set

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import PANEL_ICON, PANEL_TITLE, PANEL_URL_PATH

STATIC_PATH = "/raspyrfm_static"


async def async_register_panel(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Register the RaspyRFM panel."""

    entries: Set[str] = hass.data.setdefault("_raspyrfm_panel_entries", set())
    if entry.entry_id in entries:
        return

    if not entries:
        panel_path = resources.files(__package__).joinpath("frontend")
        hass.http.register_static_path(STATIC_PATH, str(panel_path), cache_headers=False)
        hass.components.frontend.async_register_panel(
            component_name="custom",
            frontend_url_path=PANEL_URL_PATH,
            webcomponent_path=f"{STATIC_PATH}/raspyrfm-panel.js",
            config={"name": PANEL_TITLE, "icon": PANEL_ICON},
            require_admin=True,
        )

    entries.add(entry.entry_id)


async def async_unregister_panel(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Unregister panel for a given entry."""

    entries: Set[str] = hass.data.get("_raspyrfm_panel_entries", set())
    entries.discard(entry.entry_id)

    if entries:
        return

    hass.components.frontend.async_remove_panel(PANEL_URL_PATH)
    hass.http.unregister_static_path(STATIC_PATH)
    hass.data.pop("_raspyrfm_panel_entries", None)
