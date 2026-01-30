from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import WSoundCoordinator
from .helpers import device_info


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: WSoundCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([WSoundDfPlayerReady(hass, coordinator, entry.entry_id)])


class WSoundDfPlayerReady(CoordinatorEntity[WSoundCoordinator], BinarySensorEntity):
    _attr_has_entity_name = True
    _attr_name = "DFPlayer ready"
    _attr_icon = "mdi:chip"

    def __init__(self, hass, coordinator: WSoundCoordinator, entry_id: str):
        super().__init__(coordinator)
        self._hass = hass
        self._entry_id = entry_id
        self._attr_unique_id = f"{entry_id}_dfplayer_ready"

    @property
    def device_info(self):
        host = self._hass.data[DOMAIN][self._entry_id].get("host")
        return device_info(self._entry_id, host)

    @property
    def is_on(self) -> bool:
        d = self.coordinator.data
        return bool(d.get("dfplayer", {}).get("ready")) if isinstance(d, dict) else False
