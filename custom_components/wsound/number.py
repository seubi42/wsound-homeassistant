from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.restore_state import RestoreEntity

from .const import (
    DOMAIN,
    VOLUME_MIN, VOLUME_MAX, VOLUME_DEFAULT,
    FADE_MIN, FADE_MAX, FADE_DEFAULT,
    DURATION_MIN, DURATION_MAX, DURATION_DEFAULT,
)
from .helpers import device_info


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities(
        [
            WSoundNumber(hass, entry.entry_id, "Volume", "volume", VOLUME_MIN, VOLUME_MAX, VOLUME_DEFAULT, "mdi:volume-high", None),
            WSoundNumber(hass, entry.entry_id, "Fade", "fade", FADE_MIN, FADE_MAX, FADE_DEFAULT, "mdi:fade", "s"),
            WSoundNumber(hass, entry.entry_id, "Duration", "duration", DURATION_MIN, DURATION_MAX, DURATION_DEFAULT, "mdi:timer-outline", "s"),
        ]
    )


class WSoundNumber(NumberEntity, RestoreEntity):
    _attr_has_entity_name = True
    _attr_mode = NumberMode.BOX
    _attr_step = 1
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, hass, entry_id: str, name: str, key: str,
                 min_v: int, max_v: int, default: int, icon: str, unit: str | None) -> None:
        self._hass = hass
        self._entry_id = entry_id
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"{entry_id}_{key}"
        self._attr_native_min_value = float(min_v)
        self._attr_native_max_value = float(max_v)
        self._attr_icon = icon
        self._attr_native_unit_of_measurement = unit
        self._value = int(default)

    @property
    def device_info(self):
        host = self._hass.data[DOMAIN][self._entry_id].get("host")
        return device_info(self._entry_id, host)

    @property
    def native_value(self) -> float:
        return float(self._value)

    async def async_added_to_hass(self) -> None:
        last = await self.async_get_last_state()
        if last and last.state not in (None, "unknown", "unavailable"):
            try:
                self._value = int(float(last.state))
            except Exception:
                pass
        self._hass.data[DOMAIN][self._entry_id]["settings"][self._key] = int(self._value)

    async def async_set_native_value(self, value: float) -> None:
        self._value = int(value)
        self._hass.data[DOMAIN][self._entry_id]["settings"][self._key] = int(self._value)
        self.async_write_ha_state()
