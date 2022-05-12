from service_helper import ServiceHelper


class LocationActions(ServiceHelper):
    def initialize(self):
        self.listen_state(self.carsten_arrived_home, "binary_sensor.carsten_presence", old="off", new="on")
        self.listen_state(self.carsten_left_home, "binary_sensor.carsten_presence", old="on", new="off")
        self.listen_state(self.daniela_arrived_home, "binary_sensor.daniela_presence", old="off", new="on")
        self.listen_state(self.daniela_left_home, "binary_sensor.daniela_presence", old="on", new="off")

    def carsten_arrived_home(self, entity, attribute, old, new, kwargs):
        self.notify("carsten", f"{self.friendly_name(entity)} arrived home")

    def carsten_left_home(self, entity, attribute, old, new, kwargs):
        self.notify("carsten", f"{self.friendly_name(entity)} left home")

    def daniela_arrived_home(self, entity, attribute, old, new, kwargs):
        self.notify("carsten", f"{self.friendly_name(entity)} arrived home")

    def daniela_left_home(self, entity, attribute, old, new, kwargs):
        self.notify("carsten", f"{self.friendly_name(entity)} left home")

    def noone_home(self, entity, attribute, old, new, kwargs):
        pass
        # self.notify("carsten", f"{self.friendly_name(entity)} left home")

    def someone_home(self, entity, attribute, old, new, kwargs):
        pass
        # self.notify("carsten", f"{self.friendly_name(entity)} is still at home")

    def someone_left(self, entity, attribute, old, new, kwargs):
        pass
        # self.notify("carsten", f"{self.friendly_name(entity)} left home") 