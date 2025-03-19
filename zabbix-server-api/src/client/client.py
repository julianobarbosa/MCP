from typing import List, Optional
from ..protocol.api import ZabbixAPI
from ..models.host import Host


class ZabbixClient:
    def __init__(self, url: str):
        self.api = ZabbixAPI(url)

    def login(self, username: str, password: str) -> None:
        self.api.login(username, password)

    def get_host(self, host_id: str) -> Host:
        result = self.api._make_request(
            "host.get",
            {
                "hostids": host_id,
                "output": "extend",
                "selectInterfaces": "extend",
                "selectGroups": "extend",
            },
        )

        if not result:
            raise ValueError(f"Host with ID {host_id} not found")

        return Host.from_api_response(result[0])

    def get_hosts(self, filter_dict: Optional[dict] = None) -> List[Host]:
        params = {
            "output": "extend",
            "selectInterfaces": "extend",
            "selectGroups": "extend",
        }

        if filter_dict:
            params["filter"] = filter_dict

        result = self.api._make_request("host.get", params)
        return [Host.from_api_response(host_data) for host_data in result]

    def create_item(self, name: str, key_: str, hostid: str, type_: int, value_type: int, interfaceid: Optional[str] = None, delay: str = '30s') -> dict:
        logging.error('[Setup] Creating Zabbix item...')
        params = {
            'name': name,
            'key_': key_,
            'hostid': hostid,
            'type': type_,
            'value_type': value_type,
            'delay': delay
        }
        if interfaceid:
            params['interfaceid'] = interfaceid
        try:
            result = self.api._make_request('item.create', params)
            logging.error(f'[API] create_item response: {result}')
            return result
        except Exception as error:
            logging.error(f'[Error] create_item failed: {str(error)}')
            raise

    def get_items(self, hostids: List[str], search: Optional[dict] = None) -> dict:
        logging.error('[Setup] Retrieving Zabbix items...')
        params = {'output': 'extend', 'hostids': hostids}
        if search:
            params['search'] = search
        try:
            result = self.api._make_request('item.get', params)
            logging.error(f'[API] get_items response: {result}')
            return result
        except Exception as error:
            logging.error(f'[Error] Failed to retrieve items: {str(error)}')
            raise

    def update_item(self, itemid: str, delay: Optional[str] = None, status: Optional[int] = None) -> dict:
        logging.error('[Setup] Updating Zabbix item...')
        params = {'itemid': itemid}
        if delay:
            params['delay'] = delay
        if status is not None:
            params['status'] = status
        try:
            result = self.api._make_request('item.update', params)
            logging.error(f'[API] update_item response: {result}')
            return result
        except Exception as error:
            logging.error(f'[Error] Failed update_item: {str(error)}')
            raise

    def delete_item(self, itemids: List[str]) -> dict:
        logging.error('[Setup] Deleting Zabbix items...')
        try:
            result = self.api._make_request('item.delete', itemids)
            logging.error(f'[API] delete_items response: {result}')
            return result
        except Exception as error:
            logging.error(f'[Error] delete_items failed: {str(error)}')
            raise

