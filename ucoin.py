from block import Block
from node import Node

class UCoin():
    def __init__(self):
        self.chain = self.generate_genesis()
    def generate_genesis(self, data=None):
        """ Generate the first block of UCoin.
            There is no previous data so we can add as we like.
            TODO: Merkle Root
        """
        return Block(data, root=None, 0)