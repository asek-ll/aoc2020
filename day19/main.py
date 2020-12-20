import sys
import re

if len(sys.argv) <= 1:
    raise Exception("No inputs")

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()


ll = [l.rstrip() for l in lines]

i = 0
rules = {}
while len(ll[i]) > 0:
    id, content = ll[i].split(': ')
    rules[int(id)] = content
    i += 1


msgs = []

i += 1
while i < len(ll):
    msgs.append(ll[i])
    i += 1


def comp(r):
    cache = {}

    def sub_compile(i):
        if i in cache:
            return cache[i]

        rule = r[i]

        if rule[0] == '"':
            res = rule[1]
            cache[i] = res
            return res


        parts = rule.split(" | ")
        res_parts = []
        for p in parts:
            res = []
            ids = map(int, p.split(" "))
            for id in ids:
                res.append(sub_compile(id))
        
            res_parts.append("".join(res))

        if len(res_parts) > 1:
            res = "(%s)" % ("|".join(res_parts))
        else:
            res = res_parts[0]

        cache[i] = res

        return res

    p42 = sub_compile(42)
    cache[8] = "(%s)+" % p42

    p31 = sub_compile(31)

    res = '|'.join(["(%s){%d}(%s){%d}" % (p42, i, p31, i) for i in range(1, 21)])

    cache[11] = "(%s)" % res

    return re.compile('^%s$' % sub_compile(0))

r = comp(rules)

matched = list(filter(lambda x: r.match(x), msgs))
print("Part 1/2: %d" % (len(matched)))
