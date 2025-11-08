"""Persistent storage for RaspyRFM devices."""

"""Persistent storage helpers for RaspyRFM devices."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .const import STORAGE_KEY, STORAGE_VERSION


@dataclass(slots=True)
class RaspyRFMDeviceEntry:
    """Representation of a configured device."""

    device_id: str
    name: str
    device_type: str
    signals: Dict[str, str]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation."""

        return {
            "device_id": self.device_id,
            "name": self.name,
            "device_type": self.device_type,
            "signals": self.signals,
            "metadata": self.metadata,
        }

    def matches_signal(self, payload: str) -> bool:
        """Return True if the payload matches this device."""

        return payload in self.signals.values()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RaspyRFMDeviceEntry":
        """Create an instance from stored data."""

        return cls(
            device_id=data["device_id"],
            name=data["name"],
            device_type=data.get("device_type", "switch"),
            signals=data.get("signals", {}),
            metadata=data.get("metadata", {}),
        )


class RaspyRFMDeviceStorage:
    """Storage helper managing device persistence."""

    def __init__(self, hass: HomeAssistant) -> None:
        self._hass = hass
        self._store: Store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
        self._devices: Dict[str, RaspyRFMDeviceEntry] = {}

    async def async_load(self) -> None:
        """Load device information from disk."""

        data = await self._store.async_load()
        if not data:
            self._devices = {}
            return

        devices: List[RaspyRFMDeviceEntry] = [
            RaspyRFMDeviceEntry.from_dict(item) for item in data.get("devices", [])
        ]
        self._devices = {device.device_id: device for device in devices}

    async def async_unload(self) -> None:
        """Flush changes to disk."""

        await self._store.async_save({"devices": [device.to_dict() for device in self._devices.values()]})

    def iter_devices(self) -> Iterable[RaspyRFMDeviceEntry]:
        """Iterate over all devices."""

        return list(self._devices.values())

    def iter_devices_by_type(self, device_type: str) -> Iterable[RaspyRFMDeviceEntry]:
        """Iterate over devices of a specific type."""

        return [device for device in self._devices.values() if device.device_type == device_type]

    def get_device(self, device_id: str) -> Optional[RaspyRFMDeviceEntry]:
        """Return a device by id."""

        return self._devices.get(device_id)

    async def async_add_or_update(self, device: RaspyRFMDeviceEntry) -> None:
        """Persist a device entry."""

        self._devices[device.device_id] = device
        await self._store.async_save({"devices": [d.to_dict() for d in self._devices.values()]})

    async def async_remove(self, device_id: str) -> None:
        """Remove a device entry."""

        if device_id in self._devices:
            self._devices.pop(device_id)
            await self._store.async_save({"devices": [d.to_dict() for d in self._devices.values()]})
