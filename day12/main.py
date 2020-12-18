import sys
# import turtle

if len(sys.argv) <= 1:
    raise Exception("No inputs")

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()

def parse_cmd(line):
    l = line.rstrip()
    c = l[0]
    arg = int(l[1:])

    return (c, arg)

DIRECTIONS = {
    0: (1, 0),
    1: (0, 1),
    2: (-1, 0),
    3: (0, -1),
}

def forward(p, arg):
    err = p[2] % 90
    if err > 0:
        raise Exception("Invalid degree")

    d = p[2] / 90

    change = DIRECTIONS[d]

    return (p[0] + change[0] * arg, p[1] + change[1] * arg, p[2])

CMD = {
    'E': lambda p, arg: (p[0] + arg, p[1], p[2]),
    'W': lambda p, arg: (p[0] - arg, p[1], p[2]),
    'N': lambda p, arg: (p[0], p[1] + arg, p[2]),
    'S': lambda p, arg: (p[0], p[1] - arg, p[2]),
    'L': lambda p, arg: (p[0], p[1] , (p[2] + arg) % 360),
    'R': lambda p, arg: (p[0], p[1] , (p[2] + 360 - arg % 360) % 360),
    'F': forward,
}


def waypoint_left(state, arg):
    arg = arg % 360

    if arg == 0:
        return state

    waypoint = state[0]
    pos = state[1]
    d = CMD['L'](waypoint, arg)[2]

    if arg == 90:
        return ((-waypoint[1], waypoint[0], d), pos)

    if arg == 180:
        return ((-waypoint[0], -waypoint[1], d), pos)

    if arg == 270:
        return ((waypoint[1], -waypoint[0], d), pos)


def waypoint_right(state, arg):
    return waypoint_left(state, 360 - (arg % 360))

def waypoint_forward(state, arg):
    waypoint = state[0]
    pos = state[1]
    next_pos = (pos[0] + arg * waypoint[0] , pos[1] + arg * waypoint[1])
    return (waypoint, next_pos)

CMD2 = {
    'L': waypoint_left,
    'R': waypoint_right,
    'F': waypoint_forward,
}

def wrap(c):
    def wrapped(state, arg):
        return (CMD[c](state[0], arg), state[1])
    return wrapped
for c in ['E','N','W','S']:
    CMD2[c] = wrap(c)

def next_pos(pos, cmd):
    np = CMD[cmd[0]](pos, cmd[1])
    # turtle.goto(np[0], np[1])
    # turtle.setheading(np[2])
    return np

def next_state(state, cmd):
    return CMD2[cmd[0]](state, cmd[1])


cmds = [parse_cmd(l) for l in lines]

pos = (0, 0, 0)

for cmd in cmds:
    pos = next_pos(pos, cmd)

print("Part 1: %d" % (abs(pos[0]) + abs(pos[1])))

state = ((10,1,0), (0, 0))

for cmd in cmds:
    state = next_state(state, cmd)

print("Part 2: %d" % (abs(state[1][0]) + abs(state[1][1])))
