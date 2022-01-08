import json

class User:
    def __init__(self, phone_number, lat, lng, range):
        self.phone_number = phone_number
        self.lat = lat
        self.lng = lng
        self.range = range

    def __users_file__init__(self):
        with open('secrets.json') as secrets_file:
            secrets = json.load(secrets_file)
            return (secrets['ACCOUNT_SID'], secrets['AUTH_TOKEN'], secrets['TEXT_SERVICE_ID'])

def init_users():
    with open('users.json') as users_file:
        users_json = json.load(users_file)
        users = users_json['users']
        user_list = []
        for user in users:
            user_list.append(User(user['phone_number'], user['lat'], user['lng'], user['range'])) 
        
        return user_list

