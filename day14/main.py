import sys

if len(sys.argv) <= 1:
    raise Exception("No inputs")

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()


class Computer():
    def __init__(self):
        self.state = {}
    
    def set_mask(self, mask):
        self.or_mask = int(mask.replace('X','0'), 2)
        self.and_mask = int(mask.replace('X','1'), 2)

    def process(self, address, value):
        val = value & self.and_mask | self.or_mask
        self.state[address] = val
    
    def result(self):
        return sum(self.state.values())
    

class ComputerMk2(Computer):

    def set_mask(self, mask):
        self.or_mask = int(mask.replace('X','0'), 2)
        pos = []
        for i in range(0, len(mask)):
            if mask[i] == 'X':
                pos.append(i)

        self.mask_pos = pos


    def process(self, address, value):
        add = list('{0:0{1}b}'.format(address | self.or_mask, 36))
        for i in range(0, 2 ** len(self.mask_pos)):
            for p in self.mask_pos:
                add[p] = str(i & 1)
                i = i >> 1

            result_add = int(''.join(add), 2)
            self.state[result_add] = value





p = Computer()
p2 = ComputerMk2()

for line in lines:
    l = line.rstrip()
    if l.startswith('mask = '):
        mask = l[7:]
        p.set_mask(mask)
        p2.set_mask(mask)
    else:
        address, val = map(int, l[4:].split('] = '))
        p.process(address, val)
        p2.process(address, val)


print("Part 1: %d" % p.result())
print("Part 2: %d" % p2.result())