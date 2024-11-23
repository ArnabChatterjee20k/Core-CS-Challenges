> Note: The headers Content-Type and Content-Length are essential for describing the transferred data (in both the request and the response). Without Content-Type the browser won't know how to render the file and will default to plain text. Without the correct Content-Length the browser waits indefinitely for more data (if it's more than the actual length) or reads the data partially (if it's less than the actual length).

# HTTP Request and Response Rules

## HTTP Request Rules

An HTTP request consists of the following components:

### 1. Request Line
- **Structure**:
  ```plaintext
  <HTTP Method> <Request Target> <HTTP Version>\r\n
  ```
- **Rules**:
  - **HTTP Method**: Must be a valid HTTP method (e.g., `GET`, `POST`, `PUT`, `DELETE`).
  - **Request Target**: The path or URL the client wants to access (e.g., `/index.html` or `/api/data`).
  - **HTTP Version**: Typically `HTTP/1.1`.

#### Examples:
```plaintext
GET /index.html HTTP/1.1\r\n
POST /submit HTTP/1.1\r\n
```

### 2. Headers
- **Structure**:
  ```plaintext
  <Header-Name>: <Header-Value>\r\n
  ```
- **Rules**:
  - Headers are key-value pairs.
  - Header names are case-insensitive (e.g., `Host` and `host` are treated the same).
  - Each header is followed by a CRLF (`\r\n`).
  - The last header is followed by an empty line (`\r\n`) to signal the end of headers.

#### Common Headers:
- `Host`: Specifies the hostname and port.
- `User-Agent`: Identifies the client (browser, API client).
- `Content-Length`: Indicates the size of the body (for requests with a body).

#### Example:
```plaintext
Host: example.com\r\n
User-Agent: curl/7.68.0\r\n
Content-Length: 27\r\n
\r\n
```

### 3. Optional Body
- The request body contains data for the server, typically for `POST`, `PUT`, or `PATCH` requests.
- **Rules**:
  - The body is separated from the headers by an empty line (`\r\n`).
  - Its length is specified by the `Content-Length` header.

#### Example:
```plaintext
POST /submit HTTP/1.1\r\n
Host: example.com\r\n
Content-Length: 13\r\n
\r\n
name=JohnDoe
```

## HTTP Response Rules

An HTTP response consists of the following components:

### 1. Status Line
- **Structure**:
  ```plaintext
  <HTTP Version> <Status Code> <Reason Phrase>\r\n
  ```
- **Rules**:
  - **HTTP Version**: Typically `HTTP/1.1`.
  - **Status Code**: A three-digit code indicating the result of the request (e.g., `200`, `404`, `500`).
  - **Reason Phrase**: A short description of the status code (e.g., `OK`, `Not Found`).

#### Examples:
```plaintext
HTTP/1.1 200 OK\r\n
HTTP/1.1 404 Not Found\r\n
```

### 2. Headers
- **Structure**:
  ```plaintext
  <Header-Name>: <Header-Value>\r\n
  ```
- **Rules**:
  - Same format as request headers.
  - Common response headers include:
    - `Content-Type`: Specifies the MIME type of the body (e.g., `text/html`, `application/json`).
    - `Content-Length`: Indicates the size of the body.
    - `Connection`: Specifies whether the connection should remain open (`keep-alive`) or close.

#### Example:
```plaintext
Content-Type: text/html\r\n
Content-Length: 123\r\n
Connection: keep-alive\r\n
\r\n
```

### 3. Optional Body
- The response body contains the content returned by the server (e.g., HTML, JSON, etc.).
- **Rules**:
  - The body is separated from the headers by an empty line (`\r\n`).
  - The content format is specified by the `Content-Type` header.

#### Example:
```plaintext
HTTP/1.1 200 OK\r\n
Content-Type: text/plain\r\n
Content-Length: 13\r\n
\r\n
Hello, World!
```

## General Rules for Both Requests and Responses

1. **Line Endings**:
   - Each line must end with **CRLF (`\r\n`)**.
   - For compatibility, some servers may handle **LF-only (`\n`)** line endings.

2. **Whitespace**:
   - Allow multiple spaces between components in the request line.
   - Ignore trailing spaces.

3. **Header Parsing**:
   - Headers are case-insensitive.
   - Duplicate headers may be combined, depending on the header type (e.g., `Set-Cookie`).

4. **Empty Line**:
   - A blank line (`\r\n`) separates headers from the body.

5. **Length of Body**:
   - For requests: Determined by the `Content-Length` header or `Transfer-Encoding: chunked`.
   - For responses: Same rules apply.

## Example: Complete Request and Response

### Request
```plaintext
GET /hello.html HTTP/1.1\r\n
Host: example.com\r\n
User-Agent: curl/7.68.0\r\n
Accept: text/html\r\n
\r\n
```

### Response
```plaintext
HTTP/1.1 200 OK\r\n
Content-Type: text/html\r\n
Content-Length: 22\r\n
\r\n
<h1>Hello World!</h1>
```

| **Value**           | **Meaning**                                                | **Common Use Case**                                      |
|----------------------|------------------------------------------------------------|---------------------------------------------------------|
| `keep-alive`        | Keep the connection open for reuse.                         | HTTP/1.1 default, multiple requests over one connection. |
| `close`             | Close the connection after the current request/response.    | Ensure the connection is closed after the transaction.   |
| `Upgrade`           | Upgrade the connection to a different protocol (e.g., WebSockets). | Protocol switching for WebSocket or other protocols. |
| `proxy-connection`  | Indicates whether the connection to a proxy should be kept open. | Proxy-specific, similar to `keep-alive`.               |
| `TE`                | Specifies acceptable transfer encodings for the connection. | Used in HTTP/1.1 to declare acceptable transfer encodings. |
| `timeout`           | Connection may be closed after a timeout period.            | In cases where the connection might timeout due to inactivity. |
