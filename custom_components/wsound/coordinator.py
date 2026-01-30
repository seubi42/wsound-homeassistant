from __future__ import annotations

from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import WSoundApiClient, WSoundApiError
from .const import DOMAIN, COORDINATOR_UPDATE_INTERVAL_SECONDS


class WSoundCoordinator(DataUpdateCoordinator[dict]):
    def __init__(self, hass, client: WSoundApiClient) -> None:
        super().__init__(
            hass,
            logger=__import__("logging").getLogger(__name__),
            name=DOMAIN,
            update_interval=timedelta(seconds=COORDINATOR_UPDATE_INTERVAL_SECONDS),
        )
        self.client = client

    async def _async_update_data(self) -> dict:
        try:
            return await self.client.get_state()
        except WSoundApiError as e:
            raise UpdateFailed(str(e)) from e
