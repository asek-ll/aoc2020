import sys

if len(sys.argv) <= 1:
    raise Exception("No inputs")

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()


field = [list(l.rstrip()) for l in lines]
state = []
for i in range(0, len(field)):
    for j in range(0, len(field[i])):
        if field[i][j] == '#':
            state.append((i,j,0))



def get_neigbor(c):
    res = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            for z in range(-1, 2):
                if x == 0 and y == 0 and z == 0:
                    continue 
                res.append((c[0]+x, c[1]+y, c[2]+z))

    return res
                
def get_neigbor4(c):
    res = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            for z in range(-1, 2):
                for w in range(-1, 2):
                    if x == 0 and y == 0 and z == 0 and w == 0:
                        continue 
                    res.append((c[0]+x, c[1]+y, c[2]+z, c[3]+w))

    return res
                

def count_active(s, nei):
    c = 0
    for n in nei:
        if n in s:
            c+=1
    
    return c

def next_state(s, gn = get_neigbor):
    ns = set([])
    active_neibor_by_neibor = {}
    for c in s:
        nei = gn(c)
        active_neigbor = count_active(s, nei)
        if active_neigbor == 2 or active_neigbor == 3:
            ns.add(c)

        for n in nei:
            if n not in s:
                if n not in active_neibor_by_neibor:
                    active_neibor_by_neibor[n] = 1
                else:
                    active_neibor_by_neibor[n] += 1

    for c in active_neibor_by_neibor:
        if active_neibor_by_neibor[c] == 3:
            ns.add(c)


    return ns


def debug(s, l):
    print("z=%d" % l)
    for i in range(-1, 4):
        o = []
        for j in range(-1, 4):
            if (i,j,l) in s:
                o.append('#')
            else:
                o.append('.')
        print(''.join(o))

ns = state
for i in range(0, 6):
    ns = next_state(ns)

print("Part 1: %d" % len(ns))


state4 = []
for i in range(0, len(field)):
    for j in range(0, len(field[i])):
        if field[i][j] == '#':
            state4.append((i,j,0,0))

ns = state4
for i in range(0, 6):
    ns = next_state(ns, get_neigbor4)

print("Part 2: %d" % len(ns))