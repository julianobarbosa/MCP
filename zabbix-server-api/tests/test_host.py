import pytest
from zabbix_sdk.models.host import Host

def test_host_creation():
    host = Host(host="test.example.com")
    assert host.host == "test.example.com"
    assert host.hostid is None

def test_host_from_api_response():
    api_response = {
        'hostid': '10084',
        'host': 'test.example.com',
        'name': 'Test Host',
        'status': '0',
        'interfaces': [],
        'groups': []
    }
    
    host = Host.from_api_response(api_response)
    assert host.hostid == '10084'
    assert host.host == 'test.example.com'
    assert host.name == 'Test Host'