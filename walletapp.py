from wallet import Wallet
import socket
from threading import Thread
import pickle
import time

localhost = socket.gethostname()
ithread = False
def print_break():
    print(f'=====================================================================')
    return
class WalletApp():
    ithread = False
    def __init__(self, port):
        self.host = localhost
        self.port = port
        self.wallet = Wallet(100)
        self.known_wallet = dict()
        self.transaction = None
    
    def add_connected_wallet(self, tup):
        self.known_wallet[tup[0]] = (tup[1], tup[2])
    
    # ====================== Communication functions ============================== #
    def get_transaction(self):
        """ Waiting for new transaction from from keyboard
        """
        global ithread
        st = input('Your command here, show balance / <pubkey> <amount>:')
        if st == 'show balance':
            print(self.wallet.balance)
            ithread = False
            return
        params = st.split(' ')
        port = int(params[0])
        amount = int(params[1])
        self.transaction = (port, amount)
        print(f'Received transaction order.')
        ithread = False
        return

    def prepare_message(self, mtarget, mtype, data):
        print(f'message len: {len(pickle.dumps(data, 0))}')
        return bytes(mtarget + ' ', 'utf-8') + bytes(mtype + ' ', 'utf-8') + pickle.dumps(data, 0)

    def serialize_wallet(self):
        return pickle.dumps(self.wallet)
    
    # ====================== Communication functions ============================== #
    def listening(self, p):
        """ Listen to block announcement and normal message from a node
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((localhost, p))
        print(f'Wallet at port {p}, listen to node at port {self.port}')
        s.listen(1)
        while True:
            new_connection, peer_address = s.accept()
            print(f'Send wallet info to my node at port {peer_address[1]}')
            x = (self.wallet.key.n, self.wallet.key.e, self.wallet.key.d, self.wallet.key.p, self.wallet.key.q) 
            msg = self.prepare_message('node', 'walletinfo', x)
            new_connection.send(msg)
            while True:
                global ithread
                if not ithread:
                    t = Thread(target=self.get_transaction)
                    t.start()
                    del t
                ithread = True                
                if self.transaction is not None:
                    msg = self.prepare_message('node', 'transaction', self.transaction)
                    new_connection.send(msg)
                    self.transaction = None
                
    def receiving(self, p):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((localhost, p+4000))      # Node port + 4000
        s.connect((localhost, p))
        print(f'I am connecting to miner {p}. My address is {s.getsockname()[1]}')
        while True:
            msg = s.recv(4096)
            if len(msg) > 0:
                self.process_msg(msg)
        return
    # ==================== Input from keyboard functions ========================== #
    def get_pubkey(self):
        return self.wallet.pubkey

    def get_known_wallet(self):
        print('Information of the known wallet: wallet port - corresponding node port')
        for k, v in self.known_wallet.values():
            print(v[0], v[1])
        return
    # ======================== Process message functions ========================== #
    def process_msg(self, msg): # decoded message
        comps = msg.split(b' ')
        mtarget, mtype = comps[0].decode('utf-8'), comps[1].decode('utf-8')
        if mtarget == 'node':
            return None        # Do nothing because message not concerned me
        if mtype == 'balance':
            print('\nUpdate balance')
            self.wallet.balance = pickle.loads(comps[2])
        






