"""Constants for the LG webOS TV integration."""

import asyncio

import aiohttp
from aiowebostv import WebOsTvCommandError

from homeassistant.const import Platform

DOMAIN = "webostv"
PLATFORMS = [Platform.MEDIA_PLAYER]
DATA_HASS_CONFIG = "hass_config"
DEFAULT_NAME = "LG webOS TV"

ATTR_BUTTON = "button"
ATTR_CONFIG_ENTRY_ID = "entry_id"
ATTR_PAYLOAD = "payload"
ATTR_SOUND_OUTPUT = "sound_output"

CONF_ON_ACTION = "turn_on_action"
CONF_SOURCES = "sources"

SERVICE_BUTTON = "button"
SERVICE_COMMAND = "command"
SERVICE_SELECT_SOUND_OUTPUT = "select_sound_output"

LIVE_TV_APP_ID = "com.webos.app.livetv"

WEBOSTV_EXCEPTIONS = (
    ConnectionResetError,
    WebOsTvCommandError,
    aiohttp.ClientConnectorError,
    aiohttp.ServerDisconnectedError,
    aiohttp.WSMessageTypeError,
    asyncio.CancelledError,
    asyncio.TimeoutError,
)
