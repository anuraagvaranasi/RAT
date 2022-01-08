import json

class Secrets:
    def __init__(self):
        account_sid, auth_token, text_service_id = self.__secrets_file__init__()
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.text_service_id = text_service_id

    def __secrets_file__init__(self):
        with open('secrets.json') as secrets_file:
            secrets = json.load(secrets_file)
            return (secrets['ACCOUNT_SID'], secrets['AUTH_TOKEN'], secrets['TEXT_SERVICE_ID'])
