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
        self.config_dict = device["config"]["name"]
        
        self.id = device["id"]
        
        self.manufacturer = device["manufacturer"]
        self.product = device["product"]
        self.serialnumber = device["serialNumber"]
        self.type = device["type"]
        self.version = device["version"]

        #TODO: Handle tags?

        if "device_state" in device:
            state_dict = {}
            if "updateAvailable" in device["device_state"]:
                state = device["device_state"]["updateAvailable"]
                state_dict.update({"updateAvailable":{"value":state["value"], "lastchanged":state["lastChanged"]}})

            self.device_state_dict = state_dict

        if "capabilities" in device:
            capabilities_dict = {}
            for cap in device["capabilities"]:
                cap_id = cap.replace('/capability/','')
                capabilities_dict.update({cap_id:{"id": cap_id}})
            self.capabilities_dict = capabilities_dict

        if "Location" in device:
            locations_dict = {}
            for loc in device["Location"]:
                loc_id = loc["value"]
                resolved = loc["resolved"]
                loc_name = resolved[0]["value"]
                loc_type = resolved[1]["value"]
                locations_dict.update({loc_name:{"id": loc_id, "type":loc_type}})
            self.location_dict = locations_dict

    def update(self):
        _LOGGER.info("updating device...")
        device_data = self.client.get_full_device_by_id(self.id)
        self._set_data(device_data)