import sys

if len(sys.argv) <= 1:
    raise Exception("No inputs")

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()


rules = {}

for line in lines:
    l = line.rstrip('\n.')
    key, contain = l.split(' contain ')

    out = []
    if contain != 'no other bags':
        bags = contain.split(', ')
        for bag in bags:
            count, name = bag.split(' ', 1)
            if name[-1] != 's':
                name += 's'
            out.append((int(count), name))

    rules[key] = out


def to_contains_dict(rules):
    res = {}
    for name in rules:
        for sub_bag in rules[name]:
            sub_name = sub_bag[1]
            if sub_name not in res:
                res[sub_name] = []

            res[sub_name].append(name)

    return res

def find_contains(rules, target):
    res = set([])
    if target not in rules:
        return res

    for c in rules[target]:
        res.add(c)
        res = res.union(find_contains(rules, c))

    return res

def count_bags(rules, target):
    nested = rules[target[1]]
    if len(nested) == 0:
        return target[0]

    res = target[0]
    for n in nested:
        res += target[0] * count_bags(rules, n)

    return res


contains_rules = to_contains_dict(rules)

target = 'shiny gold bags'
print("Part 1: %d" % len(find_contains(contains_rules, target)))

print("Part 2: %d" % (count_bags(rules, (1, target))-1))
