from __future__ import annotations

from homeassistant.core import HomeAssistant

from .api import WSoundApiClient
from .const import DOMAIN, PLATFORMS, CONF_HOST, CONF_PORT
from .coordinator import WSoundCoordinator


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry) -> bool:
    hass.data.setdefault(DOMAIN, {})

    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]

    client = WSoundApiClient(hass, host, port)
    coordinator = WSoundCoordinator(hass, client)

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {"client": client, "coordinator": coordinator}

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
