#!/usr/bin/python3
# Imports already in python/installed via pip
import time
import requests
# Imports of files in project
import users
from messages import Messages
from pretty import pretty_print
from user_places import UserPlaces

USER = users.init_users()[0]
MESSAGES = Messages()

def main(): 
    try:
        places = get_json()
        user_places = UserPlaces(places, USER)
        
        for x in range(5):
            distance, place = user_places.sorted_places[x]
            pretty_print(distance, place)
        print()

        MESSAGES.send_text(USER, user_places.within_range)

    except Exception as err:
        print(err)
        print("Something went wrong. Swalloing issue, will retry in 5 seconds")

def get_json():
        response = requests.get('https://sparkling-voice-bdd0.pipelabs-au.workers.dev/')
        return response.json()

if __name__ == "__main__":
    while True:
        main()
        time.sleep(5)
