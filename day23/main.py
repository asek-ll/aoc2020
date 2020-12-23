import sys

if len(sys.argv) <= 1:
    raise Exception("No inputs")

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()

def parse(lines):
    return [int(c) for c in lines[0].rstrip()]

def step(n):
    current = n[0]
    remains = [current] + n[4:]
    extracted = n[1:4]

    remains_sorted = sorted(remains)
    t_idx = remains_sorted.index(current) - 1
    if t_idx < 0:
        t_idx = len(remains) - 1

    target = remains_sorted[t_idx]
    target_pos = remains.index(target)

    remains[target_pos+1:target_pos+1] = extracted

    return remains[1:] + [current]

def step_in_place(state):
    current = state['current']
    
    extracted = []
    nxt = current
    for i in range(0, 3):
        nxt = nxt['next']
        extracted.append(nxt['num'])

    target = current['num'] - 1
    while target in extracted:
        target -= 1

    if target <= 0:
        target = state['len']

    while target in extracted:
        target -= 1

    target_num = state['num_by_no'][target]

    first_extracted = current['next']
    last_extracted = nxt

    current['next'] = last_extracted['next']

    target_next = target_num['next']
    target_num['next'] = first_extracted
    last_extracted['next'] = target_next

    state['current'] = current['next']

    return state

nums = parse(lines)

def part_1(nums):

    n = nums
    for i in range(0, 100):
        n = step(n)

    first_cap_idx = n.index(1)

    result = n[first_cap_idx+1:] + n[:first_cap_idx]

    return ''.join([str(r) for r in result])

def debug(num):
    r = [num['num']]
    c = num['next']
    while c['num'] != 1:
        r.append(c['num'])
        c = c['next']
    print(r)

def part_2(nums):

    n = nums
    T = 1000000
    for i in range(len(n)+1, T + 1):
        n.append(i)

    ll = [{'num':i} for i in n]
    for i in range(0, len(n)):
        t = (i + 1) % len(n)
        ll[i]['next'] = ll[t]

    num_by_no = {}
    for i in range(0, len(n)):
        num_by_no[n[i]] = ll[i]

    state = {"num_by_no": num_by_no, "current": ll[0], "len": len(ll)}

    # debug(num_by_no[1])
    for i in range(0, 10000000):
        state = step_in_place(state)
        # debug(num_by_no[1])
    
    num1 = num_by_no[1]

    return num1['next']['num'] * num1['next']['next']['num']

print("Part 1: %s" % (part_1(nums)))
print("Part 2: %d" % (part_2(nums)))
