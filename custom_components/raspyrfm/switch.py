"""Switch platform for RaspyRFM."""

from __future__ import annotations

from typing import Any, Dict

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import DOMAIN, SIGNAL_DEVICE_REGISTRY_UPDATED, SIGNAL_SIGNAL_RECEIVED
from .entity import RaspyRFMEntity
from .hub import RaspyRFMHub
from .storage import RaspyRFMDeviceEntry


async def async_setup_entry(hass, entry, async_add_entities):
    hub: RaspyRFMHub = hass.data[DOMAIN][entry.entry_id]
    entities: Dict[str, RaspyRFMSwitch] = {}

    @callback
    def _ensure_entities() -> None:
        new_entities = []
        for device in hub.storage.iter_devices_by_type("switch"):
            if device.device_id in entities:
                continue
            entity = RaspyRFMSwitch(hub, device)
            entities[device.device_id] = entity
            new_entities.append(entity)
        if new_entities:
            async_add_entities(new_entities)

    _ensure_entities()

    @callback
    def handle_device_update(device_id: str | None) -> None:
        if device_id is None or device_id not in entities:
            _ensure_entities()

    entry.async_on_unload(
        async_dispatcher_connect(hass, SIGNAL_DEVICE_REGISTRY_UPDATED, handle_device_update)
    )


class RaspyRFMSwitch(RaspyRFMEntity, SwitchEntity):
    """Representation of a learned switch."""

    def __init__(self, hub: RaspyRFMHub, device: RaspyRFMDeviceEntry) -> None:
        super().__init__(hub, device)
        self._attr_is_on = False
        self._signal_unsub = None

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()

        @callback
        def handle_signal(event: Dict[str, Any]) -> None:
            payload = event.get("payload")
            if payload == self._device.signals.get("on"):
                self._attr_is_on = True
                self.async_write_ha_state()
            elif payload == self._device.signals.get("off"):
                self._attr_is_on = False
                self.async_write_ha_state()

        self._signal_unsub = async_dispatcher_connect(
            self.hass, SIGNAL_SIGNAL_RECEIVED, handle_signal
        )

    async def async_will_remove_from_hass(self) -> None:
        if self._signal_unsub is not None:
            self._signal_unsub()
            self._signal_unsub = None
        await super().async_will_remove_from_hass()

    async def async_turn_on(self, **kwargs: Any) -> None:
        signal = self._device.signals.get("on")
        if signal is None:
            raise ValueError("No ON signal stored for this device")
        await self._hub.async_send_raw(signal)
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        signal = self._device.signals.get("off")
        if signal is None:
            raise ValueError("No OFF signal stored for this device")
        await self._hub.async_send_raw(signal)
        self._attr_is_on = False
        self.async_write_ha_state()
