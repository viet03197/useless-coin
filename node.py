"""
"""
import socket
import pickle
from threading import Thread
from wallet import Wallet
from transaction import Transaction
from ucoin import UCoin
from trans_pool import TransactionPool

localhost = socket.gethostname()
def print_break():
    print(f'=====================================================================')
    return
class Node():
    def __init__(self, port=8000):  # If first node then chaindata
        self.host = localhost
        self.port = port
        # Connected peers/nodes
        self.peers = []
        self.peers_assigned = []
        self.connections = dict()
        # Wallet information
        self.wallet = None
        self.known_wallet = dict()      # Always start with own wallet
        self.pool = TransactionPool()
        if self.port == 8000:
            self.chain = UCoin('The first block is here')
        else:
            self.chain = None
    
    def set_port(self, port):
        self.port = port
    def set_wallet(self, wallet):
        self.wallet = wallet
    def set_peer(self, port, conn, port_assigned):
        self.peers.append(port)                     # Receiving port of peers
        self.connections[port] = conn               # Save the connection of peers for later use
        self.peers_assigned.append(port_assigned)   # Listening port of peers
    def get_next_listening_port(self):
        return self.port%8000*3 + len(self.peers) + 8001
    
    # ====================== Input from keyboard functions ====================== #
    # ======================== Port managing functions ========================== #
    def prepare_message(self, mtarget, mtype, data):
        return bytes(mtarget + ' ', 'utf-8') + bytes(mtype + ' ', 'utf-8') + pickle.dumps(data,0)
    
    def prepare_triples(self): # Triple here = (receiving port, listening port, wallet port)
        triples = []
        for i in range(len(self.peers)):
            if self.peers[i] not in self.known_wallet:
                triples.append((self.peers[i], self.peers_assigned[i], None))
            else:
                triples.append((self.peers[i], self.peers_assigned[i], self.known_wallet[self.peers[i]]))
        return triples   
    # ========================= Communication functions ========================= #
    def broadcast(self, msg):
        """ Send msg to all the peers of this node, not including wallet
        """
        for p in self.peers:
            if p != self.port:
                self.connections[p].send(msg)

    def listening(self, port=None):     # Waiting for other nodes to connect to me
        if port is None: port = self.port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, port))
        print(f'Initializing connection on port {port}')
        print_break()
        s.listen(3) # Each node listen to maximum 3 objects, including wallet
        while True:
            new_connection, peer_address = s.accept()  # Someone wants to connect to me
            peer_port = peer_address[1]
            if peer_port != self.port+2000:     # Not a wallet
                assign_port = self.get_next_listening_port()
                print(f'Peer {peer_port} is connecting to me! Assigning its listen port {assign_port}')
              # Prepare broadcast message
                msg = self.prepare_message('node', 'newnode', assign_port)
                self.broadcast(msg)
              # Send already connected nodes to new node
                msg = self.prepare_message('node', 'connected', self.prepare_triples())
                new_connection.send(msg)
              # Send assigned port
                msg = self.prepare_message('node', 'assign', assign_port)
                new_connection.send(msg)
              # Add this new node to my list
                self.set_peer(peer_port, new_connection, assign_port)
            #elif peer_port == self.port+2000:   # Connect to a wallet
    
    def receiving(self, port=None):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((localhost, int(port)))
        print(f'I am connecting to node at port {self.port}. My address is {s.getsockname()[1]}.')
        while True:
            msg = s.recv(4096)
            if len(msg) > 0:
                command = self.process_msg(msg)
                if isinstance(command, list):
                    if command[0] == 'assign':
                        self.set_peer(self.port, s, command[1])
                        self.set_port(command[1])
                        t = Thread(target=self.listening, args=[self.port])
                        t.start()

    # ======================== Process message functions ======================== #        
    def process_msg(self, msg): # not yet decoded message
        comps = msg.split(b' ')
        mtarget, mtype = comps[0].decode('utf-8'), comps[1].decode('utf-8')
        assign_port = None
        if mtarget == 'wallet':
            return None
        if mtype == 'assign':      # the node I connect to send me new port
            assign_port = pickle.loads(comps[2])
            print(f'I receive my assigned port {assign_port}. I am listening at this port.')
            print_break()
            return [mtype, assign_port]
        if mtype == 'connected':   # other nodes that connected to that node before me
            triples = pickle.loads(comps[2])
            if len(triples) == 0:
                print(f'I am the first connected peer.')
                return [mtype]
            print(f'The following peers are connected:')
            for tr in triples:
                self.peers.append(tr[0])
                self.peers_assigned.append(tr[1])
                if tr[2] is None: print(f' - port {tr[1]} not associated to a wallet.')
                else:
                    print(f' - port {tr[1]} with wallet {tr[2]}')
                    self.known_wallet[tr[0]] = tr[2]
            print_break()
            return [mtype]

