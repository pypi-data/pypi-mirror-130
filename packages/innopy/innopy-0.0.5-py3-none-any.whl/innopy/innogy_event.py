class InnogyEvent():

    def __init__(self, evt):
        if "desc" in evt:
            self.desc = evt["desc"]
        
        self.timestamp = evt["timestamp"]
        self.type = evt["type"]


        if "properties" in evt:
            prop_dict = {}
            for prop_k in evt["properties"]:
                prop_dict.update({prop_k:{"value":evt["properties"][prop_k]}})

            self.properties_dict = prop_dict
        if "source" in evt:
            self.link_dict = evt["source"].replace('/capability/', '')