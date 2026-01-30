from __future__ import annotations

import voluptuous as vol

from .const import (
    CONF_FOLDERS_COUNT,
    CONF_POLL_INTERVAL,
    DEFAULT_FOLDERS_COUNT,
    DEFAULT_POLL_INTERVAL,
)


def options_schema(config_entry):
    current_folders = config_entry.options.get(CONF_FOLDERS_COUNT, DEFAULT_FOLDERS_COUNT)
    current_poll = config_entry.options.get(CONF_POLL_INTERVAL, DEFAULT_POLL_INTERVAL)

    return vol.Schema(
        {
            vol.Required(CONF_FOLDERS_COUNT, default=current_folders): vol.All(
                int, vol.Range(min=1, max=99)
            ),
            vol.Required(CONF_POLL_INTERVAL, default=current_poll): vol.All(
                int, vol.Range(min=2, max=300)
            ),
        }
    )
