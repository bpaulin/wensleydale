import logging

import voluptuous as vol

from homeassistant.components.light import Light, PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME, CONF_ADDRESS, CONF_DEVICES
import homeassistant.helpers.config_validation as cv
from brownpaperbag.bpbgate import BpbGate

DOMAIN = "brownpaperbag"
DEPENDENCIES=["brownpaperbag"]

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
    """Setup the BrownPaperBage Light platform."""
    #import OpenWebNet
    gate_data = hass.data[DOMAIN]
    #gate = BpbGate(gate_data[0],gate_data[1],gate_data[2])
    gate = gate_data[3]
    add_devices(BrownPaperBagLight(light,gate) for light in config[CONF_DEVICES])


class BrownPaperBagLight(Light):
    """Representation of an BrownPaperBag Light."""

    def __init__(self, light, gate: BpbGate):
        """Initialize an BrownPaperBageLight."""
        self._gate = gate
        self._light_id = light[CONF_ADDRESS]
        self._name = light[CONF_NAME]
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
