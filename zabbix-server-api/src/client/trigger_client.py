import logging
from typing import Optional, List
from ..protocol.api import ZabbixAPI

logging.basicConfig(level=logging.ERROR)

class ZabbixTriggerClient:
    def __init__(self, api_url: str, username: str, password: str):
        self.api = ZabbixAPI(api_url)
        self.api.login(username, password)
        logging.error('[Setup] ZabbixTriggerClient initialized and authenticated.')

    def create_trigger(self, description: str, expression: str, priority: int = 0) -> dict:
        method = 'trigger.create'
        params = {
            "description": description,
            "expression": expression,
            "priority": priority
        }
        return self.manage_trigger(method, params)

    def get_triggers(self, triggerids: Optional[List[str]] = None, output: str = 'extend') -> dict:
        method = 'trigger.get'
        params = {
            "output": output
        }
        if triggerids:
            params["triggerids"] = triggerids
        return self.manage_trigger(method, params)

    def update_trigger(self, triggerid: str, status: Optional[int] = None, priority: Optional[int] = None) -> dict:
        method = 'trigger.update'
        params = {"triggerid": triggerid}
        if status is not None:
            params["status"] = status
        if priority is not None:
            params["priority"] = priority
        return self.manage_trigger(method, params)

    def delete_trigger(self, triggerids: List[str]) -> dict:
        method = 'trigger.delete'
        params = triggerids
        return self.manage_trigger(method, params)

    def manage_trigger(self, method: str, params: dict) -> dict:
        logging.error(f'[Setup] Initiating {method}...')
        try:
            response = self.api._make_request(method, params)
            logging.error(f'[API] Method: {method}, Params: {params}')
            logging.error(f'[API] Response: {response}')
            return response
        except Exception as error:
            logging.error(f'[Error] {method} failed: {str(error)}')
            raise