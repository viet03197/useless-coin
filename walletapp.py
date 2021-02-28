from wallet import Wallet
import socket
import threading
import pickle

localhost = socket.gethostname()

class WalletApp():
    def __init__(self, nport, port, balance=0, miner=None):
        self.host = localhost
        self.nport = nport
        self.port = port
        self.wallet = Wallet(balance)
        self.known_wallet = dict()
    
    def add_connected_wallet(self, tup):
        self.known_wallet[tup[0]] = (tup[1], tup[2])
    
    # ====================== Communication functions ============================== #
    def get_transaction(self):
        """ Waiting for new transaction from from keyboard
        """
        st = input('Enter your new transaction here <pubkey> <amount>:')
        params = st.split(' ')
        port = params[0]
        amount = params[1]
        return port, amount  

    def prepare_message(self, mtarget, mtype, data):
        return bytes(mtarget + ' ', 'utf-8') + bytes(mtype + ' ', 'utf-8') + pickle.dumps(data)

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
            new_connection, _ = s.accept()
            if self.miner is None:
                msg = bytes('8', 'utf-8') + self.serialize_wallet()
                new_connection.send(msg)
    
    def receiving(self, p):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((localhost, p))
        print(f'I am connecting to miner {p}. My address is {s.getsockname()[1]}')
        while True:
            msg = s.recv(4096).decode('utf-8')
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
        comps = msg.split(' ')
        mtarget, mtype = comps[0], comps[1]
        if mtarget != 'all' and mtype != 'wallet':
            return False        # Do nothing because message not concerned me
        if mtype == 'balance':
            self.wallet.balance = int(comps[2])
        






