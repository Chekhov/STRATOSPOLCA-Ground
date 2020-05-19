import socket


def read(sock, bufsize):
    data, address = sock.recvfrom(bufsize)
    text= ['received {} bytes from {}'.format(
        len(data), address)]
    text.append(data)
    return ';'.join(text)