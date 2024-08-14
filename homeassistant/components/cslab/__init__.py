"""The csLights integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .cshome_master import CSHomeMaster

# List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS: list[Platform] = [
    Platform.COVER,
    Platform.LIGHT,
    Platform.SENSOR,
    Platform.SWITCH,
]

# Create ConfigEntry type alias with API object
# Rename type alias and update all entry annotations
type CSNameConfigEntry = ConfigEntry[CSHomeMaster]


# Update entry annotation
async def async_setup_entry(hass: HomeAssistant, entry: CSNameConfigEntry) -> bool:
    """Set up csLights from a config entry."""

    logger = logging.getLogger(__name__)

    # Create API instance
    csmaster = CSHomeMaster(hass, entry)

    # Store the csmaster object in hass.data using DOMAIN and entry_id as keys
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    hass.data[DOMAIN][entry.entry_id] = csmaster

    if not await csmaster.async_setup():
        logger.error("CSHomeMaster setup failed")
        return False

    # Forward the setup to the platform(s)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: CSNameConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
