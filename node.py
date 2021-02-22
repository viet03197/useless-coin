"""
    TODO List
    - Mine
    - Transaction
    - P2P Network
"""
import sys
import socket
import hashlib
from random import randint
from block import Block

class Node():
    current_block = 0
    def __init__(self, host, port, peers=[], peers_assigned=[], connections=dict()):
        self.host = host
        self.port = port
        self.peers = peers
        self.peers_assigned = peers_assigned
        self.connections = connections
    
    def update_block(self):
        self.current_block+=1
        return

    def check(self, digest, diff):
        return digest[0:diff] == b'0'*diff
    
    def puzzle(self, b):
        while True:
            if self.current_block > b.id:
                return
            else:
                nonce = randint(0, int('ffffff', 16))
                d = b.hash + str(nonce).encode()
                d = hashlib.md5(d).hexdigest()
                if self.check(d, b.difficulty):
                    return nonce
    
    def mine(self):

