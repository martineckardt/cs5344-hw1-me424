import string
import random
import hashlib
from merkle import Prover, verify

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

        self.p = Prover()

    # Populate the fields self.treenodes, self.sk and self.pk. Returns self.pk.

    def KeyGen(self, seed: int) -> string:
        p = Prover()
        pairs = KeyPairGen(self.d, seed)

        self.treenodes = [pk for (sk, pk) in pairs.items()]
        self.sk = [sk for (sk, pk) in pairs.items()]
        self.pk = p.build_merkle_tree(self.treenodes)

        return self.pk

    # Returns the path SPj for the index j
    # The order in SPj follows from the leaf to the root.
    def Path(self, j: int) -> string:
        proof = self.p.generate_proof(j)

        # TODO Translate proof to concatenated string (deterministic order of parents)
        path = ''

        return path

    # Returns the signature. The format of the signature is as follows: ([sigma], [SP]).
    # The first is a sequence of sigma values and the second is a list of sibling paths.
    # Each sibling path is in turn a d-length list of tree node values.
    # All values are 64 bytes. Final signature is a single string obtained by concatentating all values.
    def Sign(self, msg: string) -> string:
        # zj = H(j ∥ m) mod 2^d
        return NotImplementedError
