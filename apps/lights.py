import re
import unicodedata
from asyncio import sleep

from requests import RequestException
from service_helper import ServiceHelper


class Lights(ServiceHelper):
    def initialize(self):
        self.listen_state(
            self.lights_on,
            "binary_sensor.tur_kammer",
            new="on",
            light="light.decke_kammer",
            timer=300,
        )
        self.listen_state(
            self.lights_off,
            "binary_sensor.tur_kammer",
            new="off",
            light="light.decke_kammer",
        )

        # self.listen_event(self.light_control_kammer, "deconz_event")

    def light_control_kammer(self, entity, attribute, kwargs):
        if attribute.get("id") == "schalter_kammer" and attribute.get("event") == 1002:
            self.log(f"Event: entity {entity}, {attribute}")
            light = "light.decke_kammer"
            self.turn_on(entity_id=light)
            if timer:
                self.run_in(self.future_off, 10, entity=light)

    def lights_on(self, entity, attribute, old, new, kwargs):
        # self.log(f"{zone}.")
        light = kwargs["light"]
        timer = kwargs.get("timer")
        self.notify("carsten", f"Turn on {light}.")
        self.turn_on(entity_id=light)

        if timer:
            self.run_in(self.future_off, timer, entity=light)

    def lights_off(self, entity, attribute, old, new, kwargs):
        light = kwargs["light"]
        # self.log(f"Window closed in {zone}.")
        # self.notify("carsten", f"Turn off {light}.")
        self.turn_off(light)
