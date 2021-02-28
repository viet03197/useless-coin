""" This is an offline test for most functions of my blockchain
"""
from miner import Miner
from ucoin import UCoin
from wallet import Wallet
from transaction import Transaction, output_list
from trans_pool import TransactionPool

w1 = Wallet(465)
print(w1.pubkey.exportKey)
w2 = Wallet(344)
w3 = Wallet(162)
poolz = TransactionPool()
blockchain = UCoin('Genesis test')
m1 = Miner(blockchain, poolz, w1)
m2 = Miner(blockchain, poolz, w2)
t1 = w1.create_transaction(w2.pubkey, 40, m1.pool)
t2 = w1.create_transaction(w2.pubkey, 16, m1.pool)
print('============================================================')
for p in m1.pool.transaction:
    print(p.id, p.input.amount, p.input.address)
    for o in p.output:
        print(o.string_repre())
m1.mine()
w1.update_balance(m1.blockchain)
w2.update_balance(m2.blockchain)
w3.update_balance(m1.blockchain)
print('current balance: ',w1.balance, w2.balance, w3.balance)
print('============================================================')
t3 = w1.create_transaction(w3.pubkey, 60, m1.pool)
t4 = w3.create_transaction(w1.pubkey, 19, m1.pool)
for p in m2.pool.transaction:
    print(p.id, p.input.amount, p.input.address)
    for o in p.output:
        print(o.string_repre())
m2.mine()
w1.update_balance(m1.blockchain)
w2.update_balance(m2.blockchain)
w3.update_balance(m1.blockchain)
print('current balance: ',w1.balance, w2.balance, w3.balance)