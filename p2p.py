""" P2P CONNECTION FOR NODE AND WALLET
    To simplify my code:  
        Nodes use port start from 8000
        Wallets use port start from 10000
    p2ptype: 
        + Node = 1
        + Wallet = 2
    Communication Protocol:
        - Node to node:
            + 2 -- Register to another node
            + 3 -- Give information (Give all the connected peers)
            + 4 -- Broadcast a block (nonce + id)
            + 5 -- Broadcast (normal message)
        - Wallet to node:
            + 8 -- Register to a node ()
            + 9 -- Subscribe to a node (Get reward, get information)
        - Node to Wallet, a node broadcast to all connected objects so same number:
            + 4 -- Broadcast a block (nonce + id, for collecting/updating balance)
            + 5 -- Broadcast (normal message)
"""
import socket
import threading

localhost = socket.gethostname()
class P2PNode():
    def __init__(self, port=8000, peers=[], peers_assigned=[], connections=dict()):
        self.host = socket.gethostname()
        self.port = port
        self.connections = connections
        self.peers = peers
        self.peers_assigned = peers_assigned
    # ============================================================================== #
    def set_port(self, p):
        self.port = p
    # ============================================================================== #
    def set_peers(self, p, conn, p_a):
        self.peers.append(p)
        self.connections[p] = conn
        self.peers_assigned.append(p_a)
    # ============================================================================== #
    def generate_next_listen_port(self):
        return self.port%8000*3 + len(self.peers) + 8001
    # ============================================================================== #
    def broadcast(self, msg):
        """ Send msg to all the peers of this node
        """
        for p in self.peers:
            if p != self.port:
                self.connections[p].send(msg)
    # ============================================================================== #
    def generate_connected_peers(self):
        msg = f'Current connected peers are :'
        for p in self.peers:
            msg += str(p) + ' '
        msg = bytes(msg, 'utf-8')
        return msg
    # ============================================================================== #
    
    def listening(self, p=None):
        """ Set up a socket for listening to other peers
            p: port
        """
        if p == None: p = self.port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, p))
        print(f'Initializing connection on port {p}')
        s.listen(3) # Each node listen to maximum 3 objects, including wallet
        while True:
            new_connection, peer_address = s.accept()
            if peer_address[1] != 10000 and peer_address[1] != 10001:
                assign_port = self.generate_next_listen_port()
                print(f'Peer {peer_address[1]} is connecting to me! Listen port {assign_port}')
                msg = f'A new peer {peer_address[1]} has connected to port {p}'
                msg = bytes(msg, 'utf-8')
                self.broadcast(msg) # Inform all connected peers
                msg = self.generate_connected_peers()
                new_connection.send(msg) # Send the list of connected peers to new peer
                msg = bytes(str(assign_port), 'utf-8')
                print(f'Assigning a new port {assign_port} to this node')
                new_connection.send(msg) # Send the assigned port to the peer (listening port)
                self.peers_assigned.append(assign_port)
                self.peers.append(peer_address[1])
                self.connections[peer_address[1]] = new_connection
            elif peer_address[1] >= 10000:
                msg = self.generate_connected_peers()
                new_connection.send(msg) # Send the list of connected peers to the wallet
                new_connection.shutdown(socket.SHUT_RDWR)
                new_connection.close()
            elif peer_address[1] == 10001:
                print('Attempt to connect with wallet!')
                msg = self.receiving_tmp(10002)
                print('Received wallet message!')
                if msg != None:
                    msg = bytes(msg, 'utf-8')
                    self.broadcast(msg)
    # ============================================================================== #
    def receiving(self, p=None):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((localhost, int(p)))
        assign_port = 0
        print(f'I am connecting to the port {self.port}. My address is {s.getsockname()[1]}.')
        while True:
            msg = s.recv(1024).decode('utf-8')
            if len(msg) > 0:
                if len(msg) == 4:   # Get the assigned port for listening
                    assign_port = int(msg)
                    print(f'My listening port is {assign_port}')
                    try:
                        self.set_peers(self.port, s, self.port)
                        self.set_port(assign_port)
                        t3 = threading.Thread(target=self.listening, args=[assign_port])
                        t3.start()
                    except:
                        print(f'Thread failed to start!!!')
                else:
                    print(msg)
    # ============================================================================== #
    def receiving_tmp(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((socket.gethostname(), port))
        s.settimeout(1)
        while True:
            msg = s.recv(1024).decode('utf-8')
            if len(msg) > 0:
                s.shutdown(socket.SHUT_RDWR)
                s.close()
                return msg
        return None