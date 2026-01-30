from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import WSoundCoordinator
from .helpers import device_info


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: WSoundCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities(
        [
            WSoundSensor(hass, coordinator, entry.entry_id, "Scenario state", "scenario_state",
                         lambda d: d.get("scenario", {}).get("state"),
                         "mdi:play-circle-outline", None, None, None),

            WSoundSensor(hass, coordinator, entry.entry_id, "Track", "track",
                         lambda d: d.get("scenario", {}).get("track"),
                         "mdi:music-note", None, None, None),

            WSoundSensor(hass, coordinator, entry.entry_id, "Time remaining", "time_remaining",
                         lambda d: d.get("scenario", {}).get("time_remaining"),
                         "mdi:timer-sand", "s", SensorDeviceClass.DURATION, SensorStateClass.MEASUREMENT),

            WSoundSensor(hass, coordinator, entry.entry_id, "Volume real", "volume_real",
                         lambda d: d.get("scenario", {}).get("volume_real"),
                         "mdi:volume-medium", None, None, SensorStateClass.MEASUREMENT),

            WSoundSensor(hass, coordinator, entry.entry_id, "Tracks in folder", "tracks_in_folder",
                         lambda d: d.get("dfplayer", {}).get("tracks_in_folder"),
                         "mdi:playlist-music", None, None, SensorStateClass.MEASUREMENT),
        ]
    )


class WSoundSensor(CoordinatorEntity[WSoundCoordinator], SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, hass, coordinator: WSoundCoordinator, entry_id: str, name: str, uid_suffix: str, getter,
                 icon: str, unit: str | None, device_class, state_class):
        super().__init__(coordinator)
        self._hass = hass
        self._entry_id = entry_id
        self._attr_name = name
        self._attr_unique_id = f"{entry_id}_{uid_suffix}"
        self._getter = getter
        self._attr_icon = icon
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = state_class

    @property
    def device_info(self):
        host = self._hass.data[DOMAIN][self._entry_id].get("host")
        return device_info(self._entry_id, host)

    @property
    def native_value(self):
        return self._getter(self.coordinator.data) if isinstance(self.coordinator.data, dict) else None
