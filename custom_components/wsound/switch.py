from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import WSoundCoordinator


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    coordinator: WSoundCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([WSoundLedSwitch(coordinator, entry.entry_id)])


class WSoundLedSwitch(CoordinatorEntity[WSoundCoordinator], SwitchEntity):
    _attr_name = "LED"
    _attr_has_entity_name = True

    def __init__(self, coordinator: WSoundCoordinator, entry_id: str) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_led"

    @property
    def is_on(self) -> bool:
        return self.coordinator.client.parse_led_is_on(self.coordinator.data)

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.client.set_led(True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.client.set_led(False)
        await self.coordinator.async_request_refresh()
