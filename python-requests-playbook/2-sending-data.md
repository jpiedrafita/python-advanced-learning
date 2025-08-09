# Sending Data to the Server

## 2.1 Submitting Data with POST requests

- The **POST** method was introduced after **GET** to allow sending data to the server.

- The **same route** can respond differently depending on the HTTP method used (GET vs POST).

- **POST** sends data in the **request body**, not in the URL.

- It’s commonly used to:
    - Submit **web forms**
    - Send **JSON** or **binary files** (e.g. images, PDFs)
    - Perform **login/authentication**

- You can specify the **Content-Type** to inform the server about the data format.

- **More secure** than GET, since sensitive data (like passwords) is not exposed in the URL.    

- **Not idempotent**: repeating a POST request may have different results (e.g. create multiple records).

- POST requests **cannot be cached or bookmarked**.

## 2.2 Working with Form Data

- **Form data** is the most common type sent via **POST** requests, especially from HTML forms.

- Forms typically use:
    - method="post" → data goes in the **request body**
    - action="/items/new" → defines the URL where the data is sent

- Test the web form in the api test server: http://127.0.0.1:8000/items/new

```html
<!DOCTYPE html>
...
    <form action="/items/new" method="post">
      <label for="name">Item Name:</label>
      <input type="text" id="name" name="name" required>
      <br><br>
      <label for="price">Price:</label>
      <input type="number" id="price" name="price" step="0.01" required>
      <br><br>
      <input type="submit" value="Submit">
    </form>
...
```
    
- POST handlers are usually different from GET, even for the same route.

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/items/new' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'name=echo2&price=101'
```

- **Form data format** (`application/x-www-form-urlencoded`):
    - Structured as key-value pairs (e.g., name=Item&price=10)
    - Similar to query params, but sent in body, not URL.

- In **Requests** library:
    - Use `.post(url, data=your_dict)`
    - It automatically sets the right headers and encoding.

```python
response = requests.post(
    "http://localhost:8000/items/new",
    data={"name": "Another Item", "price": 44},
)
```

- You can inspect the actual request using:
    `response.request.headers` and `response.request.body`.

- Use `allow_redirects=False` to avoid hiding the original POST behind a redirected GET.

```python
response = requests.post(
    "http://localhost:8000/items/new",
    data={"name": "echo3", "price": 44},
    allow_redirects=False,
)

print(response.request.headers["content-type"])
print(response.request.body)
```

```bash
❯ python script.py
application/x-www-form-urlencoded
name=echo3&price=44
```

- Useful when interacting with **non-API** endpoints expecting **form submissions**, e.g., traditional websites.

## 2.3 Working with JSON Data

- Most modern APIs expect data in **JSON format**. 

- Using `data=...` in requests sends data as **form-encoded** (`application/x-www-form-urlencoded`).

- To send raw JSON, you could manually:
    - Use `json.dumps()` on your dictionary.
	- Set the `Content-Type: application/json` header yourself.

    ```python
import requests
import json

message_body = {"name": "Some item", "price": 22}
response = requests.post(
    "http://localhost:8000/items/new",
    data=json.dumps(message_body),
    headers={"Content-Type": "application/json"},
)
    ```
    
- However, requests provides a simpler way: use the **json=...** argument.

```python
import requests

message_body = {"name": "Some item", "price": 22}

response = requests.post(
    "http://localhost:8000/items/new",
    json=message_body,
)
```

- This automatically:
    - Serializes the data to JSON.
    - Sets the correct `Content-Type` header.

- You can inspect what’s being sent with:
    - `response.request.headers`
    - `response.request.body`

```python
print(response.request.headers["content-type"])
print(response.request.body)
```

```bash
❯ python script.py
application/json
b'{"name": "Some item", "price": 22}'
```

## 2.4 Working with XML and Other Types of Data

```python
import requests

message_body = """
<item>
    <name>Sample Item</name>
    <price>300</price>
</item>
"""

