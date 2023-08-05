import socket
import sys
import urllib.parse


class Request:
    def __init__(
        self, host: str, port: int = 300, path: str = "/", data: str = ""
    ) -> "Request":
        self.host = host
        self.port = port
        self.path = path
        self.data = data

    def __repr__(self):
        return f"Request(host='{self.host}', port={self.port}, path='{self.path}') data-length={len(self.data)}"

    def __str__(self):
        return f"{self.host} {self.path} {len(self.data)}"

    def send(self):
        sock = socket.create_connection((self.host, self.port))
        host = f"{self.host}".encode("idna")
        path = self.path.encode("ascii")
        sock.send(b"%s %s %d\r\n" % (host, path, len(self.data)))
        sock.send(self.data.encode("ascii"))
        return Response(sock, self)


class Response:
    def __init__(self, socket: socket.socket, request: Request = None):
        self.socket = socket
        self.file = self.socket.makefile(mode="rb")
        self.request = request

        try:
            status, meta = self.file.readline(4096).split(maxsplit=1)
            self.status = int(status)
            self.meta = meta.strip().decode("ascii")
        except:
            self.close()
            raise InvalidHeader("Invalid header received")

    def __repr__(self):
        return f"{self.status} {self.meta}"

    def __str__(self):
        return repr(self)

    def read(self, size=4096):
        return self.file.read(size)

    def close(self):
        self.file.close()
        self.socket.close()


class InvalidHeader(Exception):
    """Invalid header"""  # Is it called header?


class Status:
    success = 2
    redirect = 3
    client_error = 4
    server_error = 5


def get(url: str, data: str = ""):
    """Fetches url and returns a response object"""
    u = urllib.parse.urlparse(url)
    if not u.hostname:
        u = urllib.parse.urlparse("spartan://"+url)
    if u.scheme != "spartan":
        raise RuntimeError("Unsupported scheme")
    if u.query:  # Ignores data argument if query is in url
        data = u.query
    req = Request(u.hostname, u.port or 300, u.path or "/", data)
    res = req.send()
    return res
