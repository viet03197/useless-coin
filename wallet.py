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

def data_hash(data):
    return SHA256.new(data)

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
            verifier = pss.new(self.key).verify(data_hash(trans.output),trans.input.signature)
        except:
            return False
        return True