import logging

import voluptuous as vol

from homeassistant.components.cover import (CoverDevice, PLATFORM_SCHEMA, SUPPORT_OPEN, SUPPORT_CLOSE, SUPPORT_STOP, STATE_OPENING, STATE_CLOSING)
from homeassistant.const import CONF_NAME, CONF_ADDRESS, CONF_DEVICES
import homeassistant.helpers.config_validation as cv
from brownpaperbag.bpbgate import BpbGate, COVER_CLOSING, COVER_OPENING

DOMAIN = "brownpaperbag"
DEPENDENCIES = ['brownpaperbag']

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_DEVICES): vol.All(cv.ensure_list, [
        {
            vol.Required(CONF_NAME): cv.string,
            vol.Required(CONF_ADDRESS): cv.string,
        }
    ])
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the BrownPaperBage Cover platform."""
    gate_data = hass.data[DOMAIN]
    gate = gate_data['gate']
    add_devices(BrownPaperBagCover(cover, gate) for cover in config[CONF_DEVICES])
    
    add_devices(
        BrownPaperBagCover({CONF_NAME:address, CONF_ADDRESS:address}, gate)
        for address
        in gate_data['covers']
        if address not in
            [cover[CONF_ADDRESS] for cover in config[CONF_DEVICES]]
    )

class BrownPaperBagCover(CoverDevice):
    """Representation of BrownPaperBag cover."""

    def __init__(self, cover, gate: BpbGate):
        """Initialize the cover."""
        self._gate = gate
        self._cover_id = cover[CONF_ADDRESS]
        self._name = cover[CONF_NAME]
        self._state = None
        self._supported_features = (SUPPORT_OPEN | SUPPORT_CLOSE | SUPPORT_STOP)

    @property
    def name(self):
        """Return the name of the cover."""
        return self._name

    @property
    def is_closed(self):
        """Return if the cover is closed."""
        return None

    def open_cover(self, **kwargs):
        """Move the cover."""
        self._gate.open_cover(self._cover_id)

    def close_cover(self, **kwargs):
        """Move the cover down."""
        self._gate.close_cover(self._cover_id)

    def stop_cover(self, **kwargs):
        """Stop the cover."""
        self._gate.stop_cover(self._cover_id)

    def update(self):
        self._state = self._gate.get_cover_state(self._cover_id)
