"""Core hub object for the RaspyRFM integration."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime
import logging
import socket
import uuid
from typing import Any, Dict, Iterable, List, Optional

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_send

from .const import (
    CONF_HOST,
    CONF_PORT,
    DEFAULT_PORT,
    DOMAIN,
    SIGNAL_DEVICE_REGISTRY_UPDATED,
    SIGNAL_DEVICE_REMOVED,
    SIGNAL_LEARNING_STATE,
    SIGNAL_SIGNAL_RECEIVED,
)
from .storage import RaspyRFMDeviceEntry, RaspyRFMDeviceStorage
from .gateway import RaspyRFMGateway
from .learn import LearnManager, LearnedSignal

_LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class ActiveSignal:
    """Representation of a signal currently known to the hub."""

    signal: LearnedSignal
    received_at: datetime
    source: tuple[str, int]


class RaspyRFMHub:
    """Bridge between Home Assistant and a RaspyRFM gateway."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self._hass = hass
        self._entry = entry
        self._gateway = RaspyRFMGateway(
            hass,
            entry.data.get(CONF_HOST, ""),
            entry.data.get(CONF_PORT, DEFAULT_PORT),
        )
        self._storage = RaspyRFMDeviceStorage(hass)
        self._learn_manager = LearnManager(hass, self)
        self._active_signals: Dict[str, ActiveSignal] = {}
        self._signals_lock = asyncio.Lock()

    @property
    def gateway(self) -> RaspyRFMGateway:
        """Return the gateway helper object."""

        return self._gateway

    @property
    def storage(self) -> RaspyRFMDeviceStorage:
        """Return the persistent storage helper."""

        return self._storage

    @property
    def learn_manager(self) -> LearnManager:
        """Return the signal learning manager."""

        return self._learn_manager

    async def async_setup(self) -> None:
        """Initialise hub resources."""

        await self._storage.async_load()

    async def async_unload(self) -> None:
        """Unload hub resources."""

        await self._learn_manager.async_stop()
        await self._storage.async_unload()

    async def async_update_entry(self, entry: ConfigEntry) -> None:
        """Handle entry updates."""

        self._entry = entry
        await self._gateway.async_update(  # type: ignore[no-untyped-call]
            entry.data.get(CONF_HOST, ""), entry.data.get(CONF_PORT, DEFAULT_PORT)
        )

    async def async_start_learning(self) -> None:
        """Start a learning session."""

        async with self._signals_lock:
            self._active_signals.clear()
        await self._learn_manager.async_start()

    async def async_stop_learning(self) -> None:
        """Stop an active learning session."""

        await self._learn_manager.async_stop()

    def iter_devices(self) -> Iterable[RaspyRFMDeviceEntry]:
        """Return all configured devices."""

        return self._storage.iter_devices()

    def get_device(self, device_id: str) -> Optional[RaspyRFMDeviceEntry]:
        """Return a device by id."""

        return self._storage.get_device(device_id)

    async def async_create_device(
        self,
        name: str,
        device_type: str,
        signals: Dict[str, str],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> RaspyRFMDeviceEntry:
        """Create a new device entry from learned signals."""

        device = RaspyRFMDeviceEntry(
            device_id=str(uuid.uuid4()),
            name=name,
            device_type=device_type,
            signals=signals,
            metadata=metadata or {},
        )
        await self._storage.async_add_or_update(device)
        async_dispatcher_send(self._hass, SIGNAL_DEVICE_REGISTRY_UPDATED, device.device_id)
        return device

    async def async_remove_device(self, device_id: str) -> None:
        """Remove a device entry."""

        await self._storage.async_remove(device_id)
        async_dispatcher_send(self._hass, SIGNAL_DEVICE_REMOVED, device_id)

    async def async_handle_learned_signal(self, signal: LearnedSignal, addr: tuple[str, int]) -> None:
        """Handle a signal received during a learning session."""

        async with self._signals_lock:
            self._active_signals[signal.uid] = ActiveSignal(
                signal=signal, received_at=datetime.utcnow(), source=addr
            )
        async_dispatcher_send(
            self._hass,
            SIGNAL_SIGNAL_RECEIVED,
            signal.to_dict(),
        )
        await self._maybe_match_devices(signal)

    async def _maybe_match_devices(self, signal: LearnedSignal) -> None:
        """Match a learned signal with configured devices and fire updates."""

        matched: List[str] = []
        for device in self._storage.iter_devices():
            if device.matches_signal(signal.payload):
                matched.append(device.device_id)

        if not matched:
            return

        for device_id in matched:
            async_dispatcher_send(self._hass, SIGNAL_DEVICE_REGISTRY_UPDATED, device_id)

    async def async_list_active_signals(self) -> List[Dict[str, Any]]:
        """Return a snapshot of all active signals."""

        async with self._signals_lock:
            return [signal.signal.to_dict() for signal in self._active_signals.values()]

    async def async_reload_devices(self) -> None:
        """Reload device information from disk."""

        await self._storage.async_load()
        async_dispatcher_send(self._hass, SIGNAL_DEVICE_REGISTRY_UPDATED, None)

    async def async_record_learning_state(self, active: bool) -> None:
        """Announce a change of the learning state."""

        async_dispatcher_send(self._hass, SIGNAL_LEARNING_STATE, {"active": active})

    async def async_send_raw(self, payload: str) -> None:
        """Send a raw UDP payload to the gateway."""

        await self._gateway.async_send_raw(payload)


async def resolve_host(host: str) -> str:
    """Resolve a host to an IP address."""

    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, socket.gethostbyname, host)
