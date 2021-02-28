from node import Node
#from walletapp import WalletApp
import socket
import sys
import threading

""" Syntax
    python test_p2p node 8000: Open new connection
    python test_p2p node register 8000: Connect to port 8000
    python test_p2p wallet register 8000: Subscribe to node 8000
"""

host = socket.gethostname()
port = int(sys.argv[-1])
node = Node(port)
is_first = len(sys.argv) == 3
if is_first:
    t = threading.Thread(target=node.listening)
    t.start()
else:
    t = threading.Thread(target=node.receiving, args=[port])
    t.start()