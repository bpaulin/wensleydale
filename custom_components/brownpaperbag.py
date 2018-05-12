import logging
import voluptuous as vol

from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_PORT, CONF_NAME, CONF_DEVICES

import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DOMAIN = "brownpaperbag"
#DEPENDENCIES = []
REQUIREMENTS = ['brownpaperbag==0.0.2']

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_PORT, default = '20000'): cv.string,
    })
}, extra=vol.ALLOW_EXTRA)

def setup(hass,config):
    from brownpaperbag.bpbgate import BpbGate

    host = config[DOMAIN].get(CONF_HOST)
    port = config[DOMAIN].get(CONF_PORT)
    password = config[DOMAIN].get(CONF_PASSWORD)
    gate = (host,port,password)
    hass.data[DOMAIN] = gate
    return True
