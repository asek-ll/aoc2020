import sys

if len(sys.argv) <= 1:
    raise Exception("No inputs")

with open(sys.argv[1], 'r') as f:
    lines = [l.rstrip() for l in f.readlines()]

def parse(ls):
    i = ls.index('')
    return (tuple(map(int, ls[1:i])), tuple(map(int, ls[i+2:])))


def step(state):
    top = []
    is_end = False
    for i in range(0, len(state)):
        if len(state[i]) == 0:
            is_end = True

    if is_end:
        return (False, state)

    ns = []
    for i in range(0, len(state)):
        top.append(state[i][0])
        ns.append((state[i][1:]))

    mx = max(top)
    idx = top.index(mx)

    ns[idx] = ns[idx] + tuple(sorted(top)[::-1])

    return (True, tuple(ns))

st = parse(lines)

def get_winner(state):
    for i in range(0, len(state)):
        if len(state[i]) > 0:
            return i

def score(state, winner):
    p = state[winner]
    return sum([p[i] * (len(p)-i) for i in range(0, len(p))])

s1 = st
while True:
    is_good, s1 = step(s1)
    if not is_good:
        break

print("Part 1: %d" % score(s1, get_winner(s1)))


def is_end(state):
    is_end = False
    for p in state:
        if len(p) == 0:
            return True

    return False

def draw(state):
    top = []
    is_end = False
    ns = []
    for i in range(0, len(state)):
        top.append(state[i][0])
        ns.append(state[i][1:])

    return (top, tuple(ns))

def is_recurse(top, state):
    for i in range(0, len(top)):
        if top[i] > len(state[i]):
            return False

    return True

def do_recurse(top, state):
    ns = []
    for i in range(0, len(top)):
        ns.append(state[i][:top[i]])

    state, winner = rec_game(tuple(ns))

    return winner

def rec_game(init_state):
    st = init_state

    states = set([])

    while not is_end(st):
        if st in states:
            return (st, 0)

        states.add(st)

        # for p in st:
            # print(p)

        d, st = draw(st)

        # print(d)

        if is_recurse(d, st):
            # print("RECURESE!!!")
            winner = do_recurse(d, st)
        else:
            winner = d.index(max(d))

        # print("Winner %d" % (winner + 1))

        tail = [d[winner]]
        for i in range(0, len(d)):
            if i != winner:
                tail.append(d[i])

        st = list(st)

        st[winner] = st[winner] + tuple(tail)

        st = tuple(st)

    return (st, get_winner(st))

print("Part 2: %d" % score(*rec_game(st)))
