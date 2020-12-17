import sys

if len(sys.argv) <= 1:
    raise Exception("No inputs")

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()

CMD = {
        'nop': lambda arg, s: (s[0]+1, s[1]),
        'acc': lambda arg, s: (s[0]+1, s[1] + arg),
        'jmp': lambda arg, s: (s[0]+arg, s[1]),
        }

def parse(lines):
    res = []
    for line in lines:
        cmd, op = line.rstrip().split(' ')
        res.append((cmd, int(op)))

    return res

def step(program, state):
    line = state[0]
    cmd = program[line]

    return CMD[cmd[0]](cmd[1], state)

def find_cycle(program):
    processed = set([])

    state = (0, 0)

    while state[0] not in processed and state[0] < len(program):
        processed.add(state[0])
        state = step(program, state)


    return state

BUGS = {
        'jmp': 'nop',
        'nop': 'jmp'
        }

def find_bug(program):
    for i in range(0, len(program)):
        cmd = program[i]
        if cmd[0] in BUGS:
            new_cmd = (BUGS[cmd[0]], cmd[1])
            program[i] = new_cmd
            state = find_cycle(program)
            program[i] = cmd

            if state[0] == len(program):
                return state[1]
            

    return 0


program = parse(lines)


print("Part 1: %d" % find_cycle(program)[1])
print("Part 2: %d" % find_bug(program))




