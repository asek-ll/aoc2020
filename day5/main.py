import sys

if len(sys.argv) <= 1:
    raise Exception("No inputs")

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()


def toId(pas):
    pas = pas.replace('B', '1')
    pas = pas.replace('F', '0')
    pas = pas.replace('R', '1')
    pas = pas.replace('L', '0')

    return int(pas, 2)

ids = [toId(line.rstrip()) for line in lines]
print("Part 1: %d" % max(ids))

ids.sort()
for i in range(ids[0],ids[-1]):
    if i not in (ids):
        print("Part 2: %d" % i)
        break
