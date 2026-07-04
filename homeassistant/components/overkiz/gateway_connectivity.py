"""Add gateway connectivity sensor."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from . import OverkizDataConfigEntry
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Toutes les 5 minutes suffit largement : la connectivité du gateway
# ne change pas seconde par seconde, inutile de saturer l'API Overkiz.
GATEWAY_UPDATE_INTERVAL = timedelta(minutes=5)


class OverkizGatewayCoordinator(DataUpdateCoordinator):
    """Coordinateur dédié qui interroge l'état des gateways."""

    def __init__(self, hass: HomeAssistant, client) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="overkiz_gateway_connectivity",
            update_interval=GATEWAY_UPDATE_INTERVAL,
        )
        self.client = client

    async def _async_update_data(self) -> dict:
        """Récupère la liste des gateways et leur état de connexion."""
        gateways = await self.client.get_gateways()
        return {gateway.id: gateway for gateway in gateways}


class OverkizGatewayConnectivitySensor(
    CoordinatorEntity[OverkizGatewayCoordinator], BinarySensorEntity
):
    """Binary sensor reflétant si le gateway Overkiz est bien connecté."""

    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_has_entity_name = True
    _attr_name = "Connectivité"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self, coordinator: OverkizGatewayCoordinator, gateway_id: str
    ) -> None:
        super().__init__(coordinator)
        self.gateway_id = gateway_id
        self._attr_unique_id = f"{gateway_id}-connectivity"
        self._attr_device_info = {"identifiers": {(DOMAIN, gateway_id)}}

    @property
    def is_on(self) -> bool:
        """True si le gateway est réellement en ligne."""
        gateway = self.coordinator.data.get(self.gateway_id)
        if gateway is None:
            return False

        return bool(gateway.alive) and gateway.connectivity.status != "DISCONNECTED"

    @property
    def extra_state_attributes(self) -> dict:
        gateway = self.coordinator.data.get(self.gateway_id)
        if gateway is None:
            return {}
        return {
            "alive": gateway.alive,
            "connectivity_status": gateway.connectivity.status,
            "update_status": str(gateway.update_status),
        }


async def async_setup_gateway_connectivity_sensors(
    hass: HomeAssistant,
    entry: OverkizDataConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Crée les capteurs de connectivité pour chaque gateway associé."""
    client = entry.runtime_data.coordinator.client

    gateway_coordinator = OverkizGatewayCoordinator(hass, client)
    await gateway_coordinator.async_config_entry_first_refresh()

    entities = [
        OverkizGatewayConnectivitySensor(gateway_coordinator, gateway_id)
        for gateway_id in gateway_coordinator.data
    ]
    async_add_entities(entities)