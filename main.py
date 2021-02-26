import socket
import sys
import threading
from miner import Miner
from wallet import Wallet
from transaction import Transaction
from trans_pool import TransactionPool
from walletapp import WalletApp
from ucoin import UCoin
from p2p import P2PNode

""" Syntax
    python test_p2p node 8000: Open new connection
    python test_p2p node register 8000: Connect to port 8000
    python test_p2p wallet register 8000 10000: Subscribe to node 8000
"""
host = socket.gethostname()
port = int(sys.argv[-1])
p2pnode = P2PNode(port)
is_first = len(sys.argv) == 3
block = None
if is_first:
    block = UCoin.generate_genesis('Genesis block is here')
    x = Miner(block, TransactionPool())
    t = threading.Thread(target=p2pnode.listening)
    t.start()
else:
    if sys.argv[1] == 'node':
        t = threading.Thread(target=p2pnode.receiving, args=[port])
        t.start()
    elif sys.argv[2] == 'wallet':
        w = WalletApp(port = port)
        
        t = threading.Thread(target=)
