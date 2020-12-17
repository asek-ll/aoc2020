import sys

if len(sys.argv) <= 1:
    raise Exception("No inputs")

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()

group = []
groups = [group]
for line in lines:
    l = line.rstrip()
    if len(l) == 0:
        group = []
        groups.append(group)
    else:
        group.append(set([c for c in l]))


def union(peoples):
    s = set([])
    for p in peoples:
        s = s.union(p)

    return s

def intersect(peoples):
    s = set(peoples[0])
    for i in range(1, len(peoples)):
        s = s.intersection(peoples[i])

    return s


union_groups_size = [len(union(s)) for s in groups]

print("Part 1: %d" % sum(union_groups_size))

intersect_groups_size = [len(intersect(s)) for s in groups]

print("Part 1: %d" % sum(intersect_groups_size))
