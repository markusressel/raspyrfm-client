"""Base entity classes for the RaspyRFM integration."""

from __future__ import annotations

from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import Entity

from .const import DOMAIN, SIGNAL_DEVICE_REGISTRY_UPDATED
from .hub import RaspyRFMHub
from .storage import RaspyRFMDeviceEntry


class RaspyRFMEntity(Entity):
    """Common representation of a RaspyRFM entity."""

    _attr_should_poll = False

    def __init__(self, hub: RaspyRFMHub, device: RaspyRFMDeviceEntry) -> None:
        self._hub = hub
        self._device = device
        self._unsub_dispatcher = None

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()

        def _handle_update(device_id: str | None) -> None:
            if device_id is None or device_id == self._device.device_id:
                new_device = self._hub.get_device(self._device.device_id)
                if new_device:
                    self._device = new_device
                self.async_write_ha_state()

        self._unsub_dispatcher = async_dispatcher_connect(
            self.hass, SIGNAL_DEVICE_REGISTRY_UPDATED, _handle_update
        )

    async def async_will_remove_from_hass(self) -> None:
        if self._unsub_dispatcher is not None:
            self._unsub_dispatcher()
            self._unsub_dispatcher = None
        await super().async_will_remove_from_hass()

    @property
    def device_info(self) -> dict:
        return {
            "identifiers": {(DOMAIN, self._hub.gateway.host)},
            "manufacturer": "Seegel Systeme",
            "name": "RaspyRFM",
        }

    @property
    def unique_id(self) -> str:
        return self._device.device_id

    @property
    def name(self) -> str:
        return self._device.name
