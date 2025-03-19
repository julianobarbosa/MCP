import unittest
from src.client.trigger_client import ZabbixTriggerClient
from unittest.mock import patch

class TestZabbixTriggerClient(unittest.TestCase):

    @patch('src.protocol.api.ZabbixAPI')
    def test_initialization_and_authentication(self, MockZabbixAPI):
        mock_api = MockZabbixAPI.return_value
        mock_api.login.return_value = None

        client = ZabbixTriggerClient('http://example.com/api', 'user', 'password')
        
        MockZabbixAPI.assert_called_with('http://example.com/api')
        mock_api.login.assert_called_once_with('user', 'password')

if __name__ == '__main__':
    unittest.main()