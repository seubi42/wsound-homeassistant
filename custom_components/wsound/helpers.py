from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN


def device_info(entry_id: str, host: str | None = None) -> DeviceInfo:
    name = f"WSound ({host})" if host else "WSound"
    return DeviceInfo(
        identifiers={(DOMAIN, entry_id)},
        name=name,
        manufacturer="WSound",
        model="WSound Node",
    )
