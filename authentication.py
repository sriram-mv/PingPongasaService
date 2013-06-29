import json
import cred_parser as Credentials
from endpoints import IDENTITY_URL
import requests

def auth():
    # Authenticaiton
    total_creds = Credentials.parse()
    creds={}
    creds['username'] = total_creds['user_name']
    creds['password'] = total_creds['password']
    auth_type = {'passwordCredentials': creds}
    wrapper = {'auth': auth_type}
    data = json.dumps(wrapper)
    r = requests.post(IDENTITY_URL, data=data,
                      headers={'content-type': 'application/json'})
    response = r.json()
    return response