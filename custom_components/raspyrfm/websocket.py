"""Websocket commands exposed by the RaspyRFM integration."""

from __future__ import annotations

import logging
from typing import Any, Dict

import voluptuous as vol

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.components import websocket_api

from .const import (
    DOMAIN,
    SIGNAL_LEARNING_STATE,
    SIGNAL_SIGNAL_RECEIVED,
    WS_TYPE_DEVICE_CREATE,
    WS_TYPE_DEVICE_DELETE,
    WS_TYPE_DEVICE_LIST,
    WS_TYPE_DEVICE_RELOAD,
    WS_TYPE_LEARNING_START,
    WS_TYPE_LEARNING_STATUS,
    WS_TYPE_LEARNING_STOP,
    WS_TYPE_LEARNING_SUBSCRIBE,
    WS_TYPE_SIGNALS_LIST,
    WS_TYPE_SIGNALS_SUBSCRIBE,
)
from .hub import RaspyRFMHub

_LOGGER = logging.getLogger(__name__)

HANDLERS_REGISTERED = "_raspyrfm_ws_handlers"


def async_register_websocket_handlers(hass: HomeAssistant) -> None:
    """Register websocket commands."""

    if hass.data.get(HANDLERS_REGISTERED):
        return

    websocket_api.async_register_command(hass, handle_learning_start)
    websocket_api.async_register_command(hass, handle_learning_stop)
    websocket_api.async_register_command(hass, handle_learning_status)
    websocket_api.async_register_command(hass, handle_learning_subscribe)
    websocket_api.async_register_command(hass, handle_signals_list)
    websocket_api.async_register_command(hass, handle_signals_subscribe)
    websocket_api.async_register_command(hass, handle_device_create)
    websocket_api.async_register_command(hass, handle_device_delete)
    websocket_api.async_register_command(hass, handle_device_list)
    websocket_api.async_register_command(hass, handle_device_reload)

    hass.data[HANDLERS_REGISTERED] = True


def _get_hub(hass: HomeAssistant, msg: Dict[str, Any]) -> RaspyRFMHub:
    entry_id = msg.get("entry_id")
    if entry_id is None:
        # fallback to first entry
        if DOMAIN not in hass.data or not hass.data[DOMAIN]:
            raise websocket_api.HomeAssistantWebSocketError("No RaspyRFM entries configured")
        entry_id = next(iter(hass.data[DOMAIN]))

    hub = hass.data[DOMAIN].get(entry_id)
    if hub is None:
        raise websocket_api.HomeAssistantWebSocketError("Unknown RaspyRFM entry")
    return hub


@websocket_api.websocket_command({vol.Required("type"): WS_TYPE_LEARNING_START, vol.Optional("entry_id"): str})
@websocket_api.async_response
async def handle_learning_start(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: Dict[str, Any]) -> None:
    """Start capturing signals."""

    hub = _get_hub(hass, msg)
    await hub.async_start_learning()
    connection.send_result(msg["id"], {"active": True})


@websocket_api.websocket_command({vol.Required("type"): WS_TYPE_LEARNING_STOP, vol.Optional("entry_id"): str})
@websocket_api.async_response
async def handle_learning_stop(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: Dict[str, Any]) -> None:
    """Stop capturing signals."""

    hub = _get_hub(hass, msg)
    await hub.async_stop_learning()
    connection.send_result(msg["id"], {"active": False})


@websocket_api.websocket_command({vol.Required("type"): WS_TYPE_LEARNING_STATUS, vol.Optional("entry_id"): str})
@websocket_api.async_response
async def handle_learning_status(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: Dict[str, Any]) -> None:
    """Return the current learning state."""

    hub = _get_hub(hass, msg)
    connection.send_result(msg["id"], {"active": hub.learn_manager.is_active})


@websocket_api.websocket_command({vol.Required("type"): WS_TYPE_LEARNING_SUBSCRIBE, vol.Optional("entry_id"): str})
@callback
def handle_learning_subscribe(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: Dict[str, Any]) -> None:
    """Subscribe to learning state updates."""

    @callback
    def forward(payload: Dict[str, Any]) -> None:
        connection.send_message(websocket_api.event_message(msg["id"], payload))

    connection.subscriptions[msg["id"]] = async_dispatcher_connect(
        hass, SIGNAL_LEARNING_STATE, forward
    )
    connection.send_result(msg["id"])


@websocket_api.websocket_command({vol.Required("type"): WS_TYPE_SIGNALS_LIST, vol.Optional("entry_id"): str})
@websocket_api.async_response
async def handle_signals_list(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: Dict[str, Any]) -> None:
    """Return a list of currently captured signals."""

    hub = _get_hub(hass, msg)
    signals = await hub.learn_manager.async_list_signals()
    connection.send_result(msg["id"], {"signals": signals})


@websocket_api.websocket_command({vol.Required("type"): WS_TYPE_SIGNALS_SUBSCRIBE, vol.Optional("entry_id"): str})
@callback
def handle_signals_subscribe(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: Dict[str, Any]) -> None:
    """Subscribe to incoming signals."""

    @callback
    def forward(payload: Dict[str, Any]) -> None:
        connection.send_message(websocket_api.event_message(msg["id"], payload))

    connection.subscriptions[msg["id"]] = async_dispatcher_connect(
        hass, SIGNAL_SIGNAL_RECEIVED, forward
    )
    connection.send_result(msg["id"])


_DEVICE_CREATE_SCHEMA = websocket_api.BASE_COMMAND_MESSAGE_SCHEMA.extend(
    {
        vol.Required("type"): WS_TYPE_DEVICE_CREATE,
        vol.Required("name"): cv.string,
        vol.Required("device_type"): vol.In(["switch", "binary_sensor"]),
        vol.Required("signals"): {cv.string: cv.string},
        vol.Optional("metadata"): {cv.string: cv.Any()},
        vol.Optional("entry_id"): str,
    }
)


@websocket_api.websocket_command(_DEVICE_CREATE_SCHEMA)
@websocket_api.async_response
async def handle_device_create(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: Dict[str, Any]) -> None:
    """Create a device from captured signals."""

    hub = _get_hub(hass, msg)
    device = await hub.async_create_device(msg["name"], msg["device_type"], msg["signals"], msg.get("metadata"))
    connection.send_result(msg["id"], {"device": device.to_dict()})


@websocket_api.websocket_command({
    vol.Required("type"): WS_TYPE_DEVICE_DELETE,
    vol.Required("device_id"): cv.string,
    vol.Optional("entry_id"): str,
})
@websocket_api.async_response
async def handle_device_delete(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: Dict[str, Any]) -> None:
    """Delete a stored device."""

    hub = _get_hub(hass, msg)
    await hub.async_remove_device(msg["device_id"])
    connection.send_result(msg["id"], {})


@websocket_api.websocket_command({vol.Required("type"): WS_TYPE_DEVICE_LIST, vol.Optional("entry_id"): str})
@websocket_api.async_response
async def handle_device_list(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: Dict[str, Any]) -> None:
    """Return the list of stored devices."""

    hub = _get_hub(hass, msg)
    devices = [device.to_dict() for device in hub.iter_devices()]
    connection.send_result(msg["id"], {"devices": devices})


@websocket_api.websocket_command({vol.Required("type"): WS_TYPE_DEVICE_RELOAD, vol.Optional("entry_id"): str})
@websocket_api.async_response
async def handle_device_reload(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: Dict[str, Any]) -> None:
    """Reload devices from persistent storage."""

    hub = _get_hub(hass, msg)
    await hub.async_reload_devices()
    connection.send_result(msg["id"], {})
