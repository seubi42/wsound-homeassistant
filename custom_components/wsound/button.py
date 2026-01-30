from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import WSoundCoordinator


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator: WSoundCoordinator = data["coordinator"]
    async_add_entities(
        [
            WSoundStartButton(hass, entry.entry_id, coordinator),
            WSoundStartDefaultsButton(hass, entry.entry_id, coordinator),
            WSoundApplyDefaultsButton(hass, entry.entry_id, coordinator),
            WSoundStopButton(hass, entry.entry_id, coordinator),
        ]
    )


def _get_settings(hass, entry_id: str) -> dict:
    return hass.data[DOMAIN][entry_id]["settings"]


class _BaseButton(CoordinatorEntity[WSoundCoordinator], ButtonEntity):
    _attr_has_entity_name = True

    def __init__(self, hass, entry_id: str, coordinator: WSoundCoordinator, name: str, uid_suffix: str) -> None:
        super().__init__(coordinator)
        self._hass = hass
        self._entry_id = entry_id
        self._attr_name = name
        self._attr_unique_id = f"{entry_id}_{uid_suffix}"


class WSoundStartButton(_BaseButton):
    def __init__(self, hass, entry_id: str, coordinator: WSoundCoordinator) -> None:
        super().__init__(hass, entry_id, coordinator, "Start", "start")

    async def async_press(self) -> None:
        s = _get_settings(self._hass, self._entry_id)
        folder = s.get("folder")
        duration = s.get("duration")
        fade = s.get("fade")
        volume = s.get("volume")

        await self.coordinator.client.scenario_start(
            folder=str(folder),
            duration=int(duration),
            fade=int(fade),
            volume=int(volume),
        )
        await self.coordinator.async_request_refresh()


class WSoundStartDefaultsButton(_BaseButton):
    def __init__(self, hass, entry_id: str, coordinator: WSoundCoordinator) -> None:
        super().__init__(hass, entry_id, coordinator, "Start (defaults)", "start_defaults")

    async def async_press(self) -> None:
        # sans paramètres → firmware utilise defaults déjà configurés
        await self.coordinator.client.scenario_start()
        await self.coordinator.async_request_refresh()


class WSoundApplyDefaultsButton(_BaseButton):
    def __init__(self, hass, entry_id: str, coordinator: WSoundCoordinator) -> None:
        super().__init__(hass, entry_id, coordinator, "Apply defaults", "apply_defaults")

    async def async_press(self) -> None:
        s = _get_settings(self._hass, self._entry_id)
        await self.coordinator.client.apply_defaults(
            folder=str(s.get("folder")),
            duration=int(s.get("duration")),
            fade=int(s.get("fade")),
            volume=int(s.get("volume")),
        )
        await self.coordinator.async_request_refresh()


class WSoundStopButton(_BaseButton):
    def __init__(self, hass, entry_id: str, coordinator: WSoundCoordinator) -> None:
        super().__init__(hass, entry_id, coordinator, "Stop", "stop")

    async def async_press(self) -> None:
        await self.coordinator.client.scenario_stop()
        await self.coordinator.async_request_refresh()
