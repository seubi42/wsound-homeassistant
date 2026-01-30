from __future__ import annotations

import asyncio
from typing import Any

from aiohttp import ClientError
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession


class WSoundApiError(Exception):
    pass


class WSoundApiClient:
    def __init__(self, hass: HomeAssistant, host: str, port: int) -> None:
        self._host = host
        self._port = port
        self._session = async_get_clientsession(hass)

    @property
    def base_url(self) -> str:
        return f"http://{self._host}:{self._port}"

    async def get_state(self) -> dict[str, Any]:
        url = f"{self.base_url}/json/state"
        try:
            async with self._session.get(url, timeout=10) as resp:
                resp.raise_for_status()
                data = await resp.json()
                if not isinstance(data, dict):
                    raise WSoundApiError("Invalid JSON response (expected object)")
                return data
        except (ClientError, asyncio.TimeoutError, ValueError) as e:
            raise WSoundApiError(str(e)) from e

    @staticmethod
    def parse_led_is_on(state_json: dict[str, Any]) -> bool:
        led = state_json.get("led", {})
        if isinstance(led, dict):
            v = led.get("state")
            if isinstance(v, str):
                return v.lower() == "on"
        return False

    async def set_led(self, on: bool) -> dict[str, Any]:
        state = "on" if on else "off"
        url = f"{self.base_url}/api/led"
        params = {"state": state}
        try:
            async with self._session.post(url, params=params, timeout=10) as resp:
                resp.raise_for_status()
                data = await resp.json()
                if not isinstance(data, dict):
                    raise WSoundApiError("Invalid JSON response (expected object)")
                if data.get("ok") is not True:
                    raise WSoundApiError(f"Device returned ok={data.get('ok')}")
                return data
        except (ClientError, asyncio.TimeoutError, ValueError) as e:
            raise WSoundApiError(str(e)) from e

    async def apply_defaults(self, folder: str, duration: int, fade: int, volume: int) -> dict[str, Any]:
        url = f"{self.base_url}/api/config/defaults"
        params = {
            "folder": folder,
            "duration": int(duration),
            "fade": int(fade),
            "volume": int(volume),
        }
        try:
            async with self._session.post(url, params=params, timeout=10) as resp:
                resp.raise_for_status()
                try:
                    data = await resp.json()
                    return data if isinstance(data, dict) else {"ok": True}
                except Exception:
                    return {"ok": True}
        except (ClientError, asyncio.TimeoutError, ValueError) as e:
            raise WSoundApiError(str(e)) from e

    async def scenario_start(
        self,
        folder: str | None = None,
        duration: int | None = None,
        fade: int | None = None,
        volume: int | None = None,
    ) -> dict[str, Any]:
        url = f"{self.base_url}/api/scenario/start"
        params: dict[str, Any] = {}
        if folder is not None:
            params["folder"] = folder
        if duration is not None:
            params["duration"] = int(duration)
        if fade is not None:
            params["fade"] = int(fade)
        if volume is not None:
            params["volume"] = int(volume)

        try:
            async with self._session.post(url, params=(params or None), timeout=10) as resp:
                resp.raise_for_status()
                try:
                    data = await resp.json()
                    return data if isinstance(data, dict) else {"ok": True}
                except Exception:
                    return {"ok": True}
        except (ClientError, asyncio.TimeoutError) as e:
            raise WSoundApiError(str(e)) from e

    async def scenario_stop(self) -> dict[str, Any]:
        url = f"{self.base_url}/api/scenario/stop"
        try:
            async with self._session.post(url, timeout=10) as resp:
                resp.raise_for_status()
                try:
                    data = await resp.json()
                    return data if isinstance(data, dict) else {"ok": True}
                except Exception:
                    return {"ok": True}
        except (ClientError, asyncio.TimeoutError) as e:
            raise WSoundApiError(str(e)) from e
