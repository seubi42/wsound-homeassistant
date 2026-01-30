from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import WSoundCoordinator
from .helpers import device_info


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    coordinator: WSoundCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([WSoundLedSwitch(hass, entry.entry_id, coordinator)])


class WSoundLedSwitch(CoordinatorEntity[WSoundCoordinator], SwitchEntity):
    _attr_name = "LED"
    _attr_has_entity_name = True
    _attr_icon = "mdi:led-on"

    def __init__(self, hass, entry_id: str, coordinator: WSoundCoordinator) -> None:
        super().__init__(coordinator)
        self._hass = hass
        self._entry_id = entry_id
        self._attr_unique_id = f"{entry_id}_led"

    @property
    def device_info(self):
        host = self._hass.data[DOMAIN][self._entry_id].get("host")
        return device_info(self._entry_id, host)

    @property
    def is_on(self) -> bool:
        return self.coordinator.client.parse_led_is_on(self.coordinator.data)

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.client.set_led(True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.client.set_led(False)
        await self.coordinator.async_request_refresh()
