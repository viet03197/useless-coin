"""
"""
import socket
import pickle
from threading import Thread
from Crypto.PublicKey import RSA
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
        self.known_node = dict()    # To quickly find connection in the network
        self.peers = []
        self.peers_assigned = []
        self.connections = dict()
        # Wallet information
        self.wallet = None
        self.wallet_connection = None
        self.wallet_reproduce = dict()
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
    def mine(self):
        data = self.pool.valid_transactions()
        #data.append()
        self.chain.new_block(data)
        #print(b.hash, b.prev, b.id)
        print(self.chain.chain[-1].id, self.chain.chain[-1].hash)
        self.pool.clear()
        self.wallet.update_balance(self.chain)
        return
    # ====================== Input from keyboard functions ====================== #
    # ======================== Port managing functions ========================== #
    def prepare_message(self, mtarget, mtype, data):
        return bytes(mtarget + ' ', 'utf-8') + bytes(mtype + ' ', 'utf-8') + pickle.dumps(data,0)
    
    def prepare_triples(self): # Triple here = (receiving port, listening port, wallet port)
        triples = []
        for i in range(len(self.peers)):
            if self.peers_assigned[i] not in self.wallet_reproduce:
                triples.append((self.peers[i], self.peers_assigned[i], None))
            else:
                triples.append((self.peers[i], self.peers_assigned[i], self.wallet_reproduce[self.peers_assigned[i]]))
        return triples   
    # ========================= Communication functions ========================= #
    def broadcast(self, msg):
        """ Send msg to all the peers of this node, not including wallet
        """
        for p in self.peers:
            if p != self.port and p in self.connections:
                self.connections[p].send(msg)
            if p+1000 != self.port and p+1000 in self.connections:
                self.connections[p+1000].send(msg)
    
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
            if peer_port != self.port+4000:     # Not a wallet
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
                print(self.peers, self.peers_assigned, self.connections)
              # Send my wallet info
                if self.wallet is not None:
                    x = (self.wallet.key.n, self.wallet.key.e, self.wallet.key.d, self.wallet.key.p, self.wallet.key.q) 
                    msg = self.prepare_message('node', 'wallet', x)
                    print('Sending my wallet information to the new peer')
                    new_connection.send(msg)
                t = Thread(target=self.receiving, args=[assign_port+1000])
                t.start()
            elif peer_port == self.port+4000:   # Connect to a wallet
                self.wallet = Wallet(100)
                self.wallet_connection = new_connection
                print(f'Wallet {peer_port} is connecting to me.')
                msg = self.prepare_message('wallet', 'connected', self.prepare_triples())
                new_connection.send(msg)
                t = Thread(target=self.receiving, args=[peer_port-1000])
                t.start()
                if self.wallet is not None:
                    x = (self.wallet.key.n, self.wallet.key.e, self.wallet.key.d, self.wallet.key.p, self.wallet.key.q) 
                    msg = self.prepare_message('node', 'wallet', x)
                    print('Sending my wallet information')
                    self.broadcast(msg)

    def receiving(self, port=None):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tmp_port = self.get_next_listening_port()+1000
        s.bind((localhost, tmp_port))
        s.connect((localhost, int(port)))
        if port<10000:
            print(f'I am connecting to node at port {port}. My address is {s.getsockname()[1]}.')
        else:
            print(f'I am connecting to my wallet at port {port}.')
        fullpkg = []
        while True:
            msg = s.recv(4096)
            if not msg: break
            fullpkg.append(msg)
            if len(msg) > 0:
                command = self.process_msg(msg)
                if isinstance(command, list):
                    if command[0] == 'assign':
                        self.set_peer(self.port, s, command[1])
                        self.set_port(command[1])
                        if self.port not in self.known_node:
                            self.known_node[self.port] = set([port])
                        else: self.known_node[self.port].add(port)
                        #t = Thread(target=self.listening, args=[self.port])
                        #t.start()
                    if command[0] == 'newnode':
                        if self.port not in self.known_node:
                            self.known_node[self.port] = set([port])
                        else: self.known_node[self.port].add(port)
                    if command[0] == 'wallet':
                        print(f'A new wallet at port {port} connecting ')
                        self.wallet_reproduce[port] = command[1]
                        #print(self.wallet_reproduce[port])
                    if command[0] == 'transaction':
                        print(f'Transaction has been made.')
                        if len(self.pool.transaction) > 0:
                            self.mine()
                        print(f'New balance {self.wallet.balance}')
                        msg = self.prepare_message('wallet', 'balance', self.wallet.balance)
                        self.wallet_connection.send(msg)
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
                if self.port not in self.known_node:
                    self.known_node[self.port] = set([self.port])
                else: self.known_node[self.port].add(self.port)
                self.peers.append(tr[0])
                self.peers_assigned.append(tr[1])
                if tr[2] is None: print(f' - port {tr[1]} not associated to a wallet.')
                else:
                    print(f' - port {tr[1]} with wallet {tr[2]}')
                    self.wallet_reproduce[tr[1]] = tr[2]
            print_break()
            return [mtype]
        if mtype == 'newnode':      # Broadcast of a new node
            assign_port = pickle.loads(comps[2])
            print(f' - New node connected at port {assign_port}')
            print_break()
            return [mtype, assign_port]
        if mtype == 'walletinfo':
            w_key = pickle.loads(comps[2])
            self.wallet.key = RSA.construct(w_key)
            self.wallet.pubkey = self.wallet.key.public_key()
            print(f' - Set up my wallet info')
            return [mtype]
        if mtype == 'wallet':
            x = pickle.loads(comps[2])
            return [mtype, x]
        if mtype == 'transaction':
            port, amount = pickle.loads(comps[2])
            print(f'Setting up new transaction to port {port}, amount {amount}')
            print(self.wallet_reproduce)
            if port-4000 in self.wallet_reproduce:
                print(f'Creating new transaction to port {port}, amount {amount}')
                w_tmp = Wallet(0)
                w_tmp.key = RSA.construct(self.wallet_reproduce[port-4000])
                w_tmp.pubkey = w_tmp.key.public_key()
                self.wallet.create_transaction(w_tmp.pubkey, amount, self.pool)
                return [mtype]
            else:
                print(f'Invalid transaction, check receiver/ balance')
                return False