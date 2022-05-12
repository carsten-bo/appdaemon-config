from service_helper import ServiceHelper

class TelegramService(ServiceHelper):
    def initialize(self):
        self.listen_state(self.test, "binary_sensor.fenster_buro")
        self.listen_event(self.receive, 'telegram_command')
        self.listen_event(self.receive_callback, 'telegram_callback')

    def test(self, entity, attribute, old, new, kwargs): 
        self.send("Test") 

    def send(self, message): 
        keyboard = [[[("At Home", "/at_home"), ("Away", "/away")]]]
        self.notify("carsten", message=f"{keyboard}")

    def receive(self, event_id, payload_event, *args):
        assert event_id == 'telegram_command'
        user_id = payload_event['user_id']
        command = payload_event['command']
 
        if command == "/at_home":
            self.notify("carsten","HOME1")
        if command == "/away":
            self.notify("carsten","AWAY1")
    
    def receive_callback(self, event_id, payload_event, *args):
        assert event_id == 'telegram_callback'
        data_callback = payload_event['data']
        callback_id = payload_event['id']
 
        if data_callback == "/at_home":
            self.send("HOME")
        if data_callback == "/away":
            self.send("AWAY")