import pytest
from unittest.mock import Mock, patch
from zabbix_sdk.client.client import ZabbixClient
from zabbix_sdk.models.host import Host


@pytest.fixture
def client():
    return ZabbixClient("http://example.com/zabbix")


def test_get_host(client):
    mock_response = [
        {
            "hostid": "10084",
            "host": "test.example.com",
            "name": "Test Host",
            "status": "0",
            "interfaces": [],
            "groups": [],
        }
    ]

    with patch.object(client.api, "_make_request", return_value=mock_response):
        host = client.get_host("10084")
        assert isinstance(host, Host)
        assert host.hostid == "10084"
