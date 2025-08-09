# Providing and Receiving Additional Data with Headers

## 3.1 Analyzing Response Headers

```python
import requests

response = requests.get("http://localhost:8000/api/items")
print(response.headers)
```

```bash
❯ python script.py
{'date': 'Fri, 08 Aug 2025 12:09:37 GMT', 'server': 'uvicorn', 'content-length': '545', 'content-type': 'application/json'}
```

- **Purpose of headers**: Provide metadata about the request/response, giving context for the payload (type, size, encoding, etc.).
    
- **Accessing headers**:
    - Use `.headers` to get a dictionary of all headers.
    - Access a specific header by key (case-insensitive).

- **Example**:
    - "Content-Type" tells the media type (e.g., application/json for JSON data).

```python
print(response.headers["Content-Type"])
```

```bash
❯ python script.py
application/json
```


## 3.2 Customizing Request Headers

```python
import requests

custom_headers = {"Authorization": "Bearer ACCESS_TOKEN", "Accept": "application/json"}

response = requests.get("http://localhost:8000/api/items", headers=custom_headers)

print(response.request.headers)
```

```bash
❯ python script.py
{'User-Agent': 'python-requests/2.29.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': 'application/json', 'Connection': 'keep-alive', 'Authorization': 'Bearer ACCESS_TOKEN'}
```

- **Purpose**: Request headers send extra information to the server, such as accepted content types, authentication data, or preferences.
    
- **Custom headers**:
    - Example:
        - "Accept" → specifies expected response format (e.g., application/json).
        - "Authorization" → carries credentials (e.g., bearer token for JWT).
            
- **Usage in Requests**:
    - Pass a dictionary to the headers argument in the request method.
    - Inspect via response.request.headers to confirm values.
        
- **Other header uses**: Control cache, cookies, encoding, language, analytics, preloaded links, etc.