response = requests.post(
    "http://localhost:8000/api/items/xml",
    data=message_body,
    headers={"Content-Type": "application/xml"}
)
print(response.text)
```


```bash
❯ python script.py

        <response>
            <name>Sample Item</name>
            <price>300</price>
        </response>
```

- requests supports sending **raw data** via the data parameter, not just form data or JSON.

- To send **XML**:
    - Provide the XML string directly to `data=....`
    - Manually set the Content-Type header to application/xml.

- The response can also be in XML format.

- To **parse XML responses**, use Python’s built-in `xml.etree.ElementTree`:
    - Load the XML from `response.text` or `response.content`.
    - Use `.find(tag)` and `.text` to extract values.

        ```python
print(ET.fromstring(response.text).find("name").text)
print(ET.fromstring(response.text).find("price").text)
        ```

```bash
❯ python script.py
Sample Item
300
```

- This approach works with **any custom format**, not just XML.
- requests handles transport; it’s up to you to handle the parsing.

## 2.5 Uploading Files with POST Requests

```python
import requests

file1=open("file1.csv", "rb")
file2=open("file2.csv", "rb")
files = [
    ("files", ("file1.csv", file1, "text/csv")),
    ("files", ("file2.csv", file2, "text/csv"))
]

response = requests.post(
    "http://localhost:8000/upload-files",
    files=files
)

file1.close()
file2.close()

print(response.json())
```

```bash
❯ python script.py
{'uploaded_files': ['file1.csv', 'file2.csv']}
```

- The POST message body can include **binary data**, such as file uploads.

- To upload files with requests, use the **files=...** argument.

- Always open files in **binary mode** ('rb') when uploading.

- You can upload **multiple files** by passing a **list of tuples** to files.
    - Each tuple: `("fieldname", ("filename", file_object, "mime/type"))`
    - `fieldname`: corresponds to the HTML name attribute.
    - You can repeat the same field name (multi-upload) or use different ones.

- To upload a **single file**, use a dictionary.

```python
files = {"file": open("file1.csv", "rb")}
```

- Always close files after uploading, or better, use a **with context manager**.
- If successful, the server usually responds with confirmation (e.g. file names).

## 2.6 Using Other HTTP Methods

- HTML forms **only support GET and POST**, but HTTP/1.1 introduced **PUT, PATCH, DELETE**, etc.

- These methods can be used **freely in APIs**, without the HTML form limitations.

- APIs often reuse the **same endpoint path** and differentiate by **HTTP method**.

 **Method Purposes:**

- GET: retrieve a specific item (e.g., /items/1)
- PUT: **update entire resource** (e.g., name and price)
- PATCH: **update partial resource** (e.g., just the name)
- DELETE: remove a specific resource

**Notes:**

- PUT and PATCH both send data in the **request body** as JSON.
- The **resource ID** is included in the path (`/items/{id}`).
- `requests.put()`, `requests.patch()`, and `requests.delete()` are used for each method.
- The server selects the correct handler based on **method + path**.

```bash
# http://127.0.0.1:8000/api/items/1
{"name":"Bar","price":67.89}
```

```python
import requests


response = requests.put(
    "http://localhost:8000/api/items/1",
    json={
        "name": "Updated PUT Name",
        "price": 19.99,
    },
)

print(response.json())

```

```bash
# http://127.0.0.1:8000/api/items/1
{"name":"Updated PUT Name","price":19.99}
```

```python
import requests


response = requests.patch(
    "http://localhost:8000/api/items/1",
    json={"name": "Updated PATH Name"}
)

print(response.json())

```

```bash
# http://127.0.0.1:8000/api/items/1
{"name":"Updated PATCH Name","price":19.99}
```

```python
import requests

response = requests.delete("http://localhost:8000/api/items/0")

print(response.json())
```

```bash
❯ python script.py
{'status': 'Item deleted', 'item': {'name': 'Foo', 'price': 23.45}}
```
