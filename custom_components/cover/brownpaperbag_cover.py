import logging

import voluptuous as vol

from homeassistant.components.cover import (CoverDevice, PLATFORM_SCHEMA)
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_PORT
import homeassistant.helpers.config_validation as cv
from brownpaperbag.bpbgate import BpbGate

REQUIREMENTS = ['brownpaperbag']

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_PORT, default=20000): cv.positive_int,
    vol.Required(CONF_PASSWORD): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the BrownPaperBage Cover platform."""

    host = config.get(CONF_HOST)
    port = config.get(CONF_PORT)
    password = config.get(CONF_PASSWORD)

    # Setup connection with devices/cloud
    gate = BpbGate(host, port, password)
    gate.set_logger(_LOGGER)
    gate.connect()

    # @todo Verify that passed in configuration works

    # Add devices
    ids = gate.get_cover_ids()
    _LOGGER.info(','.join(ids))
    add_devices(BrownPaperBagCover(cover_id, gate) for cover_id in ids)


class BrownPaperBagCover(CoverDevice):
    """Representation of BrownPaperBag cover."""

    def __init__(self, cover_id, gate: BpbGate):
        """Initialize the cover."""
        self._gate = gate
        self._cover_id = cover_id
        self._name = cover_id

    # @property
    # def should_poll(self):
    #     """No polling needed."""
    #     return False

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
