import sys

if len(sys.argv) <= 1:
    raise Exception("No inputs")

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()

pk1, pk2 = nums = [int(l.rstrip()) for l in lines]

def transform(loop, subject = 7):
    val = 1
    for i in range(0, loop):
        val = (val * subject) % 20201227

    return val

def brut(public):
    val = 1
    for i in range(0, 20201227):
        val = (val * 7) % 20201227
        if val == public:
            return i+1


print("Part 1: %d" % transform(brut(pk1), pk2))
