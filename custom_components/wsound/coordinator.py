from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import WSoundApiClient, WSoundApiError
from .const import DOMAIN, CONF_POLL_INTERVAL, DEFAULT_POLL_INTERVAL

_LOGGER = logging.getLogger(__name__)


class WSoundCoordinator(DataUpdateCoordinator[dict]):
    def __init__(self, hass, client: WSoundApiClient, poll_interval: int) -> None:
        super().__init__(
            hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=poll_interval),
        )
        self.client = client

    async def _async_update_data(self) -> dict:
        try:
            return await self.client.get_state()
        except WSoundApiError as e:
            raise UpdateFailed(str(e)) from e
