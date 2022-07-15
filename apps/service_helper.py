import appdaemon.plugins.hass.hassapi as hass


class ServiceHelper(hass.Hass):
    def __init__(self, ad, name, logging, args, config, app_config, global_vars):
        super().__init__(ad, name, logging, args, config, app_config, global_vars)

        self.condition_mapping = {
            "at_day": ("sun.sun", "above_horizon"),
            "at_night": ("sun.sun", "below_horizon"),
        }

    def check_conditions(self, only):
        entity, required_state = self.condition_mapping.get(only)
        return self.get_state(entity) == required_state

    def notify(self, who, message, only_away=True, **kwargs):
        if only_away:
            if not self.at_home(who):
                self.log(f"not at home, notifying")
                super().call_service(f"notify/{who}", message=message, **kwargs)
            else:
                self.log(
                    f"Will not notify because {who} is at home and notifications are set to only_away"
                )
        else:
            super().call_service(f"notify/{who}", message=message, **kwargs)

    def at_home(self, who):
        if self.get_state(f"group.{who}") == "home":
            return True
        return False

    def friendly_name(self, entity_id):
        return self.get_state(entity_id, attribute="friendly_name")

    def future_off(self, kwargs):
        entity = kwargs["entity"]
        self.turn_off(entity)

    def call_service(self, service, only=None, **kwargs):
        conditions_met = self.check_conditions(only) if only is not None else True

        if conditions_met:
            self.log(f"Calling {service}")
            return super().call_service(service, **kwargs)

        self.log(f"{service} not executed. Only {only}.")
