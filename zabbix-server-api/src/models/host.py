from dataclasses import dataclass
from typing import Optional, List, Dict

@dataclass
class Host:
    host: str
    name: Optional[str] = None
    status: Optional[int] = None
    interfaces: Optional[List[Dict]] = None
    groups: Optional[List[Dict]] = None
    hostid: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict) -> 'Host':
        return cls(
            hostid=data.get('hostid'),
            host=data.get('host'),
            name=data.get('name'),
            status=data.get('status'),
            interfaces=data.get('interfaces'),
            groups=data.get('groups')
        )