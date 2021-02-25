"""
"""
from transaction import Transaction
class TransactionPool():
    def __init__(self):
        self.transaction = []
        self.index = dict()

    def add(self, transaction):
        if transaction.id in self.index:
            self.transaction[self.index[transaction.id]] == transaction
        else:
            self.transaction.append(transaction)
            self.index[transaction.id] = len(self.transaction)-1
        return

    def check(self, w):
        for i in range(len(self.transaction)):
            if self.transaction[i].input.address == w.pubkey:
                return self.transaction[i]
        return False