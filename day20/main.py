import sys

if len(sys.argv) <= 1:
    raise Exception("No inputs")

with open(sys.argv[1], 'r') as f:
    lines = [l.rstrip() for l in f.readlines()]

def read_tiles(ls):
    i = 0
    tiles = []

    while i < len(ls):
        l = ls[i]
        title, id = l[:-1].split(' ')
        i += 1
        m = []
        while i < len(ls) and len(ls[i]) > 0:
            l = ls[i]
            m.append(list(l))
            i += 1

        tiles.append((int(id), m))
        i += 1

    return tiles


def get_corners(m):
    corners = [tuple(m[0])]

    corners.append(tuple(l[len(l)-1] for l in m))
    corners.append(tuple(m[len(m)-1]))
    corners.append(tuple(l[0] for l in m))

    return corners


tiles = read_tiles(lines)
H = len(tiles[0][1])

tile_by_id = {t[0]: t[1] for t in tiles}
corners_for_tile = {t[0]: get_corners(t[1]) for t in tiles}
tile_for_corner = {}
for id in corners_for_tile:
    cs = corners_for_tile[id]
    for c in cs: 
        c_r = c[::-1]
        if c not in tile_for_corner and c_r not in tile_for_corner:
            tile_for_corner[c] = set([])

        if c in tile_for_corner:
            tile_for_corner[c].add(id)
        elif c_r in tile_for_corner:
            tile_for_corner[c_r].add(id)


def find_corners(ts, t_by_c):
    corners = []
    for tid in ts:
        non_matched = []
        for c in ts[tid]:
            uniq = True
            if c in t_by_c and len(t_by_c[c]) > 1:
                uniq = False
            i_c = c[::-1]
            if i_c in t_by_c and len(t_by_c[i_c]) > 1:
                uniq = False
            
            if uniq:
                non_matched.append(c)
                
        if len(non_matched) == 2:
            corners.append((tid, non_matched))

    return corners
        

def part1(c):
    res = 1
    for i in c:
        res *= i[0]
    return res

corners = find_corners(corners_for_tile, tile_for_corner)
print("Part 1: %d" % part1(corners))

c1 = corners[0]

def print_tile(mp):
    for r in mp:
        print("".join(r))

def rotate(tid, count = 1):
    for i in range(0, count):
        mp = tile_by_id[tid]
        mp2 = []
        for i in range(0, len(mp)):
            rw = []
            mp2.append(rw)
            for j in range(0, len(mp)):
                rw.append(mp[len(mp)-j-1][i])

        
        tile_by_id[tid] = mp2


    corners_for_tile[tid] = get_corners(tile_by_id[tid])

def reverse(tid, vert):
    if vert:
        tile_by_id[tid] = tile_by_id[tid][::-1]

    else:
        mp = tile_by_id[tid]
        mp2 = []

        for r in mp:
            mp2.append(r[::-1])

        tile_by_id[tid] = mp2


    corners_for_tile[tid] = get_corners(tile_by_id[tid])


def rotate_corner(c):
    c1 = c[1][0]
    c2 = c[1][1]

    cs = corners_for_tile[c[0]]
    c1i = cs.index(c1)

    rotate(c[0], 3-c1i)



rotate_corner(c1)

def find_right_tile(tid):
    r_c = corners_for_tile[tid][1]
    print("SEARCH")
    print(r_c)
    if r_c in tile_for_corner:
        tids = tile_for_corner[r_c]
        if len(tids) == 1:
            return None

        r_tid = next(iter(tids.difference(set([tid]))))

        r_c_i = r_c[::-1]
        r_corners = corners_for_tile[r_tid]
        for i in range(0, len(r_corners)):
            c = r_corners[i]
            if c == r_c:
                rotate(r_tid, 3-i)
                return r_tid

            if c == r_c_i:
                rotate(r_tid, 3-i)
                reverse(r_tid, True)
                return r_tid
            
    else:
        raise Exception("WTF???")


def find_bot_tile(tid):
    r_c = corners_for_tile[tid][2]
    print("B SEARCH")
    print(r_c)
    if r_c in tile_for_corner:
        tids = tile_for_corner[r_c]
        print(len(tids))
        if len(tids) == 1:
            return None


        r_tid = next(iter(tids.difference(set([tid]))))

        r_c_i = r_c[::-1]
        r_corners = corners_for_tile[r_tid]
        for i in range(0, len(r_corners)):
            c = r_corners[i]
            if c == r_c:
                rotate(r_tid, 4-i)
                return r_tid

            if c == r_c_i:
                rotate(r_tid, 4-i)
                reverse(r_tid, True)
                return r_tid
            
    else:
        raise Exception("WTF???")


def restore_line(s_tid):
    r = [s_tid]
    c_tid = s_tid
    while True:
        n_tid = find_right_tile(c_tid)
        if n_tid is not None:
            c_tid = n_tid
            r.append(c_tid)
        else:
            return r


def jm(pt):
    res = []
    for r in pt:
        for i in range(0, H):
            l = []
            for tid in r:
                mp = tile_by_id[tid]
                l.append("".join(mp[i]))
                l.append(" ")
            res.append("".join(l))
            print("".join(l))

    return jm



restored = []
rl = restore_line(c1[0])
restored.append(rl)
jm(restored)
i = 0
while True:
    b_t = find_bot_tile(restored[i][0])
    if b_t is None:
        break

    restored.append(restore_line(b_t))
    i += 1


jm(restored)