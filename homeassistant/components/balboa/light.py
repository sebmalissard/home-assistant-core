"""Support for Balboa Spa lights."""

from __future__ import annotations

from typing import Any, cast

from pybalboa import SpaControl
from pybalboa.enums import OffOnState, UnknownState

from homeassistant.components.light import ColorMode, LightEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import BalboaConfigEntry
from .entity import BalboaEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: BalboaConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the spa's lights."""
    spa = entry.runtime_data
    async_add_entities(BalboaLightEntity(control) for control in spa.lights)


class BalboaLightEntity(BalboaEntity, LightEntity):
    """Representation of a Balboa Spa light entity."""

    _attr_color_mode = ColorMode.ONOFF
    _attr_supported_color_modes = {ColorMode.ONOFF}

    def __init__(self, control: SpaControl) -> None:
        """Initialize a Balboa Spa light entity."""
        super().__init__(control.client, control.name)
        self._control = control
        self._attr_translation_key = (
            "light_of_n" if len(control.client.lights) > 1 else "only_light"
        )
        self._attr_translation_placeholders = {
            "index": f"{cast(int, control.index) + 1}"
        }

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the light off."""
        await self._control.set_state(OffOnState.OFF)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the light on."""
        await self._control.set_state(OffOnState.ON)

    @property
    def is_on(self) -> bool | None:
        """Return true if the light is on."""
        if self._control.state == UnknownState.UNKNOWN:
            return None
        return self._control.state != OffOnState.OFF
