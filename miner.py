""" MINER
    Mining Process:
        - Take valid transactions
        - Create a new block with transactions as data
        - Synchronize, add block to chain
        - Clear the transactions
    TODO: Mining
"""
from wallet import Wallet
from transaction import Transaction
from p2p import P2PNode

class Miner():
    def __init__(self, blockchain, pool, wallet=None, p2p=None):
        self.blockchain = blockchain
        self.pool = pool
        self.wallet = wallet
        self.p2p = p2p

    def set_wallet(self, wallet):
        self.wallet = wallet

    def mine(self):
        data = self.pool.valid_transactions()
        #data.append()
        self.blockchain.new_block(data)
        #print(b.hash, b.prev, b.id)
        print(self.blockchain.chain[-1].id, self.blockchain.chain[-1].hash)
        self.pool.clear()
        return