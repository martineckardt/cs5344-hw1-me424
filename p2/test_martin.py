from merkle import Prover, verify
from copy import deepcopy


def test_basic(objects):
    p = Prover()
    commitment = p.build_merkle_tree(deepcopy(objects))

    print(p.generate_proof(4))


test_basic(['a', 'b', 'c', 'd', 'e'])
