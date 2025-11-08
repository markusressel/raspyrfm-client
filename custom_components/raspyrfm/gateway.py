"""Helpers for interacting with the RaspyRFM UDP gateway."""

from __future__ import annotations
import logging
import socket

from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)


class RaspyRFMGateway:
    """Abstraction around the UDP based RaspyRFM gateway."""

    def __init__(self, hass: HomeAssistant, host: str, port: int) -> None:
        self._hass = hass
        self._host = host
        self._port = port

    @property
    def host(self) -> str:
        """Return the configured host."""

        return self._host

    @property
    def port(self) -> int:
        """Return the configured port."""

        return self._port

    async def async_update(self, host: str, port: int) -> None:
        """Update connection details."""

        self._host = host
        self._port = port

    async def async_send_raw(self, payload: str) -> None:
        """Send a raw payload to the gateway via UDP."""

        if not self._host:
            raise OSError("Gateway host not configured")

        def _send() -> None:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.settimeout(2)
                sock.sendto(payload.encode("utf-8"), (self._host, self._port))

        await self._hass.async_add_executor_job(_send)

    async def async_ping(self) -> None:
        """Attempt to contact the gateway."""

        await self.async_send_raw("PING")
