import requests
from typing import Dict, Any, Optional

class ZabbixAPI:
    def __init__(self, url: str):
        self.url = url.rstrip('/') + '/api_jsonrpc.php'
        self.auth_token = None
        self.id = 1

    def _make_request(self, method: str, params: Dict[str, Any]) -> Dict:
        headers = {
            'Content-Type': 'application/json-rpc'
        }
        
        data = {
            'jsonrpc': '2.0',
            'method': method,
            'params': params,
            'id': self.id,
        }

        if self.auth_token and method != 'user.login':
            data['auth'] = self.auth_token

        response = requests.post(self.url, json=data, headers=headers)
        response_data = response.json()

        if 'error' in response_data:
            raise ZabbixAPIError(response_data['error'])

        self.id += 1
        return response_data['result']

    def login(self, username: str, password: str) -> None:
        result = self._make_request('user.login', {
            'user': username,
            'password': password
        })
        self.auth_token = result

class ZabbixAPIError(Exception):
    pass