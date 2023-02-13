from typing import Optional, List
from hashlib import sha256
from copy import deepcopy
from math import floor


def verify(obj: str, proof: str, commitment: str) -> bool:

    raise NotImplementedError


class Prover:
    def __init__(self):
        self.tree = []

    # Build a merkle tree and return the commitment
    def build_merkle_tree(self, objects: List[str]) -> str:

        # Fill leaf with None if number of leafs is not a power of two
        self.tree = objects + \
            ([None] * (self.next_power_of_two(len(objects)) - len(objects)))

        parents = self.tree

        while len(parents) > 1:

            parents = [sha256((parents[i] if parents[i] is not None else '' + parents[i+1] if parents[i+1] is not None else '').encode()).hexdigest()
                       for i in range(0, len(parents), 2)]
            self.tree = parents + self.tree

        print(self.tree)
        return self.tree[0]

    def get_leaf(self, index: int) -> Optional[str]:
        leaf_index = floor(len(self.tree)/2) + index
        return self.tree[leaf_index]

    def generate_proof(self, index: int) -> Optional[str]:
        if len(self.tree) == 1:
            return self.tree[0]

        if self.get_leaf(index) is None:
            return None

        proof = []

        # Start proof with node
        next_node_index = floor(len(self.tree)/2) + index

        # TODO Only include nodes that cannot be calculate

        # if right sibling leaf node, start with left
        if next_node_index % 2 == 0:
            next_node_index -= 1

        while (next_node_index > 0):
            proof.append(self.tree[next_node_index])
            proof.append(self.tree[self.calc_sibling_index(next_node_index)])

            next_node_index = floor((next_node_index - 1) / 2)

        # Add Merkle root to proof
        proof.append(self.tree[0])

        return ", ".join(proof)

    # Source: https://stackoverflow.com/questions/32419967/python-closest-power-of-two-to-target
    def next_power_of_two(self, target):
        if target > 1:
            for i in range(1, int(target)):
                if (2 ** i >= target):
                    return 2 ** i
        else:
            return 2

    def calc_sibling_index(self, index):
        return index + 1 if index % 2 == 1 else index - 1
