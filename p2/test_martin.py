import sys
import random
import string
from merkle import Prover, verify
from collections import defaultdict
from matplotlib import pyplot as plt
from hashlib import sha256
from math import log2, ceil
from copy import deepcopy


def test_basic(objects):
    p = Prover()
    commitment = p.build_merkle_tree(deepcopy(objects))

    print(p.generate_proof(1))


test_basic(['a', 'b', 'c'])
