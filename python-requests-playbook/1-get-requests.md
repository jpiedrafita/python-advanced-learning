# Analyzing GET Requests and the Response Object
## 1.1 Initiating GET Requests

- HTTP defines several request methods (verbs); **GET** is the most common.

- Browsers use **GET** to retrieve and display resources like HTML pages.

- **GET requests** are used to **retrieve data** from a specific URL, especially in APIs (often returning JSON).

- Example use case: requesting weather data using a location.

- **GET requests are idempotent** – sending the same request multiple times yields the same result.

- GET is not suited for sending large payloads.

- They are typically **cached** and **bookmarkable**.

- To use the **requests** library in Python:

```python
import requests
response = requests.get("http://localhost:8000/api/items")
print(response)
```

```bash
❯ python script.py
<Response [200]>
```

## 1.2 Analyzing the Response's Status Code

- The **response object** has a `status_code` property to check the outcome of a request.

```python
print(response.status_code)  # 200 means OK
```

- Common status codes:
    - 200 – Success
    - 404 – Not Found   
    - 500 – Server Error

- Status codes help control program flow and handle different outcomes (errors, redirection, rate limits, etc.).

- You can use conditionals:

```python
if response.status_code == 200:
    # proceed
elif response.status_code == 404:
    # handle not found
```

- The `response.ok` property returns `True` for codes in the 200–299 range.

- The `.ok` shortcut is available but **less precise** than explicitly checking codes.

## 1.3 Handling HTTP Error Exceptions

```python
import requests

try:
    response = requests.get("http://localhost:8000/api/items")
    response.raise_for_status()
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(err)
else:
    print(response.status_code)
```

- Use `response.raise_for_status()` to automatically raise an exception for **client** (4xx) or **server** (5xx) errors.

- Raises a `requests.exceptions.HTTPError` if the response is an error.    

- Useful for:
	- **Simple error handling** when no custom logic is needed.
    - **Debugging**, as the exception includes detailed error info.
    - **Larger apps** where consistent error handling is important.

- Avoids manually checking status codes if you only care whether the request succeeded or not.

## 1.4 Inspecting the Response Object

```python
response = requests.get("http://localhost:8000/api/items")
print(response.content)
```

```bash
❯ python script.py
b'[{"name":"Foo","price":23.45},{"name":"Bar","price":67.89},{"name":"Baz","price":12.34},{"name":"Qux","price":56.78},{"name":"Quux","price":45.67},{"name":"Corge","price":78.9},{"name":"Grault","price":90.12},{"name":"Garply","price":34.56},{"name":"Waldo","price":89.01},{"name":"Fred","price":67.23},{"name":"Plugh","price":45.89},{"name":"Xyzzy","price":23.78},{"name":"Thud","price":90.23}]'
```

- **Response payload** contains the actual data, key for GET requests.    

- Use `.content` to get raw bytes (useful for binary files like images or PDFs).

- The `b` prefix in the output means the response is a **byte string**.
	- It is readable because `print` automatically tries to convert bytes into text.
    
- `.hex()` shows the byte content in hexadecimal format.

```python
print(response.content.hex())
```
```bash

❯ python script.py
5b7b226e616d65223a22466f6f222c227072696365223a32332e34357d2c7b226e616d65223a22426172222c227072696365223a36372e38397d2c7b226e616d65223a2242617a222c227072696365223a31322e33347d2c7b226e616d65223a22517578222c227072696365223a35362e37387d2c7b226e616d65223a2251757578222c227072696365223a34352e36377d2c7b226e616d65223a22436f726765222c227072696365223a37382e397d2c7b226e616d65223a22477261756c74222c227072696365223a39302e31327d2c7b226e616d65223a22476172706c79222c227072696365223a33342e35367d2c7b226e616d65223a2257616c646f222c227072696365223a38392e30317d2c7b226e616d65223a2246726564222c227072696365223a36372e32337d2c7b226e616d65223a22506c756768222c227072696365223a34352e38397d2c7b226e616d65223a2258797a7a79222c227072696365223a32332e37387d2c7b226e616d65223a2254687564222c227072696365223a39302e32337d5d
```

- Use `.text` to convert bytes to string (default encoding: UTF-8).

```python
print(response.text)
```

- The `Content-Type header helps determine how to decode the response.

```python
print(response.headers["Content-Type"])
```

```bash
❯ python script.py
application/json
```

- You can manually set the `response.encoding` before using `.text` for more control.
	- It is a good practice to set it before using the `.text` property if its already known.

```python
response.encoding = "utf-8"
print(response.headers["Content-Type"])
```

- If the content is JSON:
    - Use `.json()` to convert it directly into Python data structures (e.g., list of dicts).

	```python
print(response.json())
```

    - This allows for direct manipulation of the data in your program.

```python
print(response.json()[1]["name"])
```

```bash
❯ python script.py
Bar
```

## 1.5 Passing Values trough Query String Parameters

- **GET requests** allow adding **query string parameters** directly in the URL.

- Common use: **filtering, sorting, pagination**, or customizing response data.

- Query format:
    - Follows the ? symbol after the URL.
    - Key-value pairs use =.
    - Multiple parameters are joined using &.
    - Example: `?max_price=40&offset=2&limit=2`.

- **Drawback**: Query strings are visible in URLs → not safe for sensitive data (e.g., passwords).

- **Manual URL construction** can become messy, especially with special characters.

- **Best practice**: use the `params` argument in the `requests.get()` method with a Python dict.

```python
query_params = {"offset": 2, "limit": 2, "max_price": 40}
response = requests.get("http://localhost:8000/api/items", params=query_params)
```

## 1.6 Assigning Event Hooks

- The **Requests library supports a hook system**, useful for tasks like **custom logging** or **debugging**.

- A **hook** is a **callback function** triggered by a specific event in the request lifecycle.

- Currently, only the **response hook** is available.

- Example of a hook:

```python
# Note that the final / is not supported in the api:
# original url: http://localhost:8000/api/items
response = requests.get("http://localhost:8000/api/items/", hooks={"response": log_url})

response.encoding = "utf-8"
print(response.status_code)
```

```bash
❯ python script.py
Requested URL: http://localhost:8000/api/items/
Requested URL: http://localhost:8000/api/items
200
```

> [!WARNING] Note that the hook returned two requests because the server will figure out that we didn't mean to use `/` at the end of the URL and redirects to `http://localhost:8000/api/items`. This is not an issue with GET request, but it might be with PUT requests.

- The **hook function receives the response object** as its first argument.

- Hooks help inspect things like:
    - **Redirects**
    - **Actual final URL used**
    - **Headers, status, or content of the response**

- Example case:
    - A route with a trailing slash (/api/items/) causes a **redirect** to /api/items.
    - Hook prints both requests, making the redirection visible.
    - This can prevent issues, especially with **POST requests** where a redirect might change the method to **GET**.