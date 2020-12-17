import sys
from itertools import groupby

if len(sys.argv) <= 1:
    raise Exception("No inputs")

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()


nums = [int(l.rstrip()) for l in lines]

def diffs(orig_nums):
    nums = list(orig_nums)
    nums.append(0)
    nums.sort()
    nums.append(nums[-1]+3)


    d = map(lambda p: p[0]-p[1], zip(nums[1:], nums[:-1]))
    d.sort()
    
    res = {}

    for k, g in groupby(d):
        res[k] = len(list(g))

    return res



def arrangements(nums):
    nums = list(nums)
    nums.append(0)
    nums.sort()
    nums.append(nums[-1]+3)

    cache = {}

    def count(pos):
        if len(nums) == pos+1:
            return 1

        if pos in cache:
            return cache[pos]

        res = 0

        i = pos+1
        while i < len(nums) and nums[i] - nums[pos] <= 3:
            res += count(i)
            i += 1

        cache[pos] = res

        return res

    return count(0)





d = diffs(nums)
print("Part 1: %d" % (d[1] * d[3]))


a = arrangements(nums)
print("Part 2: %d" % a)
