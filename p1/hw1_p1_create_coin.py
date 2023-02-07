import sys
import hashlib

watermark_length = 4

# Source: https://people.csail.mit.edu/rivest/pubs/RS96b.pdf


def create_micromint_coin(netid, k=4, n=28):
    coins = {}

    watermark = hashlib.sha256(netid.encode("ascii")).hexdigest()[:4]

    print(watermark)
    print(bin(int(watermark, base=16))[2:].zfill(16))

    counter = 0
    while True:
        c_i = watermark + f"{counter:0{12}x}"

        c_i_hash = bin(int(hashlib.sha256(bytes.fromhex(
            c_i)).hexdigest(), base=16)).lstrip('0b').zfill(256)[:n]

        if c_i_hash in coins:
            coins[c_i_hash].append(c_i)
            if len(coins[c_i_hash]) == 4:
                print(coins[c_i_hash])
                break
        else:
            coins[c_i_hash] = [c_i]

        counter += 1


if __name__ == "__main__":
    netid = sys.argv[1]
    create_micromint_coin(netid)
