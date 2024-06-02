from abc import ABC, abstractmethod
import pickle
import socket
import time
from typing import Any, Dict, Optional, Tuple


INTERVAL_SECS = 1
BUFFER_SIZE = 1024
ADDRESS = ("localhost", 65535)


MESSAGE_KINDS = set(["HEADER", "OBJECT", "KILL", "ACK"])


class Message:
    """

    :param kind: message type name. see docstring for recognized types.
    :param content: any serializable data
    """

    kind: str
    content: Any

    def __init__(self, kind: str, content: Any = None) -> None:
        assert kind in MESSAGE_KINDS
        self.kind = kind
        self.content = content

    def __str__(self) -> str:
        return f"{self.kind}: '{self.content}'"

    def __repr__(self) -> str:
        return str(self)

    def dump(self) -> bytes:
        return pickle.dumps(self)

    @staticmethod
    def load(content: bytes) -> "Message":
        return pickle.loads(content)


class ICommunicator(ABC):
    @abstractmethod
    def send(self, message: Message):
        raise NotImplementedError

    @abstractmethod
    def receive(self):
        raise NotImplementedError


class ServerIPv4(ICommunicator):

    def __init__(self, address: Tuple[str, int], num_clients=5) -> None:
        self.address = address
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.address)
        self.socket.listen(num_clients)
        self.connection = None

    def __del__(self):
        print("server: preparing for garbage collection")
        if self.connection is not None:
            self.connection_terminate()
        self.socket.close()

    def connection_accept(self):
        self.connection = self.socket.accept()

    def connection_terminate(self):
        if self.connection:
            print(f"disconnecting client: {self.connection[1]}")
            connection = self.connection[0]
            connection.shutdown(socket.SHUT_RDWR)
            connection.close()
            self.connection = None

    def send(self, message: Message):
        connection, address = self.connection  # pyright: ignore
        print(f"server: sending to client ({address}) payload '{message}'")
        connection.sendall(message.dump())

    def receive(self):

        # log connection
        connection, address = self.connection  # pyright: ignore
        print(f"server: connection from {address}")

        # receive header
        message_header = connection.recv(BUFFER_SIZE)  # pyright: ignore
        message_header = Message.load(message_header)
        print(f"server: received '{message_header}'")
        assert message_header.kind == "HEADER"
        payload_size: int = message_header.content

        # acknowledge payload size
        print(f"server: sending ACK")
        self.send(Message("ACK", payload_size))

        # receive client data
        tstart = time.time()
        received_data = bytearray()
        while len(received_data) < payload_size:
            chunk = connection.recv(BUFFER_SIZE)
            if not chunk:
                break
            received_data.extend(chunk)
        elapsed = time.time() - tstart
        rbytes = len(received_data)
        print(f"server: recv {rbytes} b: {rbytes / elapsed / 1e3} KB/s")

        # acknowledge content transmission
        print(f"server: sending ACK")
        self.send(Message("ACK", payload_size))
        received_data = Message.load(received_data)
        print(f"server: received '{received_data}'")
        return received_data

    def receive_once(self):
        self.connection_accept()
        message = self.receive()
        self.send(Message(kind="KILL"))
        self.connection_terminate()
        return message


class ClientIPv4(ICommunicator):

    def __init__(self, address: Tuple[str, int]) -> None:

        self.address = address
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

    def __del__(self):
        self.connection_terminate()

    def connection_create(self):
        self.socket.connect(self.address)

    def connection_terminate(self):
        if not self.socket._closed:  # pyright: ignore
            print(f"disconnecting from server: {self.address}")
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
                self.socket.close()
            except Exception:
                pass

    def receive(self):
        raise NotImplementedError

    def send(self, message: Message):
        # prepare message for transmission and send header
        message_bytes = message.dump()
        header = Message(kind="HEADER", content=len(message_bytes))
        self.socket.sendall(header.dump())

        # receive acknowledgement - server is prepared for the actual message
        response = self.socket.recv(BUFFER_SIZE)
        response = Message.load(response)
        assert response.kind == "ACK" and response.content == len(message_bytes)

        # send actual message
        self.socket.sendall(message_bytes)

        # receive acknowledgement - server received message
        response = self.socket.recv(BUFFER_SIZE)
        response = Message.load(response)
        assert response.kind == "ACK" and response.content == len(message_bytes)

    def send_single(self, message: Message):
        self.connection_create()
        self.send(message)
        signal = pickle.loads(self.socket.recv(BUFFER_SIZE))
        assert signal.kind == "KILL"
        print("transmission complete - closing connection")
        self.connection_terminate()
