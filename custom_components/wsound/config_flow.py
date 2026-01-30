from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.exceptions import HomeAssistantError

from .api import WSoundApiClient, WSoundApiError
from .const import DOMAIN, CONF_HOST, CONF_PORT, DEFAULT_PORT


class WSoundConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST].strip()
            port = int(user_input[CONF_PORT])

            try:
                await self._validate_input(host, port)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:
                errors["base"] = "unknown"
            else:
                # Unique ID simple (tu pourras l’améliorer plus tard avec un /json/info)
                await self.async_set_unique_id(f"wsound_{host}_{port}")
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=f"WSound ({host})",
                    data={CONF_HOST: host, CONF_PORT: port},
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST, default="wsound-b3f8.local"): str,
                vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    async def _validate_input(self, host: str, port: int) -> None:
        client = WSoundApiClient(self.hass, host, port)
        try:
            await client.get_state()
        except WSoundApiError as e:
            raise CannotConnect from e


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""
