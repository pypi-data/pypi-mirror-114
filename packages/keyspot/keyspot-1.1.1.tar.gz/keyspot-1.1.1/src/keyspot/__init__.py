import http.client
import json

__all__ = ['get_record', 'update_record']

url = 'database-driver-ifhogzjzbq-uc.a.run.app'

def get_record(access_key):
    connection = http.client.HTTPSConnection(url, 443)
    connection.request('GET', f'/{access_key}')
    return connection.getresponse().read().decode()

def update_record(access_key, new_record):
    connection = http.client.HTTPSConnection(url, 443)
    connection.request('PUT', f'/{access_key}', json.dumps(new_record), {'Content-Type': 'application/json'})
    connection.getresponse()