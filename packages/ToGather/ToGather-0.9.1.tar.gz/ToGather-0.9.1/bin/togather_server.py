import sys
from socketserver import *
import threading
import socket


# Overrides socketserver.BaseRequestHandler class.
# Class methods setup, handle, and finish are called automatically by superclass constructor.
class PythonHandler(BaseRequestHandler):
    _connections = {}  # Static dictionary to keep track of active connections
    _db_requester = socket.socket()

    data = ""

    def setup(self):
        print("setting up new connection")
        # self.request is the socket object being handled.
        PythonHandler._connections[len(PythonHandler._connections)] = self.request
        self.my_connection = len(PythonHandler._connections)  # Keeps track of current connection number

    def handle(self):

        print("Connected to client: %s:%d" % self.client_address)

        # TODO: Handle when connection is closed incorrectly by client.
        # TODO: Create method to handle header
        while PythonHandler.data != "exit()":
            length = int.from_bytes(self.request.recv(4), "big")  # Get length of message from first 4 bytes.

            msg_type = int.from_bytes(self.request.recv(1), "big")
            print("msg_type: ", msg_type)

            PythonHandler.data = self.request.recv(length)
            prefix = length.to_bytes(4, "big")  # Convert length to bytes.
            msg_type = msg_type.to_bytes(1, "big")
            # Create bytearray to append then convert back to bytes.
            PythonHandler.data = bytes(bytearray(prefix + msg_type + PythonHandler.data))

            # Added a check in header to prevent server from sending db to everyone.
            if int.from_bytes(msg_type, "big") == 0:  # Broadcast to everyone.
                PythonHandler.broadcast(PythonHandler.data, self.request)
            if int.from_bytes(msg_type, "big") == 1:  # Broadcast db to requester only.
                PythonHandler.send(PythonHandler.data, PythonHandler._db_requester)
                PythonHandler._db_requester = None
            # Send db
            if int.from_bytes(msg_type, "big") == 2:  # Send db from server to new client
                print("db req sent to host client")
                PythonHandler._db_requester = self.request
                target = PythonHandler._connections[0]
                PythonHandler.send(PythonHandler.data, target)


            if int.from_bytes(msg_type, "big") == 3:  # Exit command.  Close connection.
                PythonHandler.data = "exit()"
                break
            if int.from_bytes(msg_type, "big") == 4:  # Broadcast database update.
                PythonHandler.broadcast(PythonHandler.data, self.request)
            if int.from_bytes(msg_type, "big") == 5:  # Broadcast database deletion.
                PythonHandler.broadcast(PythonHandler.data, self.request)

        self.request.close()

    def finish(self):
        print("Connection to %s:%d closed" % self.client_address)
        try:
            del PythonHandler._connections[self.my_connection]
        except:
            pass
        self.request.close()

    # Sends a message to all connected clients except for sender.
    @staticmethod  # Static method has access to static variable connections[]
    def broadcast(message, source):
        source_exists = False
        for connection, request in PythonHandler._connections.items():
            if request.getpeername() == source.getpeername():
                source_exists = True

        if source_exists is True:
            # Iterate through connections and send data if remote address is not same as source's
            print("Broadcasting from: %s:%d" % source.getpeername())
            for connection, request in PythonHandler._connections.items():
                if request.getpeername() != source.getpeername():  # getpeername() returns remote address.
                    request.sendall(message)

        # Send signal to clients to update UI
        PythonHandler.update_ui()
        # Prevent server from sending message again
        PythonHandler.data = None

    """ Sends update header to all clients.  Receive class in client will 
        change boolean in Data class to signal that a UI update is needed. """
    @staticmethod
    def update_ui():
        # Create update header with message size of 0
        msg = bytes([0, 0, 0, 0, 6])

        # Send header to all connected clients.
        for connection, request in PythonHandler._connections.items():
            request.sendall(msg)

    # Sends a message to one client.
    @staticmethod  # Static method has access to static variable connections[]
    def send(message, destination):
        print("Sending to: %s:%d" % destination.getpeername())
        destination.sendall(message)


class TogatherTCPServer(ThreadingTCPServer):
    def __init__(self, host, port):
        self.allow_reuse_address = True
        super().__init__(host, port)


class StartServer(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.server = TogatherTCPServer(("localhost", 55557), PythonHandler)

    def run(self):
        # TODO: Run server in a thread to allow for exit command that calls _server.shutdown()
        # Creates an instance of PythonHandler class whenever connection is received from server.
        # ThreadingTCPServer uses threads to connect to each client.
        with self.server as _server:
            print("Python server started.")
            _server.serve_forever()
