from service_helper import ServiceHelper
import re
from PyTado.interface import Tado
from requests import RequestException
import unicodedata


class Heating(ServiceHelper):
    def initialize(self):
        user = self.args["tado.user"]
        pw = self.args["tado.pw"]
        self.tado = self.setup(user, pw)
        self.listen_state(self.set_window_open, "binary_sensor", new="on", duration=10)
        self.listen_state(self.set_window_closed, "binary_sensor", new="off", duration=10)

    def set_window_open(self, entity, attribute, old, new, tado):
        match = re.match("binary_sensor.(tur|balkontur|fenster)_(\\w+)", entity)
        if match:
            zone = match.group(2)
            self.log(f"Window opened in {zone}.")
            self.notify("carsten", f"Window is open in {zone}. Turning off heating.")
            self.tado.setZoneOverlay(self.zone_mapping.get(zone), "MANUAL", power="OFF")

    def set_window_closed(self, entity, attribute, old, new, tado):
        match = re.match("binary_sensor.(tur|balkontur|fenster)_(\\w+)", entity)
        if match:
            zone = match.group(2)
            self.log(f"Window closed in {zone}.")
            self.notify("carsten", f"Window is closed in {zone}.")
            self.tado.resetZoneOverlay(self.zone_mapping.get(zone))

    def setup(self, user, password):
        """Connect to Tado and fetch the zones."""
        try:
            tado = Tado(user, password)
        except (RuntimeError, RequestException) as exc:
            self.log("Unable to connect: %s", exc, log="error_log", level="ERROR")
            return False
        return tado

    @property
    def zone_mapping(self):
        return {
            self.remove_accents(zone["name"].lower()): zone["id"] for zone in self.tado.getZones()
        }

    def remove_accents(self, input_str):
        nfkd_form = unicodedata.normalize("NFKD", input_str)
        return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

