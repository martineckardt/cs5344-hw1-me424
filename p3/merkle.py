from typing import Optional, List
from hashlib import sha256
from math import floor
from json import dumps, loads


def verify(obj: str, proof: str, commitment: str) -> bool:

    if obj is None or proof is None or commitment is None:
        return False

    proof = loads(proof)

    try:
        return commitment == calc_commitment(proof, obj)
    except Exception as e:
        print("Error in verify: ", e)
        return False


def calc_commitment(proof: list, obj: str) -> str:
    if type(proof[0]) is list:
        return create_hash(calc_commitment(proof[0], obj), proof[1])

    if type(proof[1]) is list:
        return create_hash(proof[0], calc_commitment(proof[1], obj))

    if (type(proof[0]) is str or proof[0] is None) and (type(proof[1]) is str or proof[1] is None):
        if (proof[0] != obj and proof[1] != obj):
            raise Exception("Object not in proof")

        return create_hash(proof[0], proof[1])

    raise Exception("Unexcepted type in proof")


# Create hash from to concatenated strings. Treat None as empty string
def create_hash(obj1: str, obj2: str) -> str:
    return sha256((obj1 if obj1 is not None else '' + obj2 if obj2 is not None else '').encode()).hexdigest()


class Prover:
    def __init__(self):
        self.tree = []

    # Build a merkle tree and return the commitment
    def build_merkle_tree(self, objects: List[str]) -> str:

        # Fill leafs with None if number of leafs is not a power of two
        self.tree = objects + \
            ([None] * (self.next_power_of_two(len(objects)) - len(objects)))

        parents = self.tree

        while len(parents) > 1:

            parents = [create_hash(parents[i], parents[i+1])
                       for i in range(0, len(parents), 2)]
            self.tree = parents + self.tree

        print(self.tree)
        return self.tree[0]

    def get_leaf(self, index: int) -> Optional[str]:
        leaf_index = self.calc_index(leaf_index=index)

        return self.tree[leaf_index] if leaf_index < len(self.tree) else None

    def generate_proof(self, index: int) -> Optional[str]:

        leaf_value = self.get_leaf(index)
        if leaf_value is None:
            return None

        proof = leaf_value

        next_node_index = self.calc_index(leaf_index=index)

        while (next_node_index > 0):

            sibling = self.tree[self.calc_sibling_index(next_node_index)]

            if (self.is_left_sibling(next_node_index)):
                proof = [proof, sibling]
            else:
                proof = [sibling, proof]

            next_node_index = self.calc_parent_index(next_node_index)

        return dumps(proof)

    def is_left_sibling(self, index):
        return index % 2 == 1

    def calc_sibling_index(self, index):
        return index + 1 if self.is_left_sibling(index) else index - 1

    def calc_parent_index(self, index):
        return floor((index - 1) / 2)

    def calc_index(self, leaf_index):
        return floor(len(self.tree)/2) + leaf_index

    # Source: https://stackoverflow.com/questions/32419967/python-closest-power-of-two-to-target
    def next_power_of_two(self, target):
        if target > 1:
            for i in range(1, int(target)):
                if (2 ** i >= target):
                    return 2 ** i
        else:
            return 2
