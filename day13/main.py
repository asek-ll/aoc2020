import sys
import math

if len(sys.argv) <= 1:
    raise Exception("No inputs")

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()

def get_bus_times(seqs):
    res = {}
    last_id = None
    for i in range(0, len(bus_seq)):
        id = bus_seq[i]
        if id == 'x':
            id = last_id
        else:
            id = int(id)
            last_id = id
            res[id] = []

        res[id].append(i)

    return res


time = int(lines[0].rstrip())
buses = [int(id) for id in lines[1].rstrip().split(",") if id != 'x' ]

buses.sort()

def find_min_wait_time(buses, target):
    id_to_wait = [(b, (b - target % b) % b) for b in buses]
    m = min(id_to_wait, key = lambda x: x[1])
    return m[0] * m[1]

print("Part 1: %d" % find_min_wait_time(buses, time))


bus_seq = [id for id in lines[1].rstrip().split(",") ]

def check(t, bus_times):
    for id in bus_times:
        any_match = False
        shift = bus_times[id][0]
        if (t + shift) % id == 0:
            any_match = True
                # break
        if not any_match:
            return False

    return True

def find_t_old(bus_times):
    m = max(buses)
    i = 0
    s = int(math.ceil(min(bus_times[m])/float(m)))
    while True:
        for shift in bus_times[m]:
            t = s * m - shift
            if check(t, bus_times):
                return t

            s += 1

def find_back_m(m, a):
    for x in range(1, a):
        if (m * x) % a == 1:
            return x

def find_t(bus_times):
    m = 1
    for id in bus_times:
        m *= id

    res = 0
    for id in bus_times:
        mi = m / id
        ri = (id - bus_times[id][0]) % id
        mi_1 = find_back_m(mi, id)
        res += (ri * mi * mi_1) % m

    return res % m



def explain(t, bus_times):
    s = max(0, t - 8)
    e = t + 15

    buses = [int(id) for id in lines[1].rstrip().split(",") if id != 'x' ]

    header = ['time']
    for b in buses:
        header.append('bus %d' % b)

    header_tmpl = ' '.join(["%10s" for b in header])
    
    
    print(header_tmpl % tuple(header))
    for i in range(s, e):
        row = [str(i)]
        for b in buses:
            if i % b == 0:
                row.append('D')
            else:
                row.append('.')

        print(header_tmpl % tuple(row))



bus_times = get_bus_times(bus_seq)
min_t = find_t(bus_times)
print("Part 2: %d" % min_t)
