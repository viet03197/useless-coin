from block import Block
from node import Node

class UCoin():
    def __init__(self, data=None):
        self.chain = [self.generate_genesis(data)]
    def generate_genesis(self, data=None):
        """ Generate the first block of UCoin.
            There is no previous data so we can add as we like.
            TODO: Merkle Root
        """
        # Placeholder for root
        root = None
        return Block(data, root, 0, None, diff=3)
    
    def new_block(self, data):
        """ Add new block to the current blockchain
        """    
        self.chain.append(self.chain[-1].mine(data))
        return

    def chain_validate(self, new_chain):
        """ TODO: REMINDER, PUT SOMETHING PUBLIC IN THE GENESIS !!!!
        """
        if new_chain[0].get_hash() != self.generate_genesis().get_hash():
            return False        # Different Genesis Block => Reject
        for i in range(1, len(new_chain)):
            if (new_chain[i].prev != new_chain[i-1].hash):
                return False
        return True
    
    def replace_chain(self, new_chain):
        """ Validate a new chain and replace the current chain by a new one if valid
        """
        if len(new_chain) <= len(self.chain): # Longest chain = best chain
            return
        elif self.chain_validate(new_chain):
            self.chain = new_chain[:] # Create a copy, not reference
        return


""" Test
uc = UCoin('Very first block!')
uc.new_block('A transaction here')
uc.new_block('Another transaction here')
for b in uc.chain:
    print(b.hash, b.prev, b.id)
"""