from comms import *


if __name__ == "__main__":
    message = Message(kind="OBJECT", content="star")
    client = ClientIPv4(address=ADDRESS)
    client.send_single(message=message)


# Echo client program
# import socket
# import pickle
#
# HOST = "localhost"  # The remote host
# PORT = 65535  # The same port as used by the server
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     message = b"Hello, world"
#     s.connect((HOST, PORT))
#     s.sendall(pickle.dumps(len(message)))
#     print(s.recv(1024))
#     s.sendall(message)
#     print(s.recv(1024))
