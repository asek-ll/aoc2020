import sys

if len(sys.argv) <= 1:
    raise Exception("No inputs")

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()

field = [list(l.rstrip()) for l in lines]

DIRECTIONS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1),
]

def get_adjastend(field, i, j):
    res = []
    for y in range(max(0, i-1), min(len(field), i + 2)):
        for x in range(max(0, j-1), min(len(field[y]), j+2)):
            if not (y == i and x == j):
                res.append(field[y][x])

    return res

def get_adjastend_occuped_count(adjastends):
    return len(filter(lambda x: x == '#', adjastends))

def get_new_state(field, i, j):
    state = field[i][j]

    if state == '.':
        return '.'

    occuped = get_adjastend_occuped_count(get_adjastend(field, i, j))

    if state == 'L' and occuped == 0:
        return '#'

    if state == '#' and occuped >= 4:
        return 'L'

    return state


def step(field):
    new_field = []
    for i in range(0, len(field)):
        new_line = []
        for j in range(0, len(field[i])):
            new_line.append(get_new_state(field, i, j))

        new_field.append(new_line)

    return new_field

def count_occuped(field):
    result = 0
    for i in range(0, len(field)):
        for j in range(0, len(field[i])):
            if field[i][j] == '#':
                result += 1

    return result

def debug(field):
    for l in field:
        print("".join(l))


def get_adjastend_in_direction(d, field, i, j, cache):
    if i < 0 or j < 0 or i >= len(field) or j >= len(field[i]):
        return '.'

    current = field[i][j]

    if current != '.':
        return current

    if (i,j) in cache and d in cache[(i,j)]:
        return cache[(i,j)][d]


    i_n = i + d[0]
    j_n = j + d[1]

    res = get_adjastend_in_direction(d, field, i_n, j_n, cache)

    if (i, j) not in cache:
        cache[(i, j)] = {}

    cache[(i, j)][d] = res

    return res


def get_adjastend2(field, i, j, cache):
    res = []
    for d in DIRECTIONS:
        res.append(get_adjastend_in_direction(d, field, i + d[0], j + d[1], cache))

    return res

def get_new_state2(field, i, j, cache):
    state = field[i][j]

    if state == '.':
        return '.'

    occuped = get_adjastend_occuped_count(get_adjastend2(field, i, j, cache))

    if state == 'L' and occuped == 0:
        return '#'

    if state == '#' and occuped >= 5:
        return 'L'

    return state

def step2(field):
    new_field = []
    cache = {}
    for i in range(0, len(field)):
        new_line = []
        for j in range(0, len(field[i])):
            new_line.append(get_new_state2(field, i, j, cache))

        new_field.append(new_line)

    return new_field

field_1 = field

while True:
    new_field = step(field_1)
    if field_1 == new_field:
        break;
    field_1 = new_field

field_2 = field

while True:
    new_field = step2(field_2)
    if field_2 == new_field:
        break;
    field_2 = new_field

print("Part 1: %d" % (count_occuped(field_1)))
print("Part 2: %d" % (count_occuped(field_2)))



