import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import Timeout, RetryError
from urllib3.util import Retry

# retry conf
retry_strategy = Retry(
    total = 3,
    status_forcelist=[404, 429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "OPTIONS", "POST"]
)

# timeout = (ConnectTimeout, SocketTimeout)
timeout = (10.001, 10.0015)

adapter = HTTPAdapter(max_retries=retry_strategy)

# start session
http = requests.Session()
http.mount("https://", adapter=adapter)
http.mount("http://", adapter=adapter)

try:
    response = http.get(url="https://en.wikipedia.org/w/api.ph", timeout=timeout)
    print(response.text)
except RetryError as e:
    print("Retry Attempts Exhausted", e)
except Timeout as e:
    print("Request Timed Out", e)

# close session
http.close()