from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import WSoundCoordinator
from .helpers import device_info


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
    """Récupère les réglages préparés dans HA (folder, duration, fade, volume)."""
    return hass.data[DOMAIN][entry_id]["settings"]


class _BaseButton(CoordinatorEntity[WSoundCoordinator], ButtonEntity):
    _attr_has_entity_name = True

    def __init__(
        self,
        hass,
        entry_id: str,
        coordinator: WSoundCoordinator,
        name: str,
        uid_suffix: str,
        icon: str,
    ) -> None:
        super().__init__(coordinator)
        self._hass = hass
        self._entry_id = entry_id
        self._attr_name = name
        self._attr_unique_id = f"{entry_id}_{uid_suffix}"
        self._attr_icon = icon

    @property
    def device_info(self):
        host = self._hass.data[DOMAIN][self._entry_id].get("host")
        return device_info(self._entry_id, host)


class WSoundStartButton(_BaseButton):
    """Démarre un scénario avec les paramètres HA."""

    def __init__(self, hass, entry_id: str, coordinator: WSoundCoordinator) -> None:
        super().__init__(hass, entry_id, coordinator, "Start", "start", "mdi:play")

    async def async_press(self) -> None:
        s = _get_settings(self._hass, self._entry_id)

        await self.coordinator.client.scenario_start(
            folder=str(s.get("folder")),
            duration=int(s.get("duration")),
            fade=int(s.get("fade")),
            volume=int(s.get("volume")),
        )
        await self.coordinator.async_request_refresh()


class WSoundStartDefaultsButton(_BaseButton):
    """Démarre un scénario en utilisant les defaults firmware."""

    def __init__(self, hass, entry_id: str, coordinator: WSoundCoordinator) -> None:
        super().__init__(
            hass,
            entry_id,
            coordinator,
            "Start (defaults)",
            "start_defaults",
            "mdi:play-circle",
        )

    async def async_press(self) -> None:
        # Aucun paramètre → firmware utilise les defaults déjà définis
        await self.coordinator.client.scenario_start()
        await self.coordinator.async_request_refresh()


class WSoundApplyDefaultsButton(_BaseButton):
    """Applique les defaults côté firmware."""

    def __init__(self, hass, entry_id: str, coordinator: WSoundCoordinator) -> None:
        super().__init__(
            hass,
            entry_id,
            coordinator,
            "Apply defaults",
            "apply_defaults",
            "mdi:content-save-cog",
        )

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
    """Stoppe le scénario en cours."""

    def __init__(self, hass, entry_id: str, coordinator: WSoundCoordinator) -> None:
        super().__init__(hass, entry_id, coordinator, "Stop", "stop", "mdi:stop")

    async def async_press(self) -> None:
        await self.coordinator.client.scenario_stop()
        await self.coordinator.async_request_refresh()
