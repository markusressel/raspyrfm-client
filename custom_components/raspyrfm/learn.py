"""Signal learning helper for the RaspyRFM integration."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
import logging
from typing import Any, Dict, List, Optional, Tuple

from homeassistant.core import HomeAssistant
from .const import DEFAULT_LISTEN_PORT

_LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class LearnedSignal:
    """Representation of a learned radio signal."""

    uid: str
    payload: str
    received: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Return a serialisable representation."""

        return {
            "uid": self.uid,
            "payload": self.payload,
            "received": self.received.isoformat(),
            "metadata": self.metadata,
        }


class RaspyRFMLearnProtocol(asyncio.DatagramProtocol):
    """Asyncio datagram protocol for capturing signals."""

    def __init__(self, manager: "LearnManager") -> None:
        self._manager = manager

    def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:
        payload = data.decode("utf-8", errors="ignore").strip()
        if not payload:
            return

        asyncio.create_task(self._manager.async_process_datagram(payload, addr))


class LearnManager:
    """Manage RaspyRFM learning sessions."""

    def __init__(self, hass: HomeAssistant, hub: "RaspyRFMHub") -> None:
        self._hass = hass
        self._hub = hub
        self._transport: Optional[asyncio.transports.DatagramTransport] = None
        self._active = False
        self._listen_port = DEFAULT_LISTEN_PORT
        self._signals: List[LearnedSignal] = []
        self._lock = asyncio.Lock()

    @property
    def is_active(self) -> bool:
        """Return whether learning is active."""

        return self._active

    async def async_start(self) -> None:
        """Start listening for incoming datagrams."""

        if self._active:
            return

        loop = asyncio.get_running_loop()
        self._transport, _ = await loop.create_datagram_endpoint(
            lambda: RaspyRFMLearnProtocol(self), local_addr=("0.0.0.0", self._listen_port)
        )
        self._signals.clear()
        self._active = True
        try:
            await self._hub.async_send_raw("RXSTART")
        except OSError:
            _LOGGER.debug("Unable to send RXSTART command to gateway")
        await self._hub.async_record_learning_state(True)

    async def async_stop(self) -> None:
        """Stop listening for signals."""

        if not self._active:
            return

        if self._transport is not None:
            self._transport.close()
            self._transport = None
        self._active = False
        try:
            await self._hub.async_send_raw("RXSTOP")
        except OSError:
            _LOGGER.debug("Unable to send RXSTOP command to gateway")
        await self._hub.async_record_learning_state(False)

    async def async_process_datagram(self, payload: str, addr: Tuple[str, int]) -> None:
        """Process an incoming UDP datagram."""

        if not payload:
            return

        signal = LearnedSignal(
            uid=f"sig_{len(self._signals)+1}",
            payload=payload,
            received=datetime.utcnow(),
            metadata={"source": addr[0], "port": addr[1]},
        )
        async with self._lock:
            self._signals.append(signal)
        await self._hub.async_handle_learned_signal(signal, addr)

    async def async_list_signals(self) -> List[Dict[str, Any]]:
        """Return a list of captured signals."""

        async with self._lock:
            return [signal.to_dict() for signal in self._signals]

    async def async_clear_signals(self) -> None:
        """Clear the signal buffer."""

        async with self._lock:
            self._signals.clear()
