from service_helper import ServiceHelper


class Vacuum(ServiceHelper):
    def initialize(self):
        #self.listen_state(self.clean, "binary_sensor.carsten_presence", old="off", new="on")
    
    def clean(self, entity, attribute, old, new, kwargs):
        self.call_service(
            "vacuum/send_command", entity_id="vacuum.xiaomi_vacuum_cleaner",
            command="app_segment_clean", params=room_list
        )
    

