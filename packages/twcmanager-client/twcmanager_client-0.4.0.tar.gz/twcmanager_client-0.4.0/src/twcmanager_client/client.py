import aiohttp
from typing import Any


class TWCManagerClient:
    """TWCManager client."""

    def __init__(self, host: str):
        """Construct a new TWCManager client."""
        self._host = host
        self._session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30))

    async def async_get_uuid(self) -> str:
        """Get the unique ID of the TWCManager."""
        return await self._async_get_text("http://" + self._host + ":8080/api/getUUID")

    async def async_get_config(self) -> dict[str, Any]:
        """Get the current configuration."""
        return await self._async_get_dict(
            "http://" + self._host + ":8080/api/getConfig"
        )

    async def async_get_policy(self) -> dict[str, Any]:
        """Get the policy configuration."""
        return await self._async_get_dict(
            "http://" + self._host + ":8080/api/getPolicy"
        )

    async def async_get_slave_twcs(self) -> dict[str, Any]:
        """Get a list of connected slave TWCs and their state."""
        return await self._async_get_dict(
            "http://" + self._host + ":8080/api/getSlaveTWCs"
        )

    async def async_get_status(self) -> dict[str, Any]:
        """Get the current status (charge rate, policy)."""
        return await self._async_get_dict(
            "http://" + self._host + ":8080/api/getStatus"
        )

    async def _async_get_text(self, path: str) -> str:
        async with self._session.get(path) as response:
            response.raise_for_status()
            return await response.text()

    async def _async_get_dict(self, path: str) -> dict[str, Any]:
        async with self._session.get(path) as response:
            response.raise_for_status()
            return await response.json()
