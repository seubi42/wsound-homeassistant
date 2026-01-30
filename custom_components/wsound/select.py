from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.restore_state import RestoreEntity

from .const import DOMAIN, DEFAULT_FOLDER, CONF_FOLDERS_COUNT, DEFAULT_FOLDERS_COUNT
from .helpers import device_info


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([WSoundFolderSelect(hass, entry.entry_id, entry)])


class WSoundFolderSelect(SelectEntity, RestoreEntity):
    _attr_name = "Folder"
    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.CONFIG
    _attr_icon = "mdi:folder-music"

    def __init__(self, hass, entry_id: str, entry) -> None:
        self._hass = hass
        self._entry_id = entry_id
        self._entry = entry
        self._attr_unique_id = f"{entry_id}_folder"
        self._current = DEFAULT_FOLDER

        folders_count = int(entry.options.get(CONF_FOLDERS_COUNT, DEFAULT_FOLDERS_COUNT))
        self._attr_options = [f"{i:02d}" for i in range(1, folders_count + 1)]

        # if default folder not in options, pick first
        if self._current not in self._attr_options and self._attr_options:
            self._current = self._attr_options[0]

    @property
    def device_info(self):
        host = self._hass.data[DOMAIN][self._entry_id].get("host")
        return device_info(self._entry_id, host)

    @property
    def current_option(self) -> str:
        return self._current

    async def async_added_to_hass(self) -> None:
        last = await self.async_get_last_state()
        if last and last.state in self.options:
            self._current = last.state

        self._hass.data[DOMAIN][self._entry_id]["settings"]["folder"] = self._current

    async def async_select_option(self, option: str) -> None:
        self._current = option
        self._hass.data[DOMAIN][self._entry_id]["settings"]["folder"] = self._current
        self.async_write_ha_state()
