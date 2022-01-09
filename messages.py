from twilio.rest import Client
from secrets import Secrets
from pretty import pretty_print

class Messages:
    def __init__(self):
        self.secrets = Secrets()
        self.client = Client(self.secrets.account_sid, self.secrets.auth_token)
        self.places_already_sent = {}
    
    def send_text(self, sorted_distance, user, within_range):
        new = self.__new_places__(within_range, user)

        if len(new) == 0:
            print("Sending nothing")
        else:
            print(str(len(new)) + " new places within range!")
            message = "\nAvailable RAT tests! Here's a list:\n"
            for distance, place in new:
                message += pretty_print(distance, place)
            self.client.notify.services(self.secrets.text_service_id).notifications.create(
            to_binding='{"binding_type":"sms", "address": "' + user.phone_number + '"}', body=message)

    def __new_places__(self, within_range, user):
        new = []
        for distance, place in within_range:
            addr = place.get('address')
            if addr not in self.places_already_sent.get(user.phone_number, []):
                new.append((distance, place))
                if not self.places_already_sent.get(user.phone_number):
                    self.places_already_sent[user.phone_number] = set()
                self.places_already_sent[user.phone_number].add(addr)

        return new