from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import WSoundCoordinator


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: WSoundCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([WSoundDfPlayerReady(coordinator, entry.entry_id)])


class WSoundDfPlayerReady(CoordinatorEntity[WSoundCoordinator], BinarySensorEntity):
    _attr_has_entity_name = True
    _attr_name = "DFPlayer ready"

    def __init__(self, coordinator: WSoundCoordinator, entry_id: str):
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_dfplayer_ready"

    @property
    def is_on(self) -> bool:
        d = self.coordinator.data
        return bool(d.get("dfplayer", {}).get("ready")) if isinstance(d, dict) else False
