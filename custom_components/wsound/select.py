from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.helpers.restore_state import RestoreEntity

from .const import DOMAIN, DEFAULT_FOLDER

FOLDER_OPTIONS = [f"{i:02d}" for i in range(1, 11)]  # 01..10


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([WSoundFolderSelect(hass, entry.entry_id)])


class WSoundFolderSelect(SelectEntity, RestoreEntity):
    _attr_name = "Folder"
    _attr_has_entity_name = True
    _attr_options = FOLDER_OPTIONS

    def __init__(self, hass, entry_id: str) -> None:
        self._hass = hass
        self._entry_id = entry_id
        self._attr_unique_id = f"{entry_id}_folder"
        self._current = DEFAULT_FOLDER

    @property
    def current_option(self) -> str:
        return self._current

    async def async_added_to_hass(self) -> None:
        last = await self.async_get_last_state()
        if last and last.state in self.options:
            self._current = last.state
        # store
        self._hass.data[DOMAIN][self._entry_id]["settings"]["folder"] = self._current

    async def async_select_option(self, option: str) -> None:
        self._current = option
        self._hass.data[DOMAIN][self._entry_id]["settings"]["folder"] = self._current
        self.async_write_ha_state()
