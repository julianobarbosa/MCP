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
