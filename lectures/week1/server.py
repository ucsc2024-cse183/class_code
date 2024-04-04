import os
import sys
import socket
import datetime

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(("127.0.0.1", int(sys.argv[1])))
sock.listen(10)

types = {
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "gif": "image/gif",
}

header_template = (
"HTTP/1.1 {status}\r\n" +
"Date: Mon, 1 April 2024 12:28:53 GMT\r\n" +
"Server: MyFavoriteSmallServer\r\n" +
"Last-Modified: Mon, 1 April 2024 12:28:53 GMT\r\n" +
"Content-Length: {length}\r\n" +
"Content-Type: {type}\r\n" +
"Connection: Closed\r\n" +
"\r\n")

while True:
    conn, add = sock.accept()
    print(f"connection from {add}")
    data = conn.recv(1024)
    request = data.decode()
    lines = request.split("\n")
    parts = lines[0].split()
    if parts[0] != "GET":
        conn.close()
        continue
    requested_file = parts[1]      
    if not requested_file.startswith("/static/"):
        now = datetime.datetime.now()
        body = f"Hello World now is {now}"
        body = body.encode()
        status="200 OK"
        mime_type = "text/html"
    else:
        filename = requested_file[1:] # static/index.txt
        if os.path.exists(filename):
            extension = filename.split(".")[-1]
            mime_type = types.get(extension, "text/html")
            with open(filename, "br") as stream:
                status="200 OK"
                body = stream.read()
        else:
            body = b""
            status="404 NOT FOUND"
            mime_type = "text/html"

    header = header_template.format(status=status, length=str(len(body)), type=mime_type).encode()
    print(header)
    conn.send(header + body)
    conn.close()