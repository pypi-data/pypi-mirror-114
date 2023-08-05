# spartan-py

Basic spartan protocol implementation as a python library.

```python
import spartan

res = spartan.get("spartan://mozz.us/echo", "hi")
while True:
    buf = res.read()
    if not buf:
        break
    sys.stdout.buffer.write(buf)
res.close()
```

Try it in the REPL:
```python
>>> import spartan
>>> req = spartan.Request("spartan.mozz.us")
>>> req
<Request spartan.mozz.us:300 / 0>
>>> res = req.send()
>>> res
2 text/gemini
>>> res.read()
[...]
>>> res.close()
```

## install

```
pip3 install spartan-py
```

## API

- `Request(host: str, port: int = 300, path: str = "/", data: str = "")`
  - `.send() -> Response` - send the request
  - `__repr__()`
  - `__str__()`
- `Response(socket)`
  - `read()`
  - `close()` - close the socket
  - `.status` - status code
  - `.meta` - meta string for the status
  - `__repr__()`
  - `__str__()`
- `Status` - statuses
  - `success = 2`
  - `redirect = 3`
  - `client_error = 4`
  - `server_error = 5`
- `get(url: str, data: str = "") -> Response` - if the query string part in the URL exists, data will be ignored.

## TODO
- [ ] invalid url handling
- [ ] util functions like parsing meta and getting status type
- [ ] basic CLI usage
- [ ] async methods
