#!/usr/bin/python3
# Imports already in python/installed via pip
import requests
import geopy.distance
import time
from twilio.rest import Client
# Imports of files in project
from secrets import Secrets
import users


SECRETS = Secrets()
ACCOUNT_SID = SECRETS.account_sid
AUTH_TOKEN = SECRETS.auth_token
CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)

USER = users.init_users()[0]
HOME_COORDS = (USER.lat, USER.lng)
WITHIN_RANGE = USER.range

PLACES_ALREADY_SENT = set()

def main(): 
    places = get_json()
    sorted_distance = get_sorted_distances(places)
    
    for x in range(5):
        distance, place = sorted_distance[x]
        pretty_print(distance, place)
    print()

    send_text(sorted_distance)

def send_text(sorted_distance):
    within_range = places_within_range(sorted_distance)
    new = new_places(within_range)

    if len(new) == 0:
        print("Sending nothing")
    else:
        print(str(len(new)) + " new places within range!")
        message = "\nAvailable RAT tests! Here's a list:\n"
        for distance, place in new:
            message += pretty_print(distance, place)
        notification = CLIENT.notify.services(SECRETS.text_service_id).notifications.create(
        to_binding='{"binding_type":"sms", "address": "' + USER.phone_number + '"}',
        body=message)

def new_places(within_range):
    new = []
    for distance, place in within_range:
        addr = place.get('address')
        if addr not in PLACES_ALREADY_SENT:
            new.append((distance, place))
            PLACES_ALREADY_SENT.add(addr)

    return new


def places_within_range(sorted_distance):
    within_range = []
    for distance, place in sorted_distance:
        if distance <= WITHIN_RANGE:
            within_range.append((distance, place))
    return within_range

def pretty_print(distance, place):
    price = "??.?" if place.get('priceInCents') is None else str(place.get('priceInCents')/100)

    msg = str(round(distance)) + "km: " \
            + place.get('status') \
            + " $" + price \
            + " for " + str(place.get('pricePerN')) \
            + " : " + place.get('address')
    print(msg)
    return msg

def get_json():
    response = requests.get('https://sparkling-voice-bdd0.pipelabs-au.workers.dev/')
    return response.json()

def get_sorted_distances(places):
    distances = []
    for place in places:
        if place.get('status') != "NO_STOCK":
            distances.append((get_distance(place), place))

    return sorted(distances, key=lambda x: x[0])

def get_distance(place):
    coords = (place.get('lat'), place.get('lng'))
    return geopy.distance.distance(HOME_COORDS, coords).km

if __name__ == "__main__":
    while True:
        main()
        time.sleep(5)
