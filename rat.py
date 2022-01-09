#!/usr/bin/python3
# Imports already in python/installed via pip
import requests
import geopy.distance
import time
# Imports of files in project
import users
from messages import Messages
from pretty import pretty_print

USER = users.init_users()[0]
MESSAGES = Messages()

def main(): 
    try:
        places = get_json()
        sorted_distance = get_sorted_distances(places, USER)
        
        for x in range(5):
            distance, place = sorted_distance[x]
            pretty_print(distance, place)
        print()

        within_range = places_within_range(sorted_distance, USER)
        MESSAGES.send_text(sorted_distance, USER, within_range)
        
    except Exception as err:
        print(err)
        print("Something went wrong. Swalloing issue, will retry in 5 seconds")

def places_within_range(sorted_distance, user):
    within_range = []
    for distance, place in sorted_distance:
        if distance <= user.range:
            within_range.append((distance, place))
    return within_range

def get_json():
    response = requests.get('https://sparkling-voice-bdd0.pipelabs-au.workers.dev/')
    return response.json()

def get_sorted_distances(places, user):
    distances = []
    user_coords = (user.lat, user.lng)

    for place in places:
        if place.get('status') != "NO_STOCK":
            distances.append((get_distance(place, user_coords), place))

    return sorted(distances, key=lambda x: x[0])

def get_distance(place, user_coords):
    coords = (place.get('lat'), place.get('lng'))
    return geopy.distance.distance((user_coords), coords).km

if __name__ == "__main__":
    while True:
        main()
        time.sleep(5)
