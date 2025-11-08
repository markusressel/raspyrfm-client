"""Constants for the RaspyRFM Home Assistant integration."""

from __future__ import annotations

from homeassistant.const import Platform

DOMAIN = "raspyrfm"
CONF_HOST = "host"
CONF_PORT = "port"
DEFAULT_PORT = 49880
DEFAULT_LISTEN_PORT = 49881

PLATFORMS: list[Platform] = [Platform.SWITCH, Platform.BINARY_SENSOR]

STORAGE_VERSION = 1
STORAGE_KEY = f"{DOMAIN}_devices"

SIGNAL_DEVICE_REGISTRY_UPDATED = "raspyrfm_device_registry_updated"
SIGNAL_DEVICE_REMOVED = "raspyrfm_device_removed"
SIGNAL_SIGNAL_RECEIVED = "raspyrfm_signal_received"
SIGNAL_LEARNING_STATE = "raspyrfm_learning_state"

PANEL_URL_PATH = "raspyrfm"
PANEL_ICON = "mdi:radio-tower"
PANEL_TITLE = "RaspyRFM"

WS_TYPE_PREFIX = "raspyrfm/"
WS_TYPE_LEARNING_START = WS_TYPE_PREFIX + "learning/start"
WS_TYPE_LEARNING_STOP = WS_TYPE_PREFIX + "learning/stop"
WS_TYPE_LEARNING_SUBSCRIBE = WS_TYPE_PREFIX + "learning/subscribe"
WS_TYPE_LEARNING_STATUS = WS_TYPE_PREFIX + "learning/status"
WS_TYPE_SIGNALS_LIST = WS_TYPE_PREFIX + "signals/list"
WS_TYPE_SIGNALS_SUBSCRIBE = WS_TYPE_PREFIX + "signals/subscribe"
WS_TYPE_DEVICE_CREATE = WS_TYPE_PREFIX + "device/create"
WS_TYPE_DEVICE_DELETE = WS_TYPE_PREFIX + "device/delete"
WS_TYPE_DEVICE_LIST = WS_TYPE_PREFIX + "devices/list"
WS_TYPE_DEVICE_RELOAD = WS_TYPE_PREFIX + "devices/reload"
