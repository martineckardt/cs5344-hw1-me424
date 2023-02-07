import sys
import hashlib
import string


def findCollidingNetId(netid):
    watermark_length = 4

    watermark = hashlib.sha256(netid.encode("ascii")).hexdigest()[:4]

    for c1 in string.ascii_lowercase:
        for c2 in string.ascii_lowercase:
            for c3 in range(10):
                for c4 in range(10):
                    for c5 in range(10):

                        new_netid = c1 + c2 + str(c3) + str(c4) + str(c5)

                        new_watermark = hashlib.sha256(
                            new_netid.encode("ascii")).hexdigest()[:4]

                        if new_watermark == watermark and new_netid != netid:
                            print(new_netid)
                            return

    print("No collision found")


if __name__ == "__main__":
    netid = sys.argv[1]
    findCollidingNetId(netid)
