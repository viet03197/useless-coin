"""
    WALLET FOR THE BLOCKCHAIN
    TODO
    Possible action:
    - Send the transactions
    - Subscribe to a node
"""
from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from transaction import Transaction
from trans_pool import TransactionPool

def data_hash(data):
    return SHA256.new(data.encode())

def output_list(outputs):
    return ''.join([x.string_repre() for x in outputs])

class Wallet():
    def __init__(self, balance):
        self.balance = balance
        # TODO GENERATE PAIRS OF KEY !!!
        self.key = RSA.generate(1024)
        self.pubkey = self.key.public_key()

    def sign_data(self, data):
        """ Sign data with the private key of this wallet
        """
        return pss.new(self.key).sign(data_hash(data))
    
    def verify_transaction(self, trans):
        try:
            verifier = pss.new(self.key).verify(data_hash(output_list(trans.output)),trans.input.signature)
            print('Authentic')
        except:
            print('Not authentic')
            return False
        return True

    def create_transaction(self, receiver, amount, pool):
        if (amount > self.balance):
            print('Transaction not allowed: Insufficient balance!')
            return False
        tmp = pool.check(self)
        if tmp == False:
            new_trans = Transaction(self, receiver, amount)
            pool.add(new_trans)
            return new_trans.id
        else:
            #tmp.update(self, receiver, tmp.output[0].amount)
            new_trans = Transaction(self, receiver, amount)
            tmp.update(self, receiver, amount)
            #pool.add(new_trans)
            return tmp.id
    
    def update_balance(self, chain):
        """ Look for transactions related to this wallet in the last mined block
        """
        result = self.balance
        increase = 0
        decrease = 0
        if isinstance(chain.chain, list):
            for t in chain.chain[-1].data:
                if t.input.address == self.pubkey:
                    decrease += result - t.output[1].amount
                else:
                    for o in t.output:
                        if o.pubkey == self.pubkey:
                            print(f'receive {o.amount}')
                            increase += o.amount
            self.balance += (increase - decrease)
            return
        else:
            return
        
"""
# Test wallet
w1 = Wallet(200)
w2 = Wallet(480)
poolz = TransactionPool()
id1 = w1.create_transaction(w2, 50, poolz)
id2 = w1.create_transaction(w2, 10, poolz)
for p in poolz.transaction:
    print(p.id, p.input.amount, p.input.address)
    for o in p.output:
        print(o.string_repre())
print(poolz.valid_transactions())
print(w1.balance)
print(w2.balance)
"""