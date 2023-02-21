import string
import random
import hashlib
from math import floor
from pprint import pprint

# return the hash of a string


def SHA(s: string) -> string:
    return hashlib.sha256(s.encode()).hexdigest()

# transfer a hex string to integer


def toDigit(s: string) -> int:
    return int(s, 16)

# generate 2^d (si^{-1}, si) pairs based on seed r


def KeyPairGen(d: int, r: int) -> dict:
    pairs = {}
    random.seed(r)
    for i in range(1 << d):
        cur = random.randbytes(32).hex()
        while cur in pairs:
            cur = random.randbytes(32).hex()
        pairs[cur] = SHA(cur)
    return pairs


class MTSignature:
    def __init__(self, d, k):
        self.d = d
        self.k = k
        self.treenodes = [None] * (d+1)
        for i in range(d+1):
            self.treenodes[i] = [None] * (1 << i)
        self.sk = [None] * (1 << d)
        self.pk = None  # same as self.treenodes[0][0]

    # Populate the fields self.treenodes, self.sk and self.pk. Returns self.pk.

    def KeyGen(self, seed: int) -> string:
        pairs = KeyPairGen(self.d, seed)
        # Start with the public keys on the lowest level of the tree
        nodes = list(pairs.values())
        self.treenodes = [nodes]

        # Build the tree upwards
        while len(nodes) > 1:
            # Compute the parent nodes
            parents = [SHA(format(floor(i/2), "b").zfill(256) + nodes[i] + nodes[i+1])
                       for i in range(0, len(nodes), 2)]

            # Add the parent nodes to the tree
            self.treenodes.insert(0, parents)
            nodes = parents

        self.sk = list(pairs.keys())

        # The root of the tree is the public key
        self.pk = self.treenodes[0][0]
        print('=== Tree ===')
        pprint(self.treenodes)

        return self.pk

    # Returns the path SPj for the index j
    # The order in SPj follows from the leaf to the root.
    def Path(self, j: int) -> string:

        level = self.d
        path = []

        while level > 0:
            # Calcluate the sibling index
            if j % 2 == 0:
                j += 1
            else:
                j -= 1

            path.append(self.treenodes[level][j])
            level -= 1

            # Calculate the parent index
            j = floor(j/2)

        print('=== Path ===')
        print(path)

        return "".join(path)

    # Returns the signature. The format of the signature is as follows: ([sigma], [SP]).
    # The first is a sequence of sigma values and the second is a list of sibling paths.
    # Each sibling path is in turn a d-length list of tree node values.
    # All values are 64 bytes. Final signature is a single string obtained by concatentating all values.
    def Sign(self, msg: string) -> string:
        js = [format(j, "b").zfill(256) for j in range(1, self.k)]

        # Determine which key shall be used
        # zj = H(j ∥ m) mod 2^d
        z_j = [int(SHA(j + msg), 16) % (2 ** self.d) for j in js]

        # Compute the sigma values
        sigma = [SHA(self.sk[z] + msg) for z in z_j]

        SP = [self.Path(z) for z in z_j]

        print("Signature: " + "".join(sigma) + "".join(SP))

        return "".join(sigma) + "".join(SP)


m = MTSignature(4, 3)
m.KeyGen(1)
