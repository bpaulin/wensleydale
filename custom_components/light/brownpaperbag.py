import logging

import voluptuous as vol

from homeassistant.components.light import Light, PLATFORM_SCHEMA
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
    """Setup the BrownPaperBage Light platform."""

    host = config.get(CONF_HOST)
    port = config.get(CONF_PORT)
    password = config.get(CONF_PASSWORD)

    # Setup connection with devices/cloud
    gate = BpbGate(host, port, password)
    gate.set_logger(_LOGGER)
    gate.connect()

    # @todo Verify that passed in configuration works

    # Add devices
    ids = gate.get_light_ids()
    _LOGGER.info(','.join(ids))
    add_devices(BrownPaperBagLight(light_id, gate) for light_id in ids)


class BrownPaperBagLight(Light):
    """Representation of an BrownPaperBag Light."""

    def __init__(self, light_id, gate: BpbGate):
        """Initialize an BrownPaperBageLight."""
        self._gate = gate
        self._light_id = light_id
        self._name = light_id
        self._state = None

    @property
    def name(self):
        """Return the display name of this light."""
        return self._name

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._state

    def turn_on(self, **kwargs):
        """Instruct the light to turn on."""
        self._gate.turn_on_light(self._light_id)

    def turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        self._gate.turn_off_light(self._light_id)

    def update(self):
        """Fetch new state data for this light."""
        self._state = self._gate.is_light_on(self._light_id)