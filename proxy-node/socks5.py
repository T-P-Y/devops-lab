import os, socket, select, threading

USER = os.getenv("PROXY_USER", "proxyuser").encode()
PASS = os.getenv("PROXY_PASSWORD", "proxypass123").encode()

def pipe(src, dst):
    try:
        while True:
            r, _, _ = select.select([src, dst], [], [], 30)
            if not r: break
            for s in r:
                data = s.recv(4096)
                if not data: return
                (dst if s is src else src).sendall(data)
    except Exception:
        pass
    finally:
        src.close(); dst.close()

def handle(client):
    try:
        ver, nmethods = client.recv(2)
        methods = client.recv(nmethods)
        if 2 not in methods:
            client.sendall(b"\x05\xff"); return client.close()
        client.sendall(b"\x05\x02")
        _, ulen = client.recv(2)
        uname = client.recv(ulen)
        plen = client.recv(1)[0]
        passwd = client.recv(plen)
        if uname != USER or passwd != PASS:
            client.sendall(b"\x01\x01"); return client.close()
        client.sendall(b"\x01\x00")
        _, cmd, _, atyp = client.recv(4)
        if atyp == 1:
            addr = socket.inet_ntoa(client.recv(4))
        elif atyp == 3:
            dlen = client.recv(1)[0]
            addr = client.recv(dlen).decode()
        else:
            return client.close()
        port = int.from_bytes(client.recv(2), "big")
        remote = socket.create_connection((addr, port), timeout=10)
        client.sendall(b"\x05\x00\x00\x01\x00\x00\x00\x00\x00\x00")
        pipe(client, remote)
    except Exception:
        client.close()

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("0.0.0.0", 1080))
srv.listen(64)
print("SOCKS5 proxy listening on 1080...")
while True:
    c, _ = srv.accept()
    threading.Thread(target=handle, args=(c,), daemon=True).start()
