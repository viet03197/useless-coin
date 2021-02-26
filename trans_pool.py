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
        """ Used to look for transactions that haven't been performed yet.
            So we need to reduce the amount of money first
        """
        for i in range(len(self.transaction)):
            if self.transaction[i].input.address == w.pubkey:
                return self.transaction[i]
        return False
    
    def valid_transactions(self):
        result = []
        for t in self.transaction:
            inp = t.input.amount
            out = sum([o.amount for o in t.output])
            if inp == out:
                result.append(t)
        return result
    
    def clear(self):
        self.transaction = []