# HTTP Requests in `pyresponse`

> Pure OOP and Elegant Objects request inspection, transformation, and testing guide.

In `pyresponse`, incoming HTTP requests are pure domain objects implementing the `Request` protocol:

```python
class Request(Protocol):
    def head(self) -> Head: ...
    def method(self) -> str: ...
    def path(self) -> str: ...
    def query_string(self) -> bytes: ...
    def path_params(self) -> Mapping[str, str]: ...
    def body(self) -> AsyncIterable[bytes]: ...
```

Rather than calling monolithic methods on a fat request object, you compose focused **Inspectors** and **Decorators** around the request.

---

## Table of Contents

1. [Request Inspectors](#1-request-inspectors)
2. [Authentication Inspectors (`BearerToken`, `BasicAuth`)](#2-authentication-inspectors-bearertoken-basicauth)
3. [Payload Parsing (`Json`, `Urlencoded`, `Multipart`, `BodyBytes`)](#3-payload-parsing-json-urlencoded-multipart-bodybytes)
4. [Request Decorators & Envelopes (`With*`)](#4-request-decorators--envelopes-with)
5. [Testing with `Fake` (Zero Network Overhead)](#5-testing-with-fake-zero-network-overhead)

---

## 1. Request Inspectors

Focused domain objects encapsulate reading specific aspects of a request:

```python
from pyresponse.request import (
    Accept,
    ContentType,
    Cookies,
    Header,
    Host,
    Method,
    Path,
    PathParams,
    QueryParams,
    UserAgent,
)

async def handler(req):
    # Method and Path
    method_str = Method(req).value()  # e.g. "GET"
    path_str = Path(req).value()      # e.g. "/users/10"

    # Header lookup (fails fast with HeaderNotFound if missing and no default provided)
    trace_id = Header(req, "x-trace-id", default="none").value()

    # Query Parameters
    qp = QueryParams(req)
    page = qp.param("page", default="1")
    tags = qp.params("tag")  # returns list of values for ?tag=a&tag=b

    # Path Parameters (extracted from Regex or routing matches)
    user_id = PathParams(req).param("id")

    # Cookies
    session = Cookies(req).cookie("session_id", default="")

    # Specialized headers
    client_host = Host(req).value()
    user_agent = UserAgent(req).value()
    accept_mime = Accept(req).value()
    content_type = ContentType(req).value()
```

---

## 2. Authentication Inspectors (`BearerToken`, `BasicAuth`)

Extract credentials cleanly without manual string splitting:

### Bearer Token
Extracts the token from `Authorization: Bearer <token>`:
```python
from pyresponse.request import BearerToken, HeaderNotFound

async def protected_endpoint(req):
    try:
        token = BearerToken(req).value()
    except HeaderNotFound:
        # Fails fast if Authorization header is missing or not a Bearer token
        ...
```

### HTTP Basic Auth
Extracts decoded username and password from `Authorization: Basic <base64>`:
```python
from pyresponse.request import BasicAuth

async def admin_endpoint(req):
    auth = BasicAuth(req)
    username = auth.username()
    password = auth.password()
```

---

## 3. Payload Parsing (`Json`, `Urlencoded`, `Multipart`, `BodyBytes`)

Extracting request payloads is asynchronous and non-blocking:

### JSON Payload
Reads the body stream and deserializes it:
```python
from pyresponse.request import Json as RequestJson

async def create_item(req):
    data = await RequestJson(req).content()
    name = data["name"]
```

### URL-Encoded Form Data (`application/x-www-form-urlencoded`)
```python
from pyresponse.request import Urlencoded

async def submit_form(req):
    form = Urlencoded(req)
    email = await form.param("email")
    categories = await form.params("category")
```

### Streaming File Uploads (`multipart/form-data`)
Stream multipart form-data without loading entire large files into memory:
```python
from pyresponse.request import Multipart

async def upload_file(req):
    multipart = Multipart(req)
    async for part in multipart.parts():
        filename = part.filename()
        content_type = part.content_type()
        data = await part.content()
        # Process or stream part bytes...
```

### Raw Bytes
Read the entire raw body as bytes:
```python
from pyresponse.request import BodyBytes

async def raw_webhook(req):
    payload = await BodyBytes(req).content()
```

---

## 4. Request Decorators & Envelopes (`With*`)

Wrap requests with modified attributes without modifying original request instances. Ideal for middleware and testing:

```python
from pyresponse.request import (
    Fake,
    WithAccept,
    WithBearerToken,
    WithCookie,
    WithHeader,
    WithJsonBody,
    WithoutHeader,
    WithoutQueryParam,
    WithQueryParam,
    WithUserAgent,
)

req = Fake(path="/api/items")

# Add headers, tokens, and query params immutably
req = WithBearerToken(req, "my-jwt-token")
req = WithHeader(req, "X-Client", "MobileApp")
req = WithQueryParam(req, "sort", "asc")
req = WithCookie(req, "theme", "dark")
req = WithJsonBody(req, {"action": "refresh"})

# Remove attributes
req = WithoutHeader(req, "X-Client")
req = WithoutQueryParam(req, "sort")
```

---

## 5. Testing with `Fake` (Zero Network Overhead)

The `Fake` request object lets you test endpoints directly as pure Python functions or objects:

```python
import pytest
from pyresponse.request import Fake
from pyresponse.response import Ok
from my_app.endpoints import UserEndpoint

@pytest.mark.asyncio
async def test_user_endpoint():
    # Construct an in-memory request with method, path, headers, and json body
    req = Fake(
        method="POST",
        path="/users",
        headers=(("authorization", "Bearer token-123"),),
        body=b'{"username": "carol"}',
    )

    # Directly execute the endpoint
    endpoint = UserEndpoint()
    res = await endpoint.response(req)

    # Assert response
    assert res.head().status() == 201
```
