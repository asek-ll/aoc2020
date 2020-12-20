import sys

if len(sys.argv) <= 1:
    raise Exception("No inputs")

with open(sys.argv[1], 'r') as f:
    lines = list(map(lambda x: x.rstrip(), f.readlines()))

fields = {}
i = 0
while len(lines[i]) > 0:
    name, cond = lines[i].split(": ")
    cp = list(map(lambda x: tuple(map(int, x.split('-'))), cond.split(" or ")))
    fields[name] = cp
    i += 1

i += 2
while len(lines[i]) > 0:
    ticket = tuple(map(int, lines[i].split(",")))
    i += 1

o_t = []
i += 2
while i < len(lines):
    o_t.append(tuple(map(int, lines[i].split(","))))
    i += 1

def field_to_func(f):

    def fn(x):
        for c in f:
            if x >= c[0] and x <= c[1]:
                return True

        return False

    return fn


ff = {k: field_to_func(fields[k]) for k in fields}

def recognize(fields, ticket):
    res = []
    for i in range(0, len(ticket)):
        val = ticket[i]
        valid = set([])
        for f in fields:
            if fields[f](val):
                valid.add(f)
        
        res.append(valid)
    
    return res


def optimize(result):

    id_to_field = {}
    m = set([])

    changed = True
    while changed:
        changed = False
        for i in range(0, len(result)):
            r = result[i]
            if len(r) == 1:
                c = next(iter(r))
                if c not in m:
                    changed = True
                    id_to_field[i] = c
                    m.add(c)
                    for j in range(0, len(result)):
                        if j != i and c in result[j]:    
                            result[j] = set(filter(lambda x: x != c, result[j]))
    









    # changed = True

    # while changed:
    #     changed = False

    #     matched = map(lambda x: next(iter(x)), filter(lambda x: len(x) == 1, result))
    #     for m in matched:
    #         for i in range(0, len(result)):
    #             r = result[i]
    #             if len(r) > 1 and m in r:
    #                 changed = True
    #                 result[i] = set(filter(lambda x: x != m, r))


    return result

expected = optimize(recognize(ff, ticket))


def recognize_other(exp, ticket, fields):
    res = []
    for i in range(0, len(ticket)):
        valid = set([])
        t = ticket[i]
        classes = exp[i]
        for c in classes:
            if fields[c](t):
                valid.add(c)
    

        res.append(valid)
    
    return res

def find_invalid_nums(exp, ticket, fields):
    rs = recognize_other(exp, ticket, fields)
    result = []
    for i in range(0, len(rs)):
        if len(rs[i]) == 0:
            result.append(ticket[i])

    return result


def part_1(exp, tickets, fields):
    res = 0
    for t in o_t:
        res += sum(find_invalid_nums(expected, t, ff))

    return res


def part_2(exp, tickets, fields, ticket):
    base = list(exp)
    for t in o_t:
        rs = optimize(recognize_other(exp, t, fields))
        is_valid = True
        for r in rs:
            if len(r) == 0:
                is_valid = False
                break
        
        if is_valid:
            for i in range(0, len(rs)):
                base[i] = base[i].intersection(rs[i])

    base = optimize(base)

    res = 1
    for i in range(0, len(base)):
        d = list(filter(lambda x: x.startswith("departure"), base[i]))
        if len(d) > 0:
            res *= ticket[i]

    return res

print("Part 1: %d" % (part_1(expected, o_t, ff)))    

print("Part 2: %d" % part_2(expected, o_t, ff, ticket)) 
