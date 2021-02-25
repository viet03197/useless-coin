""" TRANSACTION
    This consists of 3 main things:
    - id: unique id generated by python.uuid
    - w1 is sender, w2 is receiver
"""
import uuid
import json
from wallet import Wallet

class Transaction():
    def __init__(self, w1, w2, amount=None):
        self.id = self.generate_id().hex
        self.output = []
        outputs_string = output_list(self.output)
        self.input = Input(w1, outputs_string)
        return
    
    def generate_id(self):
        return uuid.uuid4()
    
    def update(self, w1, w2, amount):
        if amount > w1.balance:
            return
        #out = Output(w1.balance - amount, w1.pubkey)
        w1.balance -= amount
        out = Output(amount, w2.pubkey)
        self.output.append(out)
        outputs_string = output_list(self.output)
        self.input = Input(w1, outputs_string)
        return

class Input():
    def __init__(self, w1, output):
        self.amount = w1.balance
        self.address = w1.pubkey
        self.signature = w1.sign_data(output)

class Output():
    def __init__(self, amount, pubkey):
        self.amount = amount
        self.pubkey = pubkey
    
    def string_repre(self):
        return json.dumps({"amount":self.amount, "pubkey":str(self.pubkey)})

def output_list(outputs):
    return ''.join([x.string_repre() for x in outputs])
        

w1 = Wallet(200)
w2 = Wallet(200)
t = Transaction(w1, w2, amount=50)
print(w1.balance, w1.pubkey)
print(t.id, t.input, t.output)
print(w1.verify_transaction(t))
t.update(w1, w2, 50)
print(w1.balance, w1.pubkey)
print(t.id, t.input)
for o in t.output:
    print(o.amount, o.pubkey)
