from service_helper import ServiceHelper


class MediaPlayer(ServiceHelper):
    def initialize(self):
        self.listen_state(self.turn_off, "media_player.firetv_wohnzimmer", new="off")
        self.listen_state(self.set_tv_scene, "sun.sun", new="below_horizon")

        self.listen_state(
            self.set_tv_scene,
            "media_player.firetv_wohnzimmer",
            old="standby",
            new="playing",
        )

        self.listen_state(
            self.resume_media, "input_boolean.recently_playing", new="on", period=600
        )

        self.listen_state(
            self.turn_on_actions,
            "media_player.firetv_wohnzimmer",
            old="off",
            new="standby",
        )

    def resume_media(self, entity, attribute, old, new, kwargs):
        period = kwargs.get("period", 600)
        self.log(f"Recently played media was turned on. Will turn off in {period} sec.")
        self.run_in(self.recently_played_off, period)

    def recently_played_off(self, kwargs):
        self.log("Recently played turned off.")
        self.call_service(
            "input_boolean/turn_off",
            entity_id="input_boolean.recently_playing",
        )

    def turn_on_actions(self, entity, attribute, old, new, kwargs):
        self.log("Pausing media & setting volumes")
        self.call_service(
            "media_player/media_pause",
            entity_id="media_player.echo_wz",
        )
        self.call_service(
            "input_boolean/turn_on",
            entity_id="input_boolean.recently_playing",
        )
        self.call_service(
            "media_player/volume_set",
            entity_id="media_player.echo_wz",
            volume_level=0.8,
        )

    def turn_off(self, entity, attribute, old, new, kwargs):
        self.log("Turning off TV")
        self.call_service("switch/turn_off", entity_id="switch.tv")
        self.call_service(
            "hue/hue_activate_scene",
            group_name="WZ",
            scene_name="Gedimmt",
            only="at_night",
        )
        self.call_service(
            "media_player/volume_set",
            entity_id="media_player.echo_wz",
            volume_level=0.5,
        )

        if self.get_state("input_boolean.recently_playing") == "on":
            self.call_service(
                "media_player/media_play",
                entity_id="media_player.echo_wz",
            )

    def set_tv_scene(self, entity, attribute, old, new, kwargs):
        self.log("Playing")
        if self.get_state("media_player.firetv_wohnzimmer") == "playing":
            self.call_service(
                "hue/hue_activate_scene",
                group_name="WZ",
                scene_name="Fernsehabend",
                only="at_night",
            )
