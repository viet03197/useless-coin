# u-coin
 Mini-blockchain Project
How my blockchain work:
- Node and wallet can be set up as follows:
  - First node of a blockchain         : ```python p2p_test.py node 8000```
  - Other nodes (ex. connect to 8000)  : ```python p2p_test.py node register 8000```
  - Wallet                             : ```python p2p_test.py wallet register 8000```

  The id of each node will be generated automatically by the peer it connects to. For example, new nodes connect to 8000 will be assigned from 8001-800x, in which x is the capacity of the peer at 8000. In my code I use 3 so the range is from 8001 to 8003.
  
  When a wallet connects to a node, its corresponding node will broadcast its information to all its connected peers. The information will be used to make transaction later.
  The wallet only communicate with its corresponding node in my project.
  
  The nodes communicate with each other to make transaction and broadcast of new nodes or wallets.  

What I failed to do:
- Effective thread use                 : for my projects, each pair of node-node or node-wallet uses 2 threads in general, another thread for mining for each node. I have to run 2 nodes and 2 wallets at least to carry out a test. So I couldn't carry out bigger test due to system limit.
- Use of true RSA key                  : Even though I included RSA use in my project, I failed to use it in a correct way. The way I generated a transaction is not working with only the RSA Public Key. It was a design fault and I didn't have enough time to come up with a workaround for this issue. Therefore I have to send the RSA key to the node to simulate a transaction. While it worked, it defeated the purpose of using RSA asymmetric keys.
- Communication protocol not effective : I find there are too much information to exchange between node-node and node-wallet, so the communication is very long on my project and I didn't manage to fully test each command. 

Main classes:
- Block                      : block.py
- Node (Miner)               : node.py
- Transaction                : transaction.py trans_pool.py
- Wallet                     : wallet.py walletapp.py
- Offline test               : test.py
- Multithread and p2p test   : p2p_test.py

Communication protocol
