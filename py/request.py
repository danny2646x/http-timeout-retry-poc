from sys import version
import requests
from requests.api import head
from urllib3.util import Retry
import platform
from urllib import parse

class HttpRequest:

    PY_VERSION = version
    USER_AGENT = 'ChargeBee-Python-Client'
    CONTENT_TYPE_JSON = 'application/json'
    API_SITE = ''
    API_KEY = ''
    API_VERSION = '2.9.0'
    PLATFORM = platform.platform()

    def __init__(
        self,
        connect_timeout_ms=15000,
        socket_timeout_ms=40000,
        retry_count=10,
        retry_methods=None,
        retry_statuses=None,
        backoff_factor=0
    ):
        self.connect_timeout_ms = connect_timeout_ms
        self.socket_timeout_ms = socket_timeout_ms
        self.retry_count = retry_count
        self.retry_methods = retry_methods
        self.retry_statuses = retry_statuses
        self.backoff_factor = backoff_factor

    def _get_retry_strategy(self):
        return Retry(
            total=self.retry_count,
            status_forcelist=self.retry_statuses,
            backoff_factor=self.backoff_factor
        )

    def _get_session(self):
        http_adapter = requests.adapters.HTTPAdapter(max_retries=self._get_retry_strategy())
        session = requests.Session()
        session.mount(self.API_SITE, http_adapter)
        return session

    def _build_headers(self, headers=None):
        return {
            'User-Agent': self.USER_AGENT,
            'Accept': self.CONTENT_TYPE_JSON,
            'Authorization': self.API_KEY,
            'Lang-Version': self.PY_VERSION,
            'OS-Version': self.PLATFORM
        } | headers


    def request(self, method, url, url_params, headers):
        session = self._get_session()
        headers = self._build_headers(headers)
        url_params = parse.urlencode(url_params)
        kwargs = {
            'timeout' : (self.connect_timeout_ms, self.socket_timeout_ms)
        }
        
        return session.request(
            method=method, 
            url=url, 
            params=url_params, 
            headers=headers,
            **kwargs
        )
