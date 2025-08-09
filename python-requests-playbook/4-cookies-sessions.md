# Persisting Connections with Cookies and Sessions

## 4.1 Sending and Receiving Cookies

- **Purpose**: Cookies store stateful data for maintaining sessions (e.g., login persistence, shopping cart).

- **How they work**:
    - The server sets a cookie via the Set-Cookie header after login or a similar action.
    - The browser saves the cookie and sends it with every request to the same domain via the Cookie header.
    - Cookies can include attributes like Max-Age, Domain, etc.

```
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Set-Cookie: user-id=RWJjMTIz; Max-Age=3600; Path=/; Domain=127.0.0.1; Secure; HttpOnly
```
    
- **In Requests library**:
    - Send cookies → pass a dictionary to the cookies argument in the request.
    - Receive cookies → access `response.cookies` (a RequestsCookieJar object).
    - Convert to a dict via `get_dict()` for easy viewing.

```python
import requests

custom_cookies = {"user_id": "2"}

response = requests.get("http://localhost:8000/api/cookies", cookies=custom_cookies)

print(response.cookies.get_dict())
print(response.cookies["user_id"])

```

```bash
❯ python script.py
{'user_id': '2'}
2
```


## 4.2 Persisting Connections with Sessions

```python
import requests

# Invalid credentials
credentials = {"username": "name", "password": "pass"}

login_response = requests.post("http://localhost:8000/api/login", data=credentials)

login_cookies = login_response.cookies

print("Cookies returned from login:")
print(login_cookies.get_dict())
print("Login response:")
print(login_response.text)

response = requests.get("http://localhost:8000/protected", cookies=login_cookies)

print("Protected route:")
print(response.status_code)
print(response.text)
```

```bash
# If we provide invalid credentials, we will not have cookies in the response, and we cannot authenticate in the protected route (401)
❯ python script.py
Cookies returned from login:
{}
Login response:
{"message":"Invalid credentials"}
Protected route:
401
{"detail":"Unauthorized"}
```

```python
# Valid credentials
login_response = requests.post("http://localhost:8000/api/login", data=credentials)
```

```bash
# The successful login response contains the hashed user_id cookie
# With the cookie we get access to the protected route
❯ python script.py
Cookies returned from login:
{'user_id': 'd8d0c6b1dbf57835f1db853794871f1a'}
Login response:
{"message":"Login successful"}
Protected route:
200
{"message":"You have access to this protected route"}
```

- This approach can be hard to maintain if we get more requests to different protected routes.

- Sessions in the requests library simplify authentication workflows by automatically storing and sending cookies.

```python
import requests

credentials = {"username": "some_name", "password": "pass"}


with requests.Session() as session:
    credentials = {"username": "some_name", "password": "pass"}

    login_response = session.post("http://localhost:8000/api/login", data=credentials)

    print("Cookies returned from login:")
    print(session.cookies.get_dict())
    print("Login response:")
    print(login_response.text)

    response = session.get("http://localhost:8000/protected")

    print("Protected route:")
    print(response.status_code)
    print(response.text)
```

```bash
❯ python script.py
Cookies returned from login:
{'user_id': 'a96c32f2df4778e0ea37eb5ea883a252'}
Login response:
{"message":"Login successful"}
Protected route:
200
{"message":"You have access to this protected route"}
```

- A Session object keeps state across requests (cookies, headers, etc.) and reuses TCP connections for better performance.
    
- Using a **Context Manager** (with `requests.Session()` as session:) ensures that all underlying TCP connections are properly closed after use.
    
- Once logged in through a session, subsequent requests **automatically include authentication cookies without manual handling**.

- There is no need to store the response as well, as the cookies are completely abstracted from the code.

```python
# login_response = session.post("http://localhost:8000/api/login", data=credentials)
session.post("http://localhost:8000/api/login", data=credentials)
```

- This behavior mimics web browsers, where cookies are managed transparently to the user.

## 4.3 Retrying Failed Connections with Transport Adapters

- [**Transport Adapters**](https://requests.readthedocs.io/en/latest/user/advanced/#transport-adapters) allow customizing how requests handles HTTP connections, including retries, SSL versions, and other low-level settings.
	- It determines how the session interacts with the server.
    
- Always attached to a **Session** object; can be configured per domain or protocol (http://, https://).

```python
import logging
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RetryError


# Capture all messages from urllib3 library
logging.basicConfig(level=logging.DEBUG)
requests_log = logging.getLogger("urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


session = requests.Session()
# Mount the HTTPAdapter instance to the Session object
session.mount("http://localhost", HTTPAdapter(max_retries=3))

try:
    # This endpoint simulates an unreliable server, returning randomly successful or internal server error
    response = session.get("http://localhost:8000/flaky")

    print("Final response status:", response.status_code)
except RetryError:
    print("Maximum rettries exceeded. Server is not available.")
```


- We mount the `HTTPAdapter` instance to the `Session` object, which will override the default adapter configuration for this session. 
	- The first argument will specify the domain (localhost) in which this adapter should be used.
	- `max_retries`: Set the number of retries.
	- We can implement a more detailed strategy with `urllib3.Retry`.

```python
session = requests.Session()
retries = Retry(
    total=3, backoff_factor=0.1, status_forcelist=[500], allowed_methods={"GET"}
)
session.mount("http://localhost", HTTPAdapter(max_retries=retries))
```

```bash
❯ python script.py
DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): localhost:8000
DEBUG:urllib3.connectionpool:http://localhost:8000 "GET /flaky HTTP/1.1" 500 25
DEBUG:urllib3.util.retry:Incremented Retry for (url='/flaky'): Retry(total=2, connect=None, read=None, redirect=None, status=None)
DEBUG:urllib3.connectionpool:Retry: /flaky
DEBUG:urllib3.connectionpool:http://localhost:8000 "GET /flaky HTTP/1.1" 500 25
DEBUG:urllib3.util.retry:Incremented Retry for (url='/flaky'): Retry(total=1, connect=None, read=None, redirect=None, status=None)
DEBUG:urllib3.connectionpool:Retry: /flaky
DEBUG:urllib3.connectionpool:http://localhost:8000 "GET /flaky HTTP/1.1" 200 21
Final response status: 200
```

- **Retry strategy** is implemented via `urllib3.Retry` and passed to `HTTPAdapter(max_retries=retry_strategy)`.
	- `total`: max retries allowed.        
	- `backoff_factor`: exponential delay between retries (factor × 2^retry_number).
	- `status_forcelist`: HTTP status codes that should trigger retries (e.g., 500).
	- `allowed_methods`: safe methods to retry (e.g., GET, avoid retrying POST).
        
- Using retries avoids giving up too early on flaky endpoints and prevents rapid retry loops.
    
- Can mount different adapters for different domains within the same session.