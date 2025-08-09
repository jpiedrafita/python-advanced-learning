# Working with Redirection and Timeouts

## 5.1 Working with Redirection and History

```python
import requests

response = requests.get("http://localhost:8000/old-route")

print(response.url)
print(response.status_code)
print(response.text)
```

```bash
❯ python script.py
http://localhost:8000/new-route
200
{"message":"This is the new route!"}
```

- **HTTP redirections** automatically guide the client to a new resource (e.g., moved routes, HTTPS upgrades).
    
- By default, GET requests in requests follow redirects automatically.

```python
response = requests.head("http://localhost:8000/old-route")
```

```bash
❯ python script.py
http://localhost:8000/old-route
307
```


- The HEAD method does not allow redirection by default.
	- We get a 307 Temporary Redirect code instead 200.

```python
response = requests.head("http://localhost:8000/old-route", allow_redirects=True)
```

```bash
❯ python script.py
http://localhost:8000/new-route
200
```

- `allow_redirects` argument controls redirect behavior:
    - GET → `allow_redirects=False` disables it.
    - HEAD → redirection disabled by default, can be enabled with `allow_redirects=True`.
    
- **Security consideration**: Disable redirection if you need strict control over request flow.

```python
response = requests.get("http://localhost:8000/old-route") 
print(response.history)
```

```bash
❯ python script.py
[<Response [307]>]
http://localhost:8000/new-route
200
{"message":"This is the new route!"}
```

- **Response history**:
    - `.history` contains a list of previous Response objects in the redirect chain (oldest → newest).
    - Useful for tracking multiple redirections.
        
- **Session-level control**:
    - `session.max_redirects` sets maximum allowed redirects (default = 30).
        
```python
session.requests.Session()
session.max_redirects = 3
response = session.get('http://127.0.0.1')
```

- **Debugging**: You can loop through `.history` to inspect `status_code` and `url` of each redirect step.

```python
response = requests.get('http://127.0.0.1')
for resp in response.history:
	print(resp.status_code, resp.url)
```

## 5.2  Setting Timeouts

```python
import requests

try:
    response = requests.get("http://localhost:8000/slow-response", timeout=(5, 3))
    print(response.json())
except requests.exceptions.ConnectTimeout:
    print("The request failed to connect in the allotted time.")
except requests.exceptions.ReadTimeout:
    print("The server did not send any data in the allotted time.")
```


- By default, requests waits indefinitely for a response — bad for production code.
    
- Always set a timeout to avoid hanging connections.
    
- `timeout` can be:
    - **Single number** → applies to both connection and read timeout.
    - **Tuple** (`connect_timeout`,` read_timeout`) → set separately.
		- **Connect timeout** → max time to establish connection.
		- **Read timeout** → max time to wait for data from server.
    
- If exceeded, a Timeout exception is raised.
    
- Can be set per request or at session level.
    