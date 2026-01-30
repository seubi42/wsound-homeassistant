from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import WSoundCoordinator


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: WSoundCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities(
        [
            WSoundSensor(coordinator, entry.entry_id, "Scenario state", "scenario_state", lambda d: d.get("scenario", {}).get("state")),
            WSoundSensor(coordinator, entry.entry_id, "Track", "track", lambda d: d.get("scenario", {}).get("track")),
            WSoundSensor(coordinator, entry.entry_id, "Time remaining", "time_remaining", lambda d: d.get("scenario", {}).get("time_remaining")),
            WSoundSensor(coordinator, entry.entry_id, "Volume real", "volume_real", lambda d: d.get("scenario", {}).get("volume_real")),
            WSoundSensor(coordinator, entry.entry_id, "Tracks in folder", "tracks_in_folder", lambda d: d.get("dfplayer", {}).get("tracks_in_folder")),
        ]
    )


class WSoundSensor(CoordinatorEntity[WSoundCoordinator], SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator: WSoundCoordinator, entry_id: str, name: str, uid_suffix: str, getter):
        super().__init__(coordinator)
        self._attr_name = name
        self._attr_unique_id = f"{entry_id}_{uid_suffix}"
        self._getter = getter

    @property
    def native_value(self):
        return self._getter(self.coordinator.data) if isinstance(self.coordinator.data, dict) else None
