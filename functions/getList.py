import requests
from datetime import datetime
import time
import json


with open('config.json') as f:
   data = json.load(f)


def make_request():
    url = data["url"]+'/panel/inbound/list'
    cookie = ""
    if(cookie == ""):
        a = requests.post(data["url"]+'/login',json={
    
	        "username": data["username"],
	        "password": data["password"],
	        "LoginSecret": ""

        })

        cookie = a.headers['Set-Cookie'].split()[0]
    headers = {
        "Cookie": cookie
    }
    
    response = requests.post(url, headers=headers)
    return response

def calculate_percentage(up, down, total):
    marks_obtained = int(up) + int(down)
    if total > 0 and marks_obtained > 0:
        percentage = (marks_obtained / total) * 100
        return int(percentage)
    return 0

def get_expired_balance():
    response = make_request()
    expired = []

    if response.json().get('success', False):
        for item in response.json()['obj']:
            for client_stat in item['clientStats']:
                if client_stat['enable']:
                    percentage = calculate_percentage(client_stat['up'], client_stat['down'], int(client_stat['total']))
                    if 80 <= (percentage) < 100:
                        user = ''
                        for id in json.loads(item['settings'])['clients']:
                            if(id['email'] == client_stat['email'] and id['tgId'] != ''):
                                user = id['tgId']
                            
                        

                        
                            
                        if(user != ''):    
                            print(client_stat['email'])
                            usage = percentage
                            expired.append({'user': user, 'usage': usage,'email':client_stat['email']})

    else:
        print('You can\'t login with this information')
        return []

    return expired

def get_expired_days():
    response = make_request()
    expired = []

    if response.json().get('success', False):
        current_time = int(time.time())

        for item in response.json()['obj']:
            for client_stat in item['clientStats']:
                if client_stat['enable'] and client_stat['expiryTime'] > 0:
                    expiry_timestamp = client_stat['expiryTime'] / 1000 

                    days_difference = (datetime.fromtimestamp(expiry_timestamp) - datetime.fromtimestamp(current_time)).days

                    if days_difference <= 1:
                        user = ''
                        for id in json.loads(item['settings'])['clients']:
                            if(id['email'] == client_stat['email'] and id['tgId'] != ''):
                                user = id['tgId']
                       
                        if(user != ''):
                            print(client_stat['email'])
                            expired.append({'user': user, 'days': days_difference,'email':client_stat['email']})
    else:
        print('You can\'t login with this information')
        return []

    return expired



def all_days():
    response = make_request()
    expired = []

    if response.json().get('success', False):
        current_time = int(time.time())
        for item in response.json()['obj']:
            for client_stat in item['clientStats']:
                if client_stat['enable'] and client_stat['expiryTime'] > 0:
                    expiry_timestamp = client_stat['expiryTime'] / 1000 
                    days_difference = (datetime.fromtimestamp(expiry_timestamp) - datetime.fromtimestamp(current_time)).days
                    user = client_stat['email']
                    expired.append({'user': user, 'days': days_difference})
        
        return expired
    
def all_balance():
    response = make_request()
    expired = []

    if response.json().get('success', False):
        for item in response.json()['obj']:
            for client_stat in item['clientStats']:
                if client_stat['enable']:
                    percentage = calculate_percentage(client_stat['up'], client_stat['down'], int(client_stat['total']))
                    user = client_stat['email']
                    usage = percentage
                    expired.append({'user': user, 'usage': usage})
        return expired