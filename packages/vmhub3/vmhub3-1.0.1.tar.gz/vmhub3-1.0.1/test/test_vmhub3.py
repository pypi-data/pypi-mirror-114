import pytest
from vmhub3 import VMHub3
from unittest.mock import MagicMock, patch


def test_vmhub3_init():
    ip = '1.1.1.1'
    password = 'abcde'
    hub = VMHub3(ip=ip, password=password)
    assert hub.ip == ip
    assert hub.password == password


@patch('vmhub3.vmhub3.requests.post')
@patch('vmhub3.vmhub3.requests.get')
def test_vmhub3_connect(mock_get, mock_post):
    resp1 = MagicMock()
    resp1.cookies.get_dict.return_value = {'sessionToken': '123'}
    mock_get.return_value = resp1
    content = MagicMock()
    content.decode.return_value = 'sid=123'
    resp2 = MagicMock()
    resp2.cookies.get_dict.return_value = content
    hub = VMHub3(ip='1.1.1.1', password='abcde')
    result = hub.connect()
    assert result is None


@patch('vmhub3.vmhub3.requests.post')
@patch('vmhub3.vmhub3.xmltodict.parse')
def test_vmhub3_get_config(mock_parse, mock_post):
    mock_parse.return_value = {'result': 'data'}
    hub = VMHub3(ip='1.1.1.1', password='abcde')
    hub.cookies = {'sessionToken': '123'}
    result = hub.get_config(0)
    mock_post.called_once()
    mock_parse.called_once()
    assert isinstance(result, dict)


@pytest.mark.parametrize('method_name', [
    'get_global_config',
    'get_language_config',
    'get_languages',
    'get_wifi_state',
    'get_wifi_config',
    'get_wifi_basic_config',
    'get_wifi_advanced_config',
    'get_status',
    'get_wps',
    'get_lan',
])
@patch('vmhub3.vmhub3.requests.post')
@patch('vmhub3.vmhub3.xmltodict.parse')
def test_vmhub3_get_methods(mock_parse, mock_post, method_name):
    mock_parse.return_value = {'result': 'data'}
    hub = VMHub3(ip='1.1.1.1', password='abcde')
    hub.cookies = {'sessionToken': '123'}
    method = getattr(hub, method_name)
    result = method()
    mock_post.called_once()
    mock_parse.called_once()
    assert isinstance(result, dict)
