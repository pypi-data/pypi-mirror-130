#import .innopy_device_types
from pprint import pprint, pformat
import logging
import colorlog
_LOGGER = logging.getLogger(__name__)


def create_devices(innogy_client, device):
    devices = []
    
    i = InnogyDevice(innogy_client, device)

    return  i

class InnogyDevice():

    def __init__(self, innogy_client, device):
        self.client = innogy_client
        self._set_data(device)
        _LOGGER.info("creating device: ", device["id"])

    def _set_data(self,device):
        self.config_dict = device["config"]
        
        self.id = device["id"]
        
        self.manufacturer = device["manufacturer"]
        self.product = device["product"]
        self.serialnumber = device["serialNumber"]
        self.type = device["type"]
        self.version = device["version"]

        #TODO: Handle tags?

        if "device_state" in device:
            state_dict = {}
            for state in device["device_state"]:
                state_dict.update({state:{"value":device["device_state"][state]["value"], "lastchanged":device["device_state"][state]["lastChanged"]}})

            self.device_state_dict = state_dict

        if "resolved_capabilities" in device:
            capabilities_dict = {}
            for cap in device["resolved_capabilities"]:
                cap_id = cap["value"]
                for resolved in cap["resolved"]:
                    capabilities_dict.update({resolved:{"value": cap["resolved"][resolved]["value"], "id": cap_id}})
            self.capabilities_dict = capabilities_dict


    def update(self):
        _LOGGER.info("updating device...")
        device_data = self.client.get_full_device_by_id(self.id)
        self._set_data(device_data)