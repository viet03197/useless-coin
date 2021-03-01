from node import Node
from walletapp import WalletApp
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
next_port = 9000
is_first = len(sys.argv) == 3
if is_first:
    t = threading.Thread(target=node.listening)
    t.start()
else:
    if sys.argv[1] == 'node':
        print(f'New node')
        t = threading.Thread(target=node.receiving, args=[port])
        next_port += 1
        t.start()
    else:
        print(f'New wallet')
        wa = WalletApp(port+3000)
        t = threading.Thread(target=wa.receiving, args=[port])
        t.start()
        t2 = threading.Thread(target=wa.listening, args=[wa.port])
        t2.start()