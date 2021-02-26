from wallet import Wallet
from p2p import P2PNode
import socket
import threading
import pickle

localhost = socket.gethostname()

class WalletApp():
    def __init__(self, port, balance=0, miner=None):
        self.host = localhost
        self.port = port
        self.wallet = Wallet(0)
    
    def get_transaction(self):
        """ Waiting for new transaction from from keyboard
        """
        st = input('Enter your new transaction here <pubkey> <amount>:')
        params = st.split(' ')
        pubkey = params[0]
        amount = params[1]
        return pubkey, amount  

    def serialize_wallet(self):
        return pickle.dumps(self.wallet)
    
    def listening(self, p):
        """ Listen to block announcement and normal message from a node
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((localhost, p))
        print(f'Wallet on port {p}, listen to node {self.miner}')
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
                if msg[0] == '5':   # Normal message print
                    print(f'Received message {msg[1:]}')
                elif msg[0] == '4': # New block announced
                    print(f'New block mined!')
                elif msg[0] == '6': # Initialize Miner
                    print(f'Received Miner information')
                    miner = pickle.loads(msg.encode('utf-8'))
                    self.set_miner(miner)
                elif msg[0] == '7': # Updated balance
                    balance = int(msg[1:])
                    self.wallet.balance = balance
        return



