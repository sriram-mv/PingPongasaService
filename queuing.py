import requests
import json
import sys

from endpoints import IDENTITY_URL,MARCONI_URL
from authentication import auth


# Create Queue
def create_queue(response,queue_name):
    XAuthToken = response['access']['token']['id']

    # Insert New Queue
    wrap = {'metadata' : 'Awesome Ping Pong Tournament'}
    dat = json.dumps(wrap)
    Final_URL = MARCONI_URL+'{0}'.format(queue_name)
    response = requests.put(Final_URL, data=dat,
                      headers={'content-type': 'application/json','X-Auth-Token':XAuthToken,'X-Project-Id':234},verify=False)

# Delete Queue
def delete_queue(response,queue_name):
    XAuthToken = response['access']['token']['id']
    Final_URL = MARCONI_URL+'{0}'.format(queue_name)
    response = requests.delete(Final_URL,headers={'content-type': 'application/json','X-Auth-Token':XAuthToken},verify=False)
    return response

# Insert Messages into the Queue

def insert_messages(response,data,queue_name):
    XAuthToken = response['access']['token']['id']
    URL = MARCONI_URL+'{0}/messages'.format(queue_name)
    _headers={'content-type': 'application/json','Client-ID':'PingPongBot','X-Auth-Token':XAuthToken,'X-Project-Id':234}
    response=requests.post(URL,data=data,headers=_headers,verify=False)

# Claim Messages
def claim_messages(response,data,queue_name):
    XAuthToken = response['access']['token']['id']
    URL = MARCONI_URL+'{0}/claims'.format(queue_name)
    _headers={'content-type': 'application/json','Client-ID':'PingPongBot','X-Auth-Token':XAuthToken,'X-Project-Id':234}
    response = requests.post(URL,data=data,headers=_headers,verify=False)
    # print q.headers,q.content,q.status_code
    if response.status_code != 204:
        data = response.json()
        message = json.loads(json.dumps(data[0]))
        firstsplit = message['href'].split('/')
        second_split = firstsplit[len(firstsplit)-1].split('?claim_id=')
        return (response, second_split[0], second_split[1],response.status_code)
    else:
        return (response,'0','0',response.status_code)

# Delete Message with claim
def delete_messages_with_claim(response, data, queue_name):
    XAuthToken = response['access']['token']['id']
    URL = MARCONI_URL+'{0}/messages/{1}'.format(queue_name,data)
    _headers={'content-type': 'application/json','Client-ID':'PingPongBot','X-Auth-Token':XAuthToken,'X-Project-Id':234}
    repsonse = requests.delete(URL,headers=_headers,verify=False)
    # print response.headers,repsonse.content,response.status_code

def delete_claim(response, data, queue_name):
    XAuthToken = response['access']['token']['id']
    URL = MARCONI_URL+'{0}/claims/{1}'.format(queue_name,data)
    _headers={'content-type': 'application/json','Client-ID':'PingPongBot','X-Auth-Token':XAuthToken,'X-Project-Id':234}
    response = requests.delete(URL,headers=_headers,verify=False)
    # print response.headers,response.content,response.status_code

def request_body(event,vs,time):
    body = {'event':event,
            'vs':vs,
            'time':time}
    message = {'body' : body,
               'ttl' : 100}
    return [message]

def construct_json(body):
    message = {"body" : body,
               "ttl" : 100}
    return [message]

def for_claim():
    data = {'ttl':100,'grace':100}
    return json.dumps(data)

    