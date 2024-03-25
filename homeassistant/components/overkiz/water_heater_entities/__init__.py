"""Water heater entities for the Overkiz (by Somfy) integration."""

from pyoverkiz.enums.ui import UIWidget

from .atlantic_dhw import AtlanticDHW
from .atlantic_pass_apc_dhw import AtlanticPassAPCDHW
from .domestic_hot_water_production import DomesticHotWaterProduction
from .hitachi_dhw import HitachiDHW

WIDGET_TO_WATER_HEATER_ENTITY = {
    UIWidget.ATLANTIC_PASS_APC_DHW: AtlanticPassAPCDHW,
    UIWidget.DOMESTIC_HOT_WATER_PRODUCTION: DomesticHotWaterProduction,
    UIWidget.HITACHI_DHW: HitachiDHW,
}

CONTROLLABLE_NAME_TO_WATER_HEATER_ENTITY = {
    "modbuslink:AtlanticDomesticHotWaterProductionMBLComponent": AtlanticDHW,
}
