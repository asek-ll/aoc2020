import sys

if len(sys.argv) <= 1:
    raise Exception("No inputs")

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()
# -2          (-1,-2) ( 0,-2) (+1,-2)
# -1              (-1,-1) ( 0,-1) (+1,-1)
# 0           (-1, 0) ( 0, 0) (+1, 0)
# +1              (-1,+1) ( 0,+1) (+1,+1)
# +2          (-1,+2) ( 0,+2) (+1,+2) 


DIR = {
    "e": lambda p: (p[0]+1, p[1]),
    "w": lambda p: (p[0]-1, p[1]),
    "ne": lambda p: (p[0] + (p[1] % 2), p[1]-1),
    "nw": lambda p: (p[0]- 1 + (p[1] % 2), p[1]-1),
    "se": lambda p: (p[0] + (p[1] % 2), p[1]+1),
    "sw": lambda p: (p[0]- 1 + (p[1] % 2), p[1]+1),
}

def parse_line(l):
    l = l.rstrip()
    res = []
    i = 0
    while i < len(l):
        if l[i] == 'e' or l[i] == 'w':
            res.append(l[i])
        else:
            res.append(l[i:i+2])
            i += 1
        i += 1
    return res

def get_destination(path):
    pos = (0,0)
    for d in path:
        pos = DIR[d](pos)

    return pos

def get_state(pathes):
    state = set([])
    for path in pathes:
        pos = get_destination(path)
        if pos in state:
            state.remove(pos)
        else:
            state.add(pos)

    return state


def part_1(state):
    return len(state)

def get_adjacent(tile):
    adjacent = []
    for d in DIR:
        adjacent.append(DIR[d](tile))

    return adjacent

def do_day(state):
    next_state = set([])

    adjacent_count_by_white_tile = {}

    for tile in state:
        adjacent = get_adjacent(tile)

        adjacent_count = 0
        for ad in adjacent:
            if ad not in state:
                if ad not in adjacent_count_by_white_tile:
                    adjacent_count_by_white_tile[ad] = 1
                else:
                    adjacent_count_by_white_tile[ad] += 1
            else:
                adjacent_count += 1


        if adjacent_count > 0 and adjacent_count < 3:
            next_state.add(tile)


    for tile in adjacent_count_by_white_tile:
        if adjacent_count_by_white_tile[tile] == 2:
            next_state.add(tile)

    return next_state

def debug(state):
    for j in range(-6, 7):
        line = []
        if j % 2 > 0:
            line.append('  ')

        for i in range(-6, 7):
            if (i, j) in state:
                line.append(' X  ')
            else:
                line.append(' -  ')
        
        print(''.join(line))


def part_2(state):

    for i in range(0, 100):
        state = do_day(state)


    return len(state)


parsed = [parse_line(l) for l in lines]
state = get_state(parsed)

print("Part 1: %d" % part_1(state))
print("Part 2: %d" % part_2(state))